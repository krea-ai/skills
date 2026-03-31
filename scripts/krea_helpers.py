# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""Shared helpers for Krea AI scripts: API calls, polling, retry, error handling."""

import json
import os
import platform
import shutil
import subprocess
import sys
import time
import mimetypes
import requests

API_BASE = "https://api.krea.ai"

# ── Model endpoint maps (single source of truth) ─────────

IMAGE_MODELS = {
    "z-image": "/generate/image/z-image/z-image",
    "flux": "/generate/image/bfl/flux-1-dev",
    "flux-kontext": "/generate/image/bfl/flux-1-kontext-dev",
    "flux-pro": "/generate/image/bfl/flux-1.1-pro",
    "flux-pro-ultra": "/generate/image/bfl/flux-1.1-pro-ultra",
    "nano-banana": "/generate/image/google/nano-banana",
    "nano-banana-flash": "/generate/image/google/nano-banana-flash",
    "nano-banana-pro": "/generate/image/google/nano-banana-pro",
    "imagen-3": "/generate/image/google/imagen-3",
    "imagen-4": "/generate/image/google/imagen-4",
    "imagen-4-fast": "/generate/image/google/imagen-4-fast",
    "imagen-4-ultra": "/generate/image/google/imagen-4-ultra",
    "ideogram-2-turbo": "/generate/image/ideogram/ideogram-2-turbo",
    "ideogram-3": "/generate/image/ideogram/ideogram-3",
    "gpt-image": "/generate/image/openai/gpt-image",
    "runway-gen4": "/generate/image/runway/gen-4",
    "seedream-3": "/generate/image/bytedance/seedream-3",
    "seedream-4": "/generate/image/bytedance/seedream-4",
    "seedream-5-lite": "/generate/image/bytedance/seedream-5-lite",
    "qwen": "/generate/image/qwen/2512",
}

VIDEO_MODELS = {
    "kling-1.0": "/generate/video/kling/kling-1.0",
    "kling-1.5": "/generate/video/kling/kling-1.5",
    "kling-2.5": "/generate/video/kling/kling-2.5",
    "veo-3": "/generate/video/google/veo-3",
    "veo-3.1": "/generate/video/google/veo-3.1",
    "hailuo-2.3": "/generate/video/hailuo/hailuo-2.3",
    "wan-2.5": "/generate/video/alibaba/wan-2.5",
}

ENHANCERS = {
    "topaz": "/generate/enhance/topaz/standard-enhance",
    "topaz-generative": "/generate/enhance/topaz/generative-enhance",
    "topaz-bloom": "/generate/enhance/topaz/bloom-enhance",
}

DEFAULT_ENHANCER_MODELS = {
    "topaz": "Standard V2",
    "topaz-generative": "Redefine",
    "topaz-bloom": "Reimagine",
}

# ── CU cost estimates (used for dry-run) ─────────────────

IMAGE_MODEL_CU = {
    "z-image": 3, "flux": 5, "flux-kontext": 9, "flux-pro": 31,
    "flux-pro-ultra": 47, "nano-banana": 32, "nano-banana-flash": 48,
    "nano-banana-pro": 119, "imagen-3": 32, "imagen-4": 32,
    "imagen-4-fast": 16, "imagen-4-ultra": 47, "ideogram-2-turbo": 20,
    "ideogram-3": 54, "gpt-image": 184, "runway-gen4": 40,
    "seedream-3": 24, "seedream-4": 24, "seedream-5-lite": 28, "qwen": 9,
}

VIDEO_MODEL_CU = {
    "kling-1.0": 282, "kling-1.5": 300, "kling-2.5": 300,
    "veo-3": 1017, "veo-3.1": 1017, "hailuo-2.3": 300, "wan-2.5": 569,
}

ENHANCER_CU = {
    "topaz": 51, "topaz-generative": 137, "topaz-bloom": 256,
}


def resolve_model(model_arg, models_dict, prefix):
    """Resolve a short model name, raw suffix, or full endpoint path."""
    if model_arg in models_dict:
        return models_dict[model_arg]
    if model_arg.startswith(prefix):
        return model_arg
    for ep in models_dict.values():
        if ep.endswith("/" + model_arg):
            return ep
    print(f"Warning: Unknown model '{model_arg}', trying as endpoint path", file=sys.stderr)
    return f"{prefix}{model_arg}"


def get_cu_estimate(action, model_or_enhancer):
    """Return estimated CU cost for a model/enhancer, or None if unknown."""
    if action == "generate_image":
        return IMAGE_MODEL_CU.get(model_or_enhancer)
    elif action == "generate_video":
        return VIDEO_MODEL_CU.get(model_or_enhancer)
    elif action == "enhance":
        return ENHANCER_CU.get(model_or_enhancer)
    return None


# ── API key ──────────────────────────────────────────────

def get_api_key(args_key=None):
    key = args_key or os.environ.get("KREA_API_TOKEN")
    if not key:
        print("Error: No API key provided. Set KREA_API_TOKEN or pass --api-key", file=sys.stderr)
        sys.exit(1)
    return key


# ── Error formatting ─────────────────────────────────────

def format_api_error(status_code, response_text):
    """Return a human-readable error message for API errors."""
    msg = f"API error {status_code}"
    try:
        data = json.loads(response_text)
        error = data.get("error", "")
    except (json.JSONDecodeError, AttributeError):
        error = response_text

    if status_code == 401:
        return f"{msg}: Authentication failed. Check your KREA_API_TOKEN."
    elif status_code == 402:
        err_str = str(error).lower()
        if "insufficient" in err_str or "balance" in err_str:
            return f"{msg}: Insufficient credits. Top up at https://krea.ai/settings/billing"
        elif "plan" in err_str or "requires" in err_str:
            return f"{msg}: This model requires a higher plan. Upgrade at https://krea.ai/settings/billing"
        return f"{msg}: Payment required — {error}"
    elif status_code == 429:
        return f"{msg}: Rate limited (too many concurrent jobs). Will retry..."
    else:
        return f"{msg}: {error}"


# ── API call with retry ──────────────────────────────────

def api_post(api_key, endpoint, body, max_retries=3):
    """POST to the Krea API with automatic retry on 429."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    delays = [5, 15, 45]

    for attempt in range(max_retries + 1):
        r = requests.post(f"{API_BASE}{endpoint}", headers=headers, json=body)
        if r.ok:
            return r.json()
        if r.status_code == 429 and attempt < max_retries:
            delay = delays[min(attempt, len(delays) - 1)]
            print(f"  Rate limited, retrying in {delay}s (attempt {attempt + 1}/{max_retries})...", file=sys.stderr)
            time.sleep(delay)
            continue
        msg = format_api_error(r.status_code, r.text)
        print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)


def api_get(api_key, path, max_retries=3):
    """GET from the Krea API with automatic retry on 429."""
    headers = {"Authorization": f"Bearer {api_key}"}
    delays = [5, 15, 45]

    for attempt in range(max_retries + 1):
        r = requests.get(f"{API_BASE}{path}", headers=headers)
        if r.ok:
            return r.json()
        if r.status_code == 429 and attempt < max_retries:
            delay = delays[min(attempt, len(delays) - 1)]
            print(f"  Rate limited, retrying in {delay}s...", file=sys.stderr)
            time.sleep(delay)
            continue
        msg = format_api_error(r.status_code, r.text)
        print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)


# ── Job polling ──────────────────────────────────────────

def poll_job(api_key, job_id, interval=3, timeout=600):
    """Poll a job until it reaches a terminal state."""
    start = time.time()
    while time.time() - start < timeout:
        job = api_get(api_key, f"/jobs/{job_id}")
        status = job.get("status", "")
        if status == "completed":
            return job
        if status == "failed":
            error_detail = json.dumps(job.get("result", {}))
            print(f"Error: Job failed: {error_detail}", file=sys.stderr)
            sys.exit(1)
        if status == "cancelled":
            print("Error: Job was cancelled", file=sys.stderr)
            sys.exit(1)
        print(f"  [{job_id[:8]}] {status}...", file=sys.stderr)
        time.sleep(interval)
    print(f"Error: Job timed out after {timeout}s", file=sys.stderr)
    sys.exit(1)


# ── File download ────────────────────────────────────────

def download_file(url, filename):
    """Download a URL to a local file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True) if os.path.dirname(filename) else None
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return os.path.abspath(filename)


# ── Local image → URL helper ─────────────────────────────

def ensure_image_url(path_or_url, api_key):
    """If the input is a local file path, upload it via the Krea assets API
    and return the hosted URL. If it's already a URL, return as-is."""
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url

    local_path = path_or_url
    if local_path.startswith("file://"):
        local_path = local_path[7:]

    if not os.path.isfile(local_path):
        print(f"Error: Local file not found: {local_path}", file=sys.stderr)
        sys.exit(1)

    mime_type = mimetypes.guess_type(local_path)[0] or "application/octet-stream"
    ext = os.path.splitext(local_path)[1].lstrip(".")

    boundary = f"----KreaBoundary{int(time.time())}"
    with open(local_path, "rb") as f:
        file_data = f.read()

    parts = []
    parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"upload.{ext}\"\r\nContent-Type: {mime_type}\r\n\r\n".encode())
    parts.append(file_data)
    parts.append(b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())

    body = b"".join(parts)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }

    print(f"  Uploading local file: {local_path}...", file=sys.stderr)
    r = requests.post(f"{API_BASE}/assets", headers=headers, data=body)
    if not r.ok:
        msg = format_api_error(r.status_code, r.text)
        print(f"Error uploading asset: {msg}", file=sys.stderr)
        sys.exit(1)

    asset = r.json()
    url = asset.get("image_url") or asset.get("url")
    if not url:
        print(f"Error: Upload succeeded but no URL returned: {json.dumps(asset)}", file=sys.stderr)
        sys.exit(1)

    print(f"  Uploaded: {url}", file=sys.stderr)
    return url


# ── Output path helper ───────────────────────────────────

def output_path(filename, output_dir=None):
    """Join filename with output_dir if provided."""
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        return os.path.join(output_dir, os.path.basename(filename))
    return filename


# ── Desktop notification ─────────────────────────────────

def send_notification(title, message):
    """Send a desktop notification. Best-effort, never raises."""
    try:
        system = platform.system()
        if system == "Linux" and shutil.which("notify-send"):
            subprocess.run(["notify-send", title, message], timeout=5)
        elif system == "Darwin":
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], timeout=5)
        else:
            print("\a", end="", file=sys.stderr)
    except Exception:
        pass
