#!/usr/bin/env python3
"""Run deterministic tests for the short-drama-agent skill.

These tests validate that each prompt in test-prompts.json is supported by
concrete skill instructions, local paths, schemas, and dry-run generation
commands. They do not call paid image/video APIs.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Callable


SKILL_DIR = Path(__file__).resolve().parents[1]


def find_project_root() -> Path | None:
    cwd = Path.cwd().resolve()
    if (cwd / "episodes").exists() and (cwd / "scripts").exists():
        return cwd
    for candidate in [SKILL_DIR, *SKILL_DIR.parents]:
        if (candidate / "episodes").exists() and (candidate / "scripts").exists():
            return candidate
    return None


PROJECT_ROOT = find_project_root()
DATA_ROOT = PROJECT_ROOT or SKILL_DIR / "tests" / "fixtures"
COMMAND_ROOT = PROJECT_ROOT or SKILL_DIR


class TestFailure(AssertionError):
    pass


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TestFailure(message)


def require_all(text: str, needles: list[str], label: str) -> None:
    missing = [needle for needle in needles if needle not in text]
    require(not missing, f"{label} missing: {missing}")


def run_cmd(args: list[str], cwd: Path = COMMAND_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def load_skill_texts() -> dict[str, str]:
    return {
        "skill": read(SKILL_DIR / "SKILL.md"),
        "contract": read(SKILL_DIR / "references" / "production-plan-contract.md"),
        "pipeline": read(SKILL_DIR / "references" / "asset-to-video-pipeline.md"),
        "tagged": read(SKILL_DIR / "references" / "tagged-storyboard-format.md"),
    }


def test_happy_path_ep001(texts: dict[str, str]) -> list[str]:
    require((DATA_ROOT / "episodes" / "ep001.md").exists(), "episodes/ep001.md missing")
    require((DATA_ROOT / "characters.md").exists(), "characters.md missing")
    require_all(
        texts["skill"],
        [
            "video/epNN/ai-production-plan.md",
            "asset-manifest.json",
            "image-generation-tasks.json",
            "video-shot-tasks.json",
            "seedance-prompts.json",
        ],
        "SKILL.md happy-path outputs",
    )
    require_all(
        texts["contract"],
        ["### 5A. 资产抽取总表", "### 5B. 资产生成队列与模型调用计划", "### 16A. 视频模型逐镜生成清单", "依赖资产ID"],
        "production contract",
    )
    return ["ep001 source present", "asset/video output contract present"]


def test_pasted_script_with_ui(texts: dict[str, str]) -> list[str]:
    combined = "\n".join(texts.values())
    require_all(
        combined,
        [
            "UI 留白图",
            "ui_plate",
            "视频中只保留屏幕留白，文字后期叠加",
            "Do not let AI video generate complex Chinese text",
            "post-production text overlays",
        ],
        "UI/post-overlay rules",
    )
    return ["UI text routed to post overlays", "blank UI plates required"]


def test_revise_existing_seedance(texts: dict[str, str]) -> list[str]:
    manifest = DATA_ROOT / "video" / "ep001" / "seedance-prompts.json"
    require(manifest.exists(), "video/ep001/seedance-prompts.json missing")
    require_all(
        texts["skill"],
        ["contradict the script", "prioritize the script", "mark affected shots for regeneration"],
        "revision conflict rules",
    )
    with tempfile.TemporaryDirectory(prefix="short-drama-agent-seedance-") as tmp:
        result = run_cmd(
            [
                "python3",
                "scripts/seedance_generate.py",
                "--manifest",
                str(manifest),
                "--out-dir",
                tmp,
                "--dry-run",
                "--limit",
                "1",
            ]
        )
        require(result.returncode == 0, f"seedance dry-run failed: {result.stderr or result.stdout}")
        require((Path(tmp) / "payloads").exists(), "seedance dry-run did not write payloads/")
    return ["existing Seedance manifest dry-runs", "revision conflict rules present"]


def test_asset_to_video_execution(texts: dict[str, str]) -> list[str]:
    require_all(
        texts["pipeline"],
        [
            "Script analysis.",
            "Asset extraction.",
            "Image generation or dry-run payload generation.",
            "Asset review and approval.",
            "Continuity-first shot language.",
            "One-shot video test.",
            "Small-batch video generation.",
            "Do not skip from script analysis directly to video generation.",
        ],
        "asset-to-video pipeline order",
    )
    require_all(
        "\n".join(texts.values()),
        ["🔴 CHECKPOINT: paid generation", "🔴 CHECKPOINT: asset approval", "blocked_by_missing_asset"],
        "generation checkpoints",
    )
    with tempfile.TemporaryDirectory(prefix="short-drama-agent-seedream-") as tmp:
        tmp_path = Path(tmp)
        manifest = tmp_path / "image-generation-tasks.json"
        manifest.write_text(
            json.dumps(
                {
                    "defaults": {"model": "test-model", "size": "9:16"},
                    "tasks": [
                        {
                            "task_id": "img_test_ui_plate",
                            "asset_id": "ui_phone_blank",
                            "prompt": "blank phone screen plate, no readable text",
                            "output_path": str(tmp_path / "ui_phone_blank.png"),
                        }
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = run_cmd(["python3", "scripts/seedream_generate.py", "--manifest", str(manifest), "--dry-run"])
        require(result.returncode == 0, f"seedream dry-run failed: {result.stderr or result.stdout}")
        require((tmp_path / "payloads" / "img_test_ui_plate.json").exists(), "seedream dry-run did not write payload")
    return ["asset pipeline order enforced", "Seedream dry-run payload writes"]


def test_professional_placeholder_resolution(texts: dict[str, str]) -> list[str]:
    combined = "\n".join(texts.values())
    require_all(
        texts["skill"],
        [
            "professional cinematography prompt language",
            "placeholder",
            "resolve",
            "professional-shot-prompts.md",
            "Do not preserve XML-like tags",
        ],
        "SKILL.md placeholder resolution trigger/output",
    )
    require_all(
        texts["contract"],
        [
            "### 16B. 专业镜头语言与占位符解析",
            "Location Map",
            "Role Map",
            "Prop/Clue Map",
            "此时他没有张嘴",
        ],
        "production contract professional prompt section",
    )
    require_all(
        texts["pipeline"],
        [
            "Professional Placeholder-Resolved Shot Prompt Layer",
            "resolved_professional_prompt",
            "duration_ms",
            "generation_duration",
            "edit_target_duration",
        ],
        "pipeline professional prompt metadata",
    )
    require_all(
        texts["tagged"],
        [
            "The tags in these examples are placeholders",
            "Do not mechanically output XML-like tags",
            "Resolved output should look like professional natural language",
            "在心里想",
            "画面中所有角色全程不说话",
            "POV",
        ],
        "placeholder resolution reference",
    )
    require(
        "Literal placeholder tags remain in final prompts" in combined,
        "reference must reject unresolved literal placeholder tags",
    )
    return ["professional placeholder resolution supported", "inner-thought/no-mouth rules present"]


TESTS: dict[str, Callable[[dict[str, str]], list[str]]] = {
    "happy_path_ep001": test_happy_path_ep001,
    "pasted_script_with_ui": test_pasted_script_with_ui,
    "revise_existing_seedance": test_revise_existing_seedance,
    "asset_to_video_execution": test_asset_to_video_execution,
    "professional_placeholder_resolution": test_professional_placeholder_resolution,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run short-drama-agent deterministic tests.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    args = parser.parse_args()

    prompts = json.loads((SKILL_DIR / "test-prompts.json").read_text(encoding="utf-8"))
    texts = load_skill_texts()
    results = []
    for prompt in prompts:
        test_id = prompt["id"]
        try:
            checks = TESTS[test_id](texts)
            results.append({"id": test_id, "status": "pass", "checks": checks})
        except Exception as exc:  # noqa: BLE001 - test runner reports all failures uniformly.
            results.append({"id": test_id, "status": "fail", "error": str(exc)})

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            if result["status"] == "pass":
                print(f"PASS {result['id']}: {', '.join(result['checks'])}")
            else:
                print(f"FAIL {result['id']}: {result['error']}")

    return 0 if all(result["status"] == "pass" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
