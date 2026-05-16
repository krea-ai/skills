# Validation

Anything coming from the user (browser, third-party API, untrusted input) must be validated server-side before being forwarded to Krea. This file covers the checks worth doing and the API errors to handle.

## Why validation matters

- **Cost.** Every unvalidated prompt is a CU burn. Catch nonsense before submitting.
- **Compliance.** Krea moderates content server-side, but flagged jobs still count against your quota. Pre-filter where you can.
- **UX.** Users see errors at submit time, not 30 seconds into a failed job.
- **Security.** Untrusted URL inputs can be SSRF vectors. Validate before forwarding.

## Server-side validation checklist

For any generation endpoint your app exposes:

### Prompts

```typescript
function validatePrompt(prompt: unknown): string {
  if (typeof prompt !== "string") throw new Error("prompt must be a string");
  const trimmed = prompt.trim();
  if (trimmed.length === 0) throw new Error("prompt cannot be empty");
  if (trimmed.length > 2000) throw new Error("prompt too long (max 2000 chars)");
  return trimmed;
}
```

Reasonable defaults:

- Minimum length: 1 char (don't enforce a higher floor — sometimes very short prompts are valid)
- Maximum length: 2000 chars (models distort with longer prompts anyway)
- Strip leading/trailing whitespace
- Don't strip Unicode — emoji and non-Latin scripts are valid

### Image URLs (user-provided)

The biggest risk: someone passes `file:///etc/passwd` or a local network URL. Filter:

```typescript
function validateImageUrl(url: unknown): string {
  if (typeof url !== "string") throw new Error("imageUrl must be a string");
  let u: URL;
  try {
    u = new URL(url);
  } catch {
    throw new Error("imageUrl must be a valid URL");
  }
  if (u.protocol !== "https:" && u.protocol !== "http:") {
    throw new Error("imageUrl must use http(s)");
  }
  // Block local network / metadata services
  const hostname = u.hostname.toLowerCase();
  if (
    hostname === "localhost" ||
    hostname.startsWith("127.") ||
    hostname.startsWith("169.254.") ||
    hostname.startsWith("10.") ||
    hostname.startsWith("172.") && parseInt(hostname.split(".")[1], 10) >= 16 && parseInt(hostname.split(".")[1], 10) < 32 ||
    hostname.startsWith("192.168.") ||
    hostname === "[::1]" ||
    hostname === "metadata.google.internal"
  ) {
    throw new Error("imageUrl cannot point to internal addresses");
  }
  return url;
}
```

For higher security: HEAD-check the URL before submitting. If it returns 4xx/5xx, reject early.

### Local file uploads

When the user attaches files:

- **Limit file size** (e.g. 25 MB). Krea accepts up to 50 MB but most use cases shouldn't.
- **Whitelist MIME types** — image/png, image/jpeg, image/webp, video/mp4, video/quicktime, audio/mpeg, audio/wav.
- **Re-validate the file content** (don't trust the client-reported MIME). Use a library like `file-type` (Node) or `python-magic` (Python).
- **Don't store the file path in the user-facing URL.** Generate a UUID for the public URL; map UUID → server path server-side.

### Parameter enums

Models declare allowed values for params like `aspectRatio` and `resolution`. Fetch the schema once and validate:

```typescript
// Cached on server startup
const ALLOWED_ASPECT_RATIOS = ["1:1", "16:9", "9:16", "4:3", "3:4", "21:9"];

function validateAspectRatio(value: unknown): string {
  if (typeof value !== "string") throw new Error("aspectRatio must be a string");
  if (!ALLOWED_ASPECT_RATIOS.includes(value)) {
    throw new Error(`aspectRatio must be one of: ${ALLOWED_ASPECT_RATIOS.join(", ")}`);
  }
  return value;
}
```

For dynamic enums, fetch `/openapi.json` at build time and generate types/validators from it.

### Numeric ranges

```typescript
function validateDimension(value: unknown, name: string, min = 512, max = 4096): number {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new Error(`${name} must be a number`);
  }
  if (value < min || value > max) {
    throw new Error(`${name} must be between ${min} and ${max}`);
  }
  return Math.round(value);
}
```

### Batch size

Cap below the API limit to avoid surprise bills:

```typescript
function validateBatchSize(value: unknown): number {
  const n = typeof value === "number" ? value : 1;
  if (n < 1 || n > 4) throw new Error("batchSize must be 1–4");
  return Math.round(n);
}
```

## Content moderation handling

Krea moderates content server-side. A flagged generation returns a `failed` status with reason. Common reasons:

- `nsfw` — sexually explicit content
- `ip_detected` — trademarked characters, copyrighted IP
- `violence` — graphic violence
- `personal_info` — recognizable real people (e.g. politicians, celebrities)

When you see these reasons:

```typescript
try {
  const job = await pollJob(jobId);
  return job.result.urls;
} catch (err) {
  const message = err.message.toLowerCase();
  if (message.includes("nsfw")) {
    throw new UserVisibleError(
      "This prompt was flagged as not safe for work. Please rephrase.",
      400,
    );
  }
  if (message.includes("ip_detected")) {
    throw new UserVisibleError(
      "This prompt references trademarked content. Please use a different subject.",
      400,
    );
  }
  // Re-throw unknown errors as 500
  throw err;
}
```

**Never auto-retry on moderation failures.** The system flagged it for a reason. Surface to the user and let them rephrase.

## Common API errors and how to handle them

| HTTP status | Meaning | Recovery |
|---|---|---|
| 200 | Job submitted, returns `{ job_id }` | poll |
| 400 | Bad request (missing required field) | fix request, retry |
| 401 | Bad / missing API key | surface clearly; check env |
| 402 | Insufficient credits OR plan required | direct user to billing; don't retry |
| 422 | Validation error from Krea | parse `detail`/`errors` and surface fields to user |
| 429 | Concurrent job limit | back off (5s, 15s, 45s) and retry |
| 500–599 | Server error | retry once with backoff; if still failing, surface |

Implementation:

```typescript
async function handleResponse<T>(res: Response): Promise<T> {
  if (res.ok) return res.json() as Promise<T>;

  const body = await res.text();
  let parsed: any;
  try {
    parsed = JSON.parse(body);
  } catch {
    parsed = { message: body };
  }

  switch (res.status) {
    case 401:
      throw new Error("Krea auth failed — check KREA_API_KEY");
    case 402:
      throw new UserVisibleError(
        parsed.message?.includes("plan")
          ? "This model requires a higher plan."
          : "Insufficient credits.",
        402,
      );
    case 422:
      // detail is an array of { loc, msg, type }
      const details = (parsed.detail ?? [])
        .map((d: any) => `${(d.loc ?? []).join(".")}: ${d.msg}`)
        .join("; ");
      throw new UserVisibleError(`Invalid input: ${details}`, 422);
    case 429:
      throw new RetryableError("Rate limited", 429);
    default:
      throw new Error(`Krea API ${res.status}: ${body.slice(0, 500)}`);
  }
}

// Helper classes
class UserVisibleError extends Error {
  constructor(public userMessage: string, public httpStatus: number) {
    super(userMessage);
  }
}
class RetryableError extends Error {
  constructor(message: string, public httpStatus: number) {
    super(message);
  }
}
```

## Pre-flight cost check

Krea exposes CU cost in the OpenAPI description for each endpoint. If you want to confirm cost before submitting (e.g. for batch jobs):

```typescript
async function estimateCost(endpoint: string): Promise<number | null> {
  const spec = await fetch("https://api.krea.ai/openapi.json").then((r) => r.json());
  const desc = spec.paths[endpoint]?.post?.description ?? "";
  const match = desc.match(/~?(\d+)\s*(?:CU|compute units)/i);
  return match ? parseInt(match[1], 10) : null;
}
```

Cache the OpenAPI spec — don't fetch on every request.

## Avoid common pitfalls

- **Don't trust `Content-Type` from the client.** Always re-detect on the server.
- **Don't echo error messages from Krea verbatim to the user.** Some messages contain internal details. Translate to user-friendly text.
- **Don't log API keys.** Even at debug level. Even partially. Just don't.
- **Don't store user-provided prompts as keys in a database without sanitizing.** SQL injection or NoSQL injection vectors.
- **Don't accept arbitrary `model` strings from the client.** Maintain an allowlist server-side, even if the API would accept other values.
