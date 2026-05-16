# Frontend Snippets

Ready-to-paste code for common Krea integration patterns. SvelteKit and React variants.

## 1. Server route: submit + poll

### SvelteKit (`src/routes/api/generate/+server.ts`)

```typescript
import { json } from "@sveltejs/kit";
import { generateImage, pollJob } from "$lib/krea";

export async function POST({ request }) {
  const { prompt, model = "bfl/flux-1-dev", aspectRatio = "16:9" } = await request.json();

  // Validate
  if (typeof prompt !== "string" || prompt.trim().length === 0 || prompt.length > 2000) {
    return json({ error: "Invalid prompt" }, { status: 400 });
  }

  try {
    const { job_id } = await generateImage({
      model,
      prompt: prompt.trim(),
      aspectRatio,
    });
    const job = await pollJob(job_id, { interval: 5_000, timeout: 120_000 });
    return json({ urls: job.result?.urls ?? [] });
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Unknown error";
    return json({ error: msg }, { status: 500 });
  }
}
```

### Next.js (`app/api/generate/route.ts`)

```typescript
import { NextResponse } from "next/server";
import { generateImage, pollJob } from "@/lib/krea";

export async function POST(req: Request) {
  const { prompt, model = "bfl/flux-1-dev", aspectRatio = "16:9" } = await req.json();

  if (typeof prompt !== "string" || prompt.trim().length === 0 || prompt.length > 2000) {
    return NextResponse.json({ error: "Invalid prompt" }, { status: 400 });
  }

  try {
    const { job_id } = await generateImage({
      model,
      prompt: prompt.trim(),
      aspectRatio,
    });
    const job = await pollJob(job_id, { interval: 5_000, timeout: 120_000 });
    return NextResponse.json({ urls: job.result?.urls ?? [] });
  } catch (err) {
    const msg = err instanceof Error ? err.message : "Unknown error";
    return NextResponse.json({ error: msg }, { status: 500 });
  }
}
```

## 2. Generator form (Svelte component)

```svelte
<script lang="ts">
  let prompt = $state("");
  let loading = $state(false);
  let urls = $state<string[]>([]);
  let error = $state<string | null>(null);

  async function generate() {
    if (!prompt.trim()) return;
    loading = true;
    error = null;
    urls = [];
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? `HTTP ${res.status}`);
      urls = data.urls;
    } catch (err) {
      error = err instanceof Error ? err.message : "Unknown error";
    } finally {
      loading = false;
    }
  }
</script>

<form onsubmit={(e) => { e.preventDefault(); generate(); }}>
  <textarea
    bind:value={prompt}
    placeholder="Describe what to generate..."
    maxlength="2000"
    disabled={loading}
  ></textarea>
  <button type="submit" disabled={loading || !prompt.trim()}>
    {loading ? "Generating..." : "Generate"}
  </button>
</form>

{#if error}
  <p class="error">{error}</p>
{/if}

{#if urls.length > 0}
  <div class="results">
    {#each urls as url}
      <img src={url} alt="Generated image" />
    {/each}
  </div>
{/if}
```

## 3. Generator form (React component)

```tsx
"use client";

import { useState, FormEvent } from "react";

export function Generator() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [urls, setUrls] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!prompt.trim()) return;
    setLoading(true);
    setError(null);
    setUrls([]);
    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? `HTTP ${res.status}`);
      setUrls(data.urls);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <form onSubmit={onSubmit}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe what to generate..."
          maxLength={2000}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !prompt.trim()}>
          {loading ? "Generating..." : "Generate"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}
      {urls.length > 0 && (
        <div className="results">
          {urls.map((url) => (
            <img key={url} src={url} alt="Generated image" />
          ))}
        </div>
      )}
    </>
  );
}
```

## 4. Streaming progress (Server-Sent Events)

For better UX on video generation, stream status updates from server to client.

### SvelteKit endpoint

```typescript
// src/routes/api/generate-stream/+server.ts
import { generateImage, getJob } from "$lib/krea";

export async function POST({ request }) {
  const { prompt, model = "bfl/flux-1-dev" } = await request.json();

  const stream = new ReadableStream({
    async start(controller) {
      const enc = new TextEncoder();
      const send = (event: string, data: unknown) =>
        controller.enqueue(
          enc.encode(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`),
        );

      try {
        const { job_id } = await generateImage({ model, prompt });
        send("submitted", { jobId: job_id });

        const start = Date.now();
        while (Date.now() - start < 600_000) {
          const job = await getJob(job_id);
          send("status", { status: job.status, elapsed: Date.now() - start });
          if (job.status === "completed") {
            send("done", { urls: job.result?.urls ?? [] });
            break;
          }
          if (job.status === "failed" || job.status === "cancelled") {
            send("error", { message: job.error ?? job.status });
            break;
          }
          await new Promise((r) => setTimeout(r, 5_000));
        }
      } catch (err) {
        send("error", { message: err instanceof Error ? err.message : "unknown" });
      } finally {
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
```

### Client (Svelte)

```svelte
<script lang="ts">
  let status = $state("idle");
  let urls = $state<string[]>([]);

  async function startStream(prompt: string) {
    const res = await fetch("/api/generate-stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    if (!res.body) return;
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split("\n\n");
      buffer = parts.pop() ?? "";
      for (const part of parts) {
        const lines = part.split("\n");
        const event = lines.find((l) => l.startsWith("event:"))?.slice(7);
        const data = lines.find((l) => l.startsWith("data:"))?.slice(6);
        if (!event || !data) continue;
        const payload = JSON.parse(data);
        if (event === "status") status = payload.status;
        if (event === "done") urls = payload.urls;
        if (event === "error") status = `error: ${payload.message}`;
      }
    }
  }
</script>
```

## 5. Static page with hardcoded assets (the productize step)

Once a user has approved a set of generations, hardcode the URLs. No runtime API.

### Svelte

```svelte
<script lang="ts">
  type Image = { url: string; title: string; caption: string };

  const moodboard: Image[] = [
    {
      url: "https://krea.../approved-night-towers.png",
      title: "Night towers",
      caption: "Rain-slicked neon, low angle",
    },
    {
      url: "https://krea.../approved-rainy-streets.png",
      title: "Rainy streets",
      caption: "Wet asphalt, sodium streetlights",
    },
    {
      url: "https://krea.../approved-aerial-grid.png",
      title: "Aerial grid",
      caption: "City from above, deep blue twilight",
    },
  ];
</script>

<section class="moodboard">
  {#each moodboard as img}
    <figure>
      <img src={img.url} alt={img.title} loading="lazy" />
      <figcaption>
        <h3>{img.title}</h3>
        <p>{img.caption}</p>
      </figcaption>
    </figure>
  {/each}
</section>
```

### React

```tsx
const moodboard = [
  { url: "https://krea.../approved-1.png", title: "Night towers", caption: "..." },
  { url: "https://krea.../approved-2.png", title: "Rainy streets", caption: "..." },
  { url: "https://krea.../approved-3.png", title: "Aerial grid", caption: "..." },
];

export default function Moodboard() {
  return (
    <section className="moodboard">
      {moodboard.map((img) => (
        <figure key={img.url}>
          <img src={img.url} alt={img.title} loading="lazy" />
          <figcaption>
            <h3>{img.title}</h3>
            <p>{img.caption}</p>
          </figcaption>
        </figure>
      ))}
    </section>
  );
}
```

## 6. Upload user file to Krea

```typescript
// SvelteKit form action for handling file uploads
import { json } from "@sveltejs/kit";
import { readFileSync } from "node:fs";

async function uploadToKrea(localPath: string, mimeType: string) {
  const key = process.env.KREA_API_KEY!;
  const data = readFileSync(localPath);
  const form = new FormData();
  form.append("file", new Blob([data], { type: mimeType }), localPath.split("/").pop()!);

  const res = await fetch("https://api.krea.ai/assets", {
    method: "POST",
    headers: { Authorization: `Key ${key}` },
    body: form,
  });
  if (!res.ok) throw new Error(`Krea upload failed: ${res.status}`);
  const asset = await res.json();
  return asset.url as string;
}
```

## 7. Cache the same prompt → same result

```typescript
import { createHash } from "node:crypto";

const cache = new Map<string, { urls: string[]; expires: number }>();

function inputHash(body: Record<string, unknown>): string {
  return createHash("sha256").update(JSON.stringify(body)).digest("hex");
}

export async function generateImageCached(body: Record<string, unknown>) {
  const key = inputHash(body);
  const now = Date.now();
  const hit = cache.get(key);
  if (hit && hit.expires > now) return hit.urls;

  const { job_id } = await apiPost(`/generate/image/${body.model}`, body);
  const job = await pollJob(job_id);
  const urls = job.result?.urls ?? [];
  cache.set(key, { urls, expires: now + 24 * 3600 * 1000 });
  return urls;
}
```

For production use a real cache layer (Redis, KV, file system) — the Map above doesn't survive a server restart.
