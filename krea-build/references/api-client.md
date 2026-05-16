# API Client — Auth, Polling, Errors

The Krea public API surface for building apps:

- **Base URL:** `https://api.krea.ai`
- **Auth:** `Authorization: Key ${KREA_API_KEY}` header
- **OpenAPI:** `https://api.krea.ai/openapi.json` — source of truth for endpoints and schemas

## TypeScript client

A minimal reusable helper. Drop into `src/lib/krea/index.ts` (SvelteKit/Vite) or `src/lib/krea.ts` (Next.js).

```typescript
const BASE_URL = "https://api.krea.ai";

function getHeaders() {
  const key = process.env.KREA_API_KEY;
  if (!key) throw new Error("KREA_API_KEY is not set");
  return {
    Authorization: `Key ${key}`,
    "Content-Type": "application/json",
  };
}

async function apiPost(path: string, body: Record<string, unknown>) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Krea API error ${res.status}: ${text}`);
  }
  return res.json();
}

async function apiGet(path: string) {
  const res = await fetch(`${BASE_URL}${path}`, { headers: getHeaders() });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Krea API error ${res.status}: ${text}`);
  }
  return res.json();
}

export type Job = {
  id: string;
  status: "queued" | "running" | "completed" | "failed" | "cancelled";
  result?: {
    urls?: string[];
    video_url?: string;
  };
  error?: string;
};

export async function getJob(jobId: string): Promise<Job> {
  return apiGet(`/jobs/${jobId}`) as Promise<Job>;
}

export async function pollJob(
  jobId: string,
  options: { interval?: number; timeout?: number } = {},
): Promise<Job> {
  const interval = options.interval ?? 5_000;       // 5 seconds
  const timeout = options.timeout ?? 600_000;        // 10 minutes
  const start = Date.now();

  while (Date.now() - start < timeout) {
    const job = await getJob(jobId);
    if (job.status === "completed") return job;
    if (job.status === "failed" || job.status === "cancelled") {
      throw new Error(`Job ${jobId} ${job.status}: ${job.error ?? "no detail"}`);
    }
    await new Promise((r) => setTimeout(r, interval));
  }
  throw new Error(`Job ${jobId} timed out after ${timeout}ms`);
}

export async function generateImage(input: {
  model: string;        // e.g. "bfl/flux-1-dev"
  prompt: string;
  width?: number;
  height?: number;
  aspectRatio?: string;
  batchSize?: number;
  imageUrl?: string;
  imageUrls?: string[];
  styleId?: string;
  styleStrength?: number;
}): Promise<{ job_id: string }> {
  const path = `/generate/image/${input.model}`;
  return apiPost(path, input);
}

export async function generateVideo(input: {
  model: string;        // e.g. "google/veo-3.1"
  prompt: string;
  duration?: number;
  aspectRatio?: string;
  startImage?: string;
  generateAudio?: boolean;
}): Promise<{ job_id: string }> {
  const path = `/generate/video/${input.model}`;
  return apiPost(path, input);
}

export async function enhanceImage(input: {
  enhancer: string;     // e.g. "topaz-standard-enhance"
  imageUrl: string;
  width: number;
  height: number;
  creativity?: number;
  faceEnhancement?: boolean;
}): Promise<{ job_id: string }> {
  return apiPost(`/generate/enhance/${input.enhancer}`, input);
}
```

## Usage pattern (server route)

SvelteKit `+server.ts`:

```typescript
import { json } from "@sveltejs/kit";
import { generateImage, pollJob } from "$lib/krea";

export async function POST({ request }) {
  const { prompt, model } = await request.json();

  // Server-side validation
  if (!prompt || prompt.length > 2000) {
    return json({ error: "Invalid prompt" }, { status: 400 });
  }

  // Submit and poll
  const { job_id } = await generateImage({ model, prompt });
  const job = await pollJob(job_id);

  return json({
    urls: job.result?.urls ?? [],
  });
}
```

Next.js `app/api/generate/route.ts`:

```typescript
import { NextResponse } from "next/server";
import { generateImage, pollJob } from "@/lib/krea";

export async function POST(req: Request) {
  const { prompt, model } = await req.json();

  if (!prompt || prompt.length > 2000) {
    return NextResponse.json({ error: "Invalid prompt" }, { status: 400 });
  }

  const { job_id } = await generateImage({ model, prompt });
  const job = await pollJob(job_id);

  return NextResponse.json({ urls: job.result?.urls ?? [] });
}
```

## Polling discipline

- **5–10 seconds** between polls for images and enhancement. Faster burns rate limits; slower wastes user time.
- **10–15 seconds** for video. Videos often run 30s–5min; faster polling adds nothing.
- **Cap at 10 minutes** total wall time. After that, the job is either stuck or running unusually long; surface to the user.
- **Don't poll from the browser.** Browser polling means N users = N polling streams hitting Krea, plus you've exposed `job_id` to the client. Poll server-side; stream status to the client over Server-Sent Events / WebSocket / one final response.

## Retries on 429

Krea returns `HTTP 429` when you hit concurrent job limits:

```typescript
async function apiPostWithRetry(
  path: string,
  body: Record<string, unknown>,
  attempt = 0,
): Promise<unknown> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify(body),
  });

  if (res.status === 429 && attempt < 3) {
    const delays = [5_000, 15_000, 45_000];
    await new Promise((r) => setTimeout(r, delays[attempt]));
    return apiPostWithRetry(path, body, attempt + 1);
  }

  if (!res.ok) {
    throw new Error(`Krea API ${res.status}: ${await res.text()}`);
  }
  return res.json();
}
```

## Python client (for backend services or scripts)

A minimal equivalent:

```python
import os
import time
import requests

BASE_URL = "https://api.krea.ai"


def _headers():
    key = os.environ["KREA_API_KEY"]
    return {"Authorization": f"Key {key}", "Content-Type": "application/json"}


def api_post(path, body, retries=3):
    delays = [5, 15, 45]
    for attempt in range(retries + 1):
        r = requests.post(f"{BASE_URL}{path}", headers=_headers(), json=body)
        if r.ok:
            return r.json()
        if r.status_code == 429 and attempt < retries:
            time.sleep(delays[min(attempt, len(delays) - 1)])
            continue
        r.raise_for_status()


def api_get(path):
    r = requests.get(f"{BASE_URL}{path}", headers=_headers())
    r.raise_for_status()
    return r.json()


def poll_job(job_id, interval=5, timeout=600):
    start = time.time()
    while time.time() - start < timeout:
        job = api_get(f"/jobs/{job_id}")
        if job["status"] == "completed":
            return job
        if job["status"] in ("failed", "cancelled"):
            raise RuntimeError(f"Job {job_id} {job['status']}: {job.get('error', '')}")
        time.sleep(interval)
    raise RuntimeError(f"Job {job_id} timed out")


def generate_image(model: str, **kwargs):
    return api_post(f"/generate/image/{model}", {"prompt": kwargs.pop("prompt"), **kwargs})


def generate_video(model: str, **kwargs):
    return api_post(f"/generate/video/{model}", {"prompt": kwargs.pop("prompt"), **kwargs})
```

## Caching

Same input → same output. Cache by hash of `(endpoint, body)`:

```typescript
import { createHash } from "crypto";

function inputHash(path: string, body: Record<string, unknown>): string {
  return createHash("sha256")
    .update(JSON.stringify({ path, body }))
    .digest("hex");
}

// Pseudocode — use whatever cache layer fits (KV, Redis, file)
async function cachedGenerate(path: string, body: Record<string, unknown>) {
  const key = inputHash(path, body);
  const cached = await cache.get(key);
  if (cached) return cached;

  const { job_id } = await apiPost(path, body);
  const job = await pollJob(job_id);
  await cache.set(key, job, { ttl: 86400 });
  return job;
}
```

For user-driven generators this saves enormous compute and gives instant repeat-prompt results.

## Discovering current model IDs

Don't hardcode model IDs from memory. Get the current list at build time or runtime:

```bash
curl https://api.krea.ai/openapi.json | jq '.paths | keys | map(select(startswith("/generate/")))'
```

This gives every available generation endpoint. The path tail after `/generate/<category>/<provider>/` is the model ID you pass to the helpers above.
