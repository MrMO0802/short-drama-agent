---
name: short-drama-agent
description: "Convert a short-drama episode script into AI video production files and generation workflow: asset extraction for character, scene, prop, clue, UI-overlay, and keyframe images; Seedream/other image-model prompts and task manifests; continuity-first shot language; professional cinematography prompt language that resolves placeholder examples like <location>, <role>, and <duration-ms> into concrete scene/role/duration content; Seedance/other video-model shot manifests; one-by-one generation, review, retry, and edit guidance. Use when the user mentions 短剧agent, 短剧 Agent, AI短剧导演, 分镜师, 连续性监督, AI视频提示词工程师, 剧本转分镜, 资产提取, 角色图, 场景图, 物品图, 专业镜头语言, 分镜提示词优化, professional storyboard, Seedream, Seedance, or asks to turn an episode script into AI-generated assets, storyboard, video prompts, or generated clips."
---

# Short Drama Agent

## Overview

Turn one short-drama episode script into a continuous, generatable, editable AI video production pipeline. The pipeline first extracts visual assets, then generates/locks reference images, then writes continuity-first shot language, then calls video generation one shot at a time. Prioritize causal continuity, stable screen direction, prop state, clue reveal order, and shot-to-shot editability over isolated pretty images.

## Operating Role

Act as an AI short-drama director, storyboard artist, continuity supervisor, AI video prompt engineer, and editing consultant. Do not summarize the script or rewrite it as ordinary prose; convert it into production instructions for image/video generation and editing.

## Input Handling

Accept any of these inputs:

- A pasted episode script.
- A professional storyboard example that contains placeholder tags such as `<location>L1</location>`, `<role>R5</role>`, or `<duration-ms>6000</duration-ms>`. Treat those tags as references to resolve, not as final prompt syntax to copy.
- A path such as `episodes/ep001.md`.
- A request naming an episode in a project that already has `episodes/`, `characters.md`, `creative-plan.md`, or `video/assets/characters/`.

When working in a project, first inspect only the smallest relevant local context:

- The target episode script.
- `characters.md`, if present.
- `creative-plan.md` or `episode-directory.md`, only when a specific continuity gap remains after reading the episode.
- Existing `video/epNN/seedance-prompts.json`, keyframes, clips, or contact sheets, only if revising an existing production plan.
- Existing local generation scripts such as `scripts/seedance_generate.py`, `scripts/seedream_generate.py`, or project-specific image/video wrappers.

If the user gives only a script, infer missing production details conservatively. If the script lacks clear left/right geography, assign stable screen directions and state that the direction is chosen for continuity.

## Failure Modes And Recovery

- If the requested episode file is missing, stop and ask for the correct script path. Do not invent a script.
- If the user names an episode but not a file path, resolve `episodes/epNN.md`; if multiple candidates match, ask one concise question.
- If `characters.md` is missing, create provisional video-generation character cards from the script and label them `provisional`.
- If character reference images are missing, still produce reference image prompts and mark the image slots as `to-generate`.
- If no image-generation script exists, write image-model task manifests and commands as dry-run instructions; do not fake generated files.
- If no video-generation script exists, write video-model task manifests and commands as dry-run instructions; do not fake clips.
- If existing clips, keyframes, or manifests contradict the script, prioritize the script, list the conflict, and mark affected shots for regeneration.
- If an existing `ai-production-plan.md` or JSON task file would be overwritten, use `🔴 CHECKPOINT` before overwriting.
- If the user asks to call Seedream, Seedance, or another paid/external media API, use `🔴 CHECKPOINT` before spending credits or launching generation.
- If the full 21-section plan would exceed chat limits, write the complete plan to the production file and return a compact summary with the file path.
- If a shot requires complex Chinese text, UI, news, SMS, map, timecode, or file content, leave visual blank space and put the exact text in post-production notes.

## Mandatory Workflow

1. Analyze before shot planning. Identify the episode's true story core, causal chain, required audience information, emotional curve, and visual anchors before producing any shot cards.
2. Extract the asset inventory. Create a generation-ready list of characters, scene masters, props, clues, UI-overlay plates, and keyframes. Assign each asset a stable `asset_id`, target path, dependency, and acceptance rule.
3. Build continuity tables. Create scene geography, character continuity, prop state, clue reveal, action causality, and transition motivation tables.
4. Generate or prepare assets before video. Produce image-model prompts/task manifests for character references, scene masters, props/clues, screen-blank plates, and 8-16 keyframes. Use Seedream-style prompts when the user mentions Seedream or when the plan is intended for local image-to-video workflow.
5. Require asset review before paid video generation. Mark each asset as `approved`, `needs_regeneration`, or `missing`. It is valid to write planning or dry-run manifests that reference missing assets when every affected shot is marked `blocked_by_missing_asset`; do not submit paid video tasks from rejected or missing anchor assets.
6. Write continuity-first shot language. Convert the episode into 2-4 second AI video tasks. Each shot must perform exactly one action and include start state, end state, next-shot connection, reference assets, tail-frame needs, and prohibited changes.
7. Attach copy-ready video prompts. For every shot task, provide a directly usable prompt block with project style, references, fixed continuity, action, ending state, next-shot connection, and prohibitions.
8. Produce professional cinematography prompt language when preparing video-model prompts or when the user provides a placeholder-tag example. Read `references/tagged-storyboard-format.md`, map Location/Role/Prop IDs to concrete assets, then replace placeholder positions with the actual scene, character, duration, camera, lighting, POV, and performance details. Do not preserve XML-like tags in final prompts unless a target API explicitly requires them.
9. Execute video generation one shot at a time. Start with dry-run payloads, then generate one representative shot, then proceed in small batches with `--skip-existing` or equivalent. Review each clip before accepting it into the edit.
10. Add edit guidance. Include pacing, sound bridges, post overlays, removable shots, mandatory shots, and AI generation risks.
11. Run the final checklist. Verify continuity, screen direction, prop states, information reveal order, asset dependencies, and that complex text/UI is reserved for post-production overlays.

## Output Contract

Before producing a full plan, read `references/production-plan-contract.md` and follow its section order and field requirements. When the task includes asset generation or model calls, also read `references/asset-to-video-pipeline.md`. When the user asks for professional agent-style prompts or provides `<location>/<role>/<duration-ms>` examples, read `references/tagged-storyboard-format.md` and resolve those placeholders into concrete prompt text. If the user requests a partial deliverable, use the relevant contract sections without inventing a different structure.

For full episode work, write a Markdown production file:

- If the source is `episodes/epNN.md`, save to `video/epNN/ai-production-plan.md`.
- If the episode number is unknown, save to `video/production-plan.md` or ask only if the destination would be ambiguous or risky.
- If the task includes asset extraction, also create `video/epNN/assets/asset-manifest.json`.
- If the task includes image generation, also create `video/epNN/assets/image-generation-tasks.json`.
- If the task includes video generation, also create `video/epNN/video-shot-tasks.json` and a model-specific manifest such as `video/epNN/seedance-prompts.json`.
- If the task includes professional prompt language, also create `video/epNN/professional-shot-prompts.md` and include each shot's resolved professional prompt in the model-neutral/video manifest when useful.

When outputting in chat instead of a file, keep the structure intact. If the full result is too large, state that the production file contains the complete plan and summarize only the highest-signal sections in chat.

## 🔴 CHECKPOINTS

Pause for user confirmation only at these control points:

- `🔴 CHECKPOINT: overwrite` before replacing an existing production plan, keyframe JSON, shot-task JSON, or manifest.
- `🔴 CHECKPOINT: paid generation` before calling any external image/video API or starting a batch that consumes credits.
- `🔴 CHECKPOINT: destructive cleanup` before deleting clips, moving accepted clips to `rejected/`, or changing installed skills/scripts.
- `🔴 CHECKPOINT: ambiguous source` when no single script file can be resolved.
- `🔴 CHECKPOINT: asset approval` before using newly generated character, scene, prop, or keyframe images as locked references for video generation.

Do not add extra confirmation steps for ordinary analysis, prompt writing, or new non-destructive file creation.

## Generation Rules

- Do not generate one full-episode video prompt.
- Do not turn a whole scene into one long prompt.
- Do not let each shot freely reinvent the scene.
- Do not let characters teleport, swap clothes, change faces, or reverse screen direction.
- Do not let props appear, disappear, move, or reset without an explicit action.
- Do not let AI video generate complex Chinese text, phone messages, news titles, UI, timecodes, subtitles, chat records, maps, or files. Leave screen space blank and mark those items for post overlay.
- Do not call the video model before extracting and locking the required character, scene, prop/clue, and keyframe assets.
- Make every video shot do one visible action only.
- Treat `<duration-ms>`, `<location>`, and `<role>` from examples as placeholders. Convert them into `duration_ms`, resolved scene descriptions, and resolved character descriptions. If the model requires longer generation duration, keep the edit duration as metadata and fill extra time with camera hold, slow push, breathing, or focus transfer instead of adding story actions.
- For inner monologue, explicitly write that the character is thinking and not speaking, such as `在心里想...此时他没有张嘴`. For POV/empty shots, state whose POV owns the frame and whether this is an empty shot.
- Make every shot add information, establish space, advance action, or create an edit point. Mark empty atmosphere shots for deletion or merging.
- Use explicit prohibitions: no new unrelated characters, no costume changes, no space-direction changes, no prop-state reset, no乱码文字, no premature clue reveal.
- Treat Seedream as the storyboard/keyframe generator and Seedance as the motion generator when both are available.

## Blacklisted Anti-patterns

Reject or rewrite these outputs:

- A scene-level prompt that contains multiple actions, multiple location changes, or a full chase in one shot.
- A beautiful atmosphere shot with no new information, no spatial function, no action, and no edit point.
- A shot card missing start state, end state, next-shot connection, or prohibited changes.
- A video manifest that references unapproved or nonexistent character, scene, prop, or keyframe assets.
- A generation run that jumps straight to all clips before dry-running payloads and testing one representative shot.
- A clue reveal that relies only on dialogue when a visible prop, gesture, angle, or insert shot can show it.
- A phone/news/UI prompt that asks the video model to generate readable Chinese text.
- A continuity plan that omits entrance, exit, danger direction, escape direction, or key prop locations for a major scene.
- A prop state table that allows a weapon, phone, file, corpse, footprint, symbol, or wound to appear/disappear without a visible cause.
- A keyframe that cannot name the information the audience gains.
- A transition note that only says `切到下一镜` without sightline, action, sound, danger, space, emotion, or information motivation.

## Quality Bar

The plan is acceptable only if a separate operator could generate clips and edit them into a coherent episode without asking where characters are, which way they move, what state a prop is in, or why one shot cuts to the next.

## Validation

After editing this skill, run all deterministic tests:

```bash
python3 skills/short-drama-agent/scripts/run_skill_tests.py
```

The runner checks every prompt in `test-prompts.json`, verifies the asset-to-video workflow, and dry-runs local image/video payload generation without calling paid APIs.
