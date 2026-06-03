#!/usr/bin/env python3
"""Generate and download image assets with an OpenAI-compatible images API.

Usage:
  export ARK_API_KEY="your-key"
  python3 scripts/seedream_generate.py --manifest video/ep001/assets/image-generation-tasks.json --dry-run
  python3 scripts/seedream_generate.py --manifest video/ep001/assets/image-generation-tasks.json --limit 1

The script keeps secrets out of manifests and chat transcripts. It loads
ARK_API_KEY from the environment or a local .env file without printing it.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEFAULT_MODEL = "doubao-seedream-5-0-lite-260128"


def load_dotenv(path: Path = Path(".env")) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def http_json(method: str, url: str, api_key: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed: HTTP {exc.code}\n{raw}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{method} {url} failed: {exc}") from exc
    return json.loads(raw)


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "aiduanju-seedream-generator/1.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        target.write_bytes(response.read())


def save_base64(data: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if "," in data and data.split(",", 1)[0].startswith("data:"):
        data = data.split(",", 1)[1]
    target.write_bytes(base64.b64decode(data))


def first_image_item(response: dict[str, Any]) -> dict[str, Any]:
    for key in ("data", "images", "image"):
        value = response.get(key)
        if isinstance(value, list) and value:
            first = value[0]
            if isinstance(first, dict):
                return first
            if isinstance(first, str):
                return {"url": first}
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            return {"url": value}
    if isinstance(response.get("url"), str):
        return {"url": response["url"]}
    if isinstance(response.get("b64_json"), str):
        return {"b64_json": response["b64_json"]}
    raise RuntimeError(f"No image payload found in response: {response}")


def build_payload(task: dict[str, Any], defaults: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    payload = dict(task.get("payload") or {})
    payload.setdefault("model", args.model or task.get("model") or defaults.get("model") or os.getenv("SEEDREAM_MODEL", DEFAULT_MODEL))
    payload.setdefault("prompt", task["prompt"])
    negative_prompt = task.get("negative_prompt") or defaults.get("negative_prompt")
    if negative_prompt and "negative_prompt" not in payload:
        payload["negative_prompt"] = negative_prompt

    size = args.size or task.get("size") or defaults.get("size")
    if size:
        payload.setdefault("size", size)
    quality = args.quality or task.get("quality") or defaults.get("quality")
    if quality:
        payload.setdefault("quality", quality)
    response_format = args.response_format or task.get("response_format") or defaults.get("response_format")
    if response_format:
        payload.setdefault("response_format", response_format)
    return payload


def task_output_path(task: dict[str, Any], out_dir: Path) -> Path:
    raw = task.get("output_path") or task.get("target_path")
    if raw:
        return Path(raw)
    task_id = task.get("task_id") or task.get("asset_id") or "image"
    return out_dir / f"{task_id}.png"


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Generate short-drama image assets with Seedream or another image model.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--base-url", default=os.getenv("ARK_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model")
    parser.add_argument("--size")
    parser.add_argument("--quality")
    parser.add_argument("--response-format", choices=["url", "b64_json"])
    parser.add_argument("--tasks", help="Task ids or 1-based indexes, e.g. 1,3,5-7 or img_ep001_kf001")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    defaults = manifest.get("defaults", {})
    tasks = list(manifest.get("tasks", []))
    if not tasks:
        raise SystemExit("No image tasks found.")

    all_ids = [str(task.get("task_id") or task.get("asset_id") or index + 1) for index, task in enumerate(tasks)]
    if args.tasks:
        selected: set[str] = set()
        for part in args.tasks.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part and part.replace("-", "").isdigit():
                start_s, end_s = part.split("-", 1)
                for index in range(int(start_s), int(end_s) + 1):
                    if 1 <= index <= len(all_ids):
                        selected.add(all_ids[index - 1])
            elif part.isdigit() and 1 <= int(part) <= len(all_ids):
                selected.add(all_ids[int(part) - 1])
            else:
                selected.add(part)
        tasks = [task for task, task_id in zip(tasks, all_ids) if task_id in selected]
    if args.limit:
        tasks = tasks[: args.limit]

    out_dir = args.out_dir or Path(manifest.get("out_dir", args.manifest.parent))
    payload_dir = out_dir / "payloads"
    result_dir = out_dir / "results"
    api_key = os.getenv("ARK_API_KEY")
    if not args.dry_run and not api_key:
        raise SystemExit("Missing ARK_API_KEY. Set it in your shell instead of putting it in files or chat.")

    endpoint = f"{args.base_url.rstrip('/')}/images/generations"
    for task in tasks:
        task_id = str(task.get("task_id") or task.get("asset_id"))
        if not task_id:
            raise SystemExit(f"Task missing task_id/asset_id: {task}")
        output_path = task_output_path(task, out_dir)
        if args.skip_existing and output_path.exists():
            print(f"skipped existing {output_path}")
            continue

        payload = build_payload(task, defaults, args)
        write_json(payload_dir / f"{task_id}.json", payload)
        if args.dry_run:
            print(f"DRY-RUN payload written: {payload_dir / (task_id + '.json')}")
            continue

        response = http_json("POST", endpoint, api_key, payload)
        write_json(result_dir / f"{task_id}.json", response)
        image = first_image_item(response)
        if isinstance(image.get("url"), str):
            download(image["url"], output_path)
        elif isinstance(image.get("b64_json"), str):
            save_base64(image["b64_json"], output_path)
        else:
            raise RuntimeError(f"No url/b64_json found for {task_id}: {response}")
        print(f"downloaded {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
