#!/usr/bin/env python3
"""Submit and download Doubao Seedance video generation tasks.

Usage:
  export ARK_API_KEY="your-key"
  python3 scripts/seedance_generate.py --manifest video/ep001/seedance-prompts.json --limit 1

The script never reads API keys from files by default. Keep secrets in the
environment, not in prompt manifests or chat transcripts.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
SUCCEEDED = {"succeeded", "completed", "success"}
FAILED = {"failed", "error", "cancelled", "canceled"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_dotenv(path: Path = Path(".env")) -> None:
    """Load simple KEY=VALUE pairs without printing secrets."""
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


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_shot_selector(selector: str | None, all_ids: list[str]) -> set[str] | None:
    if not selector:
        return None
    selected: set[str] = set()
    for part in selector.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part and part.replace("-", "").isdigit():
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            for index in range(start, end + 1):
                if 1 <= index <= len(all_ids):
                    selected.add(all_ids[index - 1])
            continue
        if part.isdigit():
            index = int(part)
            if 1 <= index <= len(all_ids):
                selected.add(all_ids[index - 1])
            continue
        selected.add(part)
    return selected


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
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed: HTTP {exc.code}\n{raw}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{method} {url} failed: {exc}") from exc
    return json.loads(raw)


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "aiduanju-seedance-generator/1.0"})
    with urllib.request.urlopen(request, timeout=300) as response:
        target.write_bytes(response.read())


def build_prompt(manifest: dict[str, Any], shot: dict[str, Any]) -> str:
    parts = [
        manifest.get("series_style", "").strip(),
        manifest.get("episode_style", "").strip(),
        shot["prompt"].strip(),
    ]
    negative = manifest.get("negative_prompt", "").strip()
    if negative:
        parts.append(f"避免：{negative}")
    return "\n".join(part for part in parts if part)


def encode_image(path: Path) -> str:
    media_type = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{media_type};base64,{encoded}"


def build_payload(manifest: dict[str, Any], shot: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    defaults = manifest.get("defaults", {})
    content: list[dict[str, Any]] = [{"type": "text", "text": build_prompt(manifest, shot)}]
    image_url = shot.get("image_url")
    if shot.get("image_path"):
        image_url = encode_image(Path(shot["image_path"]))
    if image_url:
        image_item: dict[str, Any] = {
            "type": "image_url",
            "image_url": {"url": image_url},
        }
        image_role = shot.get("image_role")
        if image_role:
            image_item["role"] = image_role
        content.append(image_item)

    payload = {
        "model": args.model or defaults.get("model", "doubao-seedance-1-5-pro-251215"),
        "content": content,
        "resolution": args.resolution or shot.get("resolution") or defaults.get("resolution", "720p"),
        "ratio": args.ratio or shot.get("ratio") or defaults.get("ratio", "9:16"),
        "duration": args.duration or shot.get("duration") or defaults.get("duration", 6),
        "seed": shot.get("seed", defaults.get("seed", 11)),
        "camera_fixed": shot.get("camera_fixed", defaults.get("camera_fixed", False)),
        "watermark": args.watermark if args.watermark is not None else defaults.get("watermark", False),
    }
    generate_audio = args.generate_audio if args.generate_audio is not None else shot.get("generate_audio", defaults.get("generate_audio"))
    if generate_audio is not None:
        payload["generate_audio"] = generate_audio
    return payload


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def extract_task_id(response: dict[str, Any]) -> str:
    task_id = response.get("id") or response.get("task_id")
    if not task_id:
        raise RuntimeError(f"Task response does not contain id/task_id: {response}")
    return str(task_id)


def extract_video_url(result: dict[str, Any]) -> str | None:
    content = result.get("content") or {}
    if isinstance(content, dict):
        value = content.get("video_url")
        if isinstance(value, str):
            return value
        if isinstance(value, list) and value:
            return str(value[0])
    value = result.get("video_url")
    if isinstance(value, str):
        return value
    return None


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Generate short-drama clips with Doubao Seedance.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--base-url", default=os.getenv("ARK_BASE_URL", DEFAULT_BASE_URL))
    parser.add_argument("--model")
    parser.add_argument("--resolution")
    parser.add_argument("--ratio")
    parser.add_argument("--duration", type=int)
    parser.add_argument("--generate-audio", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--watermark", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--shots", help="Shot ids or 1-based indexes, e.g. 1,3,5-7 or ep001_s001")
    parser.add_argument("--limit", type=int, help="Generate only the first N selected shots.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip shots whose mp4 already exists in clips/.")
    parser.add_argument("--dry-run", action="store_true", help="Write request payloads without calling the API.")
    parser.add_argument("--poll-only", action="store_true", help="Poll existing tasks from tasks.jsonl.")
    parser.add_argument("--poll-interval", type=int, default=12)
    parser.add_argument("--max-wait", type=int, default=1800)
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    episode = manifest.get("episode", "episode")
    default_out = Path("video") / f"ep{int(episode):03d}" if isinstance(episode, int) else Path("video") / str(episode)
    out_dir = args.out_dir or Path(manifest.get("out_dir", default_out))
    payload_dir = out_dir / "payloads"
    result_dir = out_dir / "results"
    clip_dir = out_dir / "clips"
    tasks_path = out_dir / "tasks.jsonl"

    shots = manifest.get("shots", [])
    all_ids = [shot["id"] for shot in shots]
    selected = parse_shot_selector(args.shots, all_ids)
    if selected is not None:
        shots = [shot for shot in shots if shot["id"] in selected]
    if args.limit:
        shots = shots[: args.limit]
    if args.skip_existing:
        shots = [shot for shot in shots if not (out_dir / "clips" / f"{shot['id']}.mp4").exists()]

    if not shots and not args.poll_only:
        raise SystemExit("No shots selected.")

    api_key = os.getenv("ARK_API_KEY")
    if not args.dry_run and not api_key:
        raise SystemExit("Missing ARK_API_KEY. Set it in your shell instead of putting it in files or chat.")

    base_url = args.base_url.rstrip("/")
    create_url = f"{base_url}/contents/generations/tasks"

    task_records: list[dict[str, Any]] = []
    if not args.poll_only:
        for shot in shots:
            payload = build_payload(manifest, shot, args)
            write_json(payload_dir / f"{shot['id']}.json", payload)
            if args.dry_run:
                print(f"DRY-RUN payload written: {payload_dir / (shot['id'] + '.json')}")
                continue
            response = http_json("POST", create_url, api_key, payload)
            task_id = extract_task_id(response)
            record = {
                "shot_id": shot["id"],
                "task_id": task_id,
                "request": payload,
                "response": response,
                "created_at": int(time.time()),
            }
            append_jsonl(tasks_path, record)
            task_records.append(record)
            print(f"submitted {shot['id']} -> {task_id}")

    if args.dry_run:
        return 0

    task_records = task_records or read_jsonl(tasks_path)
    if not task_records:
        raise SystemExit(f"No task records found: {tasks_path}")

    deadline = time.time() + args.max_wait
    pending = {record["task_id"]: record for record in task_records}
    while pending:
        if time.time() > deadline:
            raise SystemExit(f"Timed out with {len(pending)} pending tasks.")
        for task_id, record in list(pending.items()):
            result = http_json("GET", f"{create_url}/{task_id}", api_key)
            write_json(result_dir / f"{record['shot_id']}.json", result)
            status = str(result.get("status", "")).lower()
            print(f"{record['shot_id']} {task_id}: {status}")
            if status in SUCCEEDED:
                video_url = extract_video_url(result)
                if not video_url:
                    raise RuntimeError(f"Task succeeded without video_url: {result}")
                target = clip_dir / f"{record['shot_id']}.mp4"
                download(video_url, target)
                print(f"downloaded {target}")
                pending.pop(task_id)
            elif status in FAILED:
                pending.pop(task_id)
                print(f"failed {record['shot_id']}: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
        if pending:
            time.sleep(args.poll_interval)

    concat_list = out_dir / "concat.txt"
    clips = sorted(clip_dir.glob("*.mp4"))
    concat_list.write_text(
        "".join(f"file '{clip.resolve()}'\n" for clip in clips),
        encoding="utf-8",
    )
    print(f"concat list written: {concat_list}")
    print(f"ffmpeg example: ffmpeg -f concat -safe 0 -i {concat_list} -c copy {out_dir / 'ep001_rough_cut.mp4'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
