# Asset To Video Pipeline

Use this reference when the user wants the skill to extract assets, generate images, or call video models.

## Required Pipeline Order

Run the production chain in this order:

1. Script analysis.
2. Asset extraction.
3. Asset image prompts and task manifests.
4. Image generation or dry-run payload generation.
5. Asset review and approval.
6. Continuity-first shot language.
7. Professional placeholder-resolved shot prompt layer when useful.
8. Video-model manifest generation.
9. One-shot video test.
10. Small-batch video generation.
11. Clip review, retry, rough cut, and post-overlay list.

Do not skip from script analysis directly to video generation.

## Asset Manifest

Create `video/epNN/assets/asset-manifest.json` when a script file resolves to an episode number.

Use this shape:

```json
{
  "episode": 1,
  "title": "episode title",
  "style_bible": {
    "visual_style": "",
    "palette": "",
    "lighting": "",
    "camera_language": "",
    "negative_prompt": ""
  },
  "assets": [
    {
      "asset_id": "char_shenyan_front",
      "type": "character",
      "name": "沈砚",
      "purpose": "front reference for face and costume continuity",
      "first_needed_by": "kf003",
      "dependencies": [],
      "target_path": "video/ep001/assets/characters/char_shenyan_front.png",
      "prompt": "",
      "negative_prompt": "",
      "acceptance_criteria": [
        "same age impression",
        "same hairstyle",
        "same costume",
        "clear face",
        "no unrelated props"
      ],
      "status": "to-generate"
    }
  ]
}
```

Required `type` values:

- `character`: face, hair, costume, body state, scars, wounds, dirt, wetness.
- `scene`: master geography, entrance, exit, danger direction, escape direction, fixed prop positions.
- `prop`: weapon, phone, key, letter, file, medicine, vehicle, corpse cover, footprint, symbol.
- `clue`: visible evidence that the audience must notice.
- `ui_plate`: blank phone/computer/news/surveillance/map screen prepared for post overlay.
- `keyframe`: story frame that locks character positions, prop state, and shot continuity.

## Image Generation Tasks

Create `video/epNN/assets/image-generation-tasks.json` after the asset manifest.

Use this shape:

```json
{
  "defaults": {
    "model": "image-model-name",
    "size": "9:16",
    "quality": "2K",
    "style_lock": "series style line"
  },
  "tasks": [
    {
      "task_id": "img_ep001_char_shenyan_front",
      "asset_id": "char_shenyan_front",
      "output_path": "video/ep001/assets/characters/char_shenyan_front.png",
      "prompt": "",
      "negative_prompt": "",
      "reference_images": [],
      "post_overlay_required": false
    }
  ]
}
```

If the project has a local image-generation script, use it after `🔴 CHECKPOINT: paid generation`. If no script exists, produce the manifest and exact dry-run command the user can run after adding a model wrapper.

## Asset Generation Order

Generate assets in this order:

1. Style bible plate or mood reference.
2. Character references: front, half-body, full-body, special state variants.
3. Scene master images.
4. Prop and clue close-ups.
5. UI blank plates for phone/news/computer/surveillance.
6. Keyframes using approved character, scene, prop, and clue references.

Do not generate keyframes before the required character and scene references exist.

## Asset Approval Gate

Before video generation, produce an asset review table:

- asset_id
- target_path
- approval_status: `approved`, `needs_regeneration`, `missing`
- issue
- regeneration_prompt_delta

Use `🔴 CHECKPOINT: asset approval` before locking generated images into paid video tasks. Planning and dry-run manifests can reference missing assets only when affected shots are marked `blocked_by_missing_asset`.

## Continuity-first Shot Language

Write video prompts from state, not from mood. Each shot prompt must include:

- Locked references: character image, scene master, prop/clue image, previous tail frame.
- Previous end state.
- Current start state.
- Single visible action.
- Current end state.
- Next cut motivation.
- Prohibited changes.

Every shot must name the exact asset IDs it depends on.

## Professional Placeholder-Resolved Shot Prompt Layer

When prompts will be copied into a professional video-agent interface, or when the user provides examples with `<location>`, `<role>`, or `<duration-ms>` placeholders, create `video/epNN/professional-shot-prompts.md` after the shot cards and before paid video generation.

The professional prompt layer must:

- define Location/Role/Prop/Clue placeholder maps before shots
- parse placeholder tags from examples, then replace them with concrete scene, role, asset, and duration content
- avoid literal XML-like tags in final prompts unless a target API explicitly requires that syntax
- preserve the shot card's single action, start/end state, prop state, and next-cut motive
- include concrete camera language: angle, shot size, camera height or POV, lens, movement, focus, lighting, palette
- mark inner monologue as thought/post voiceover and explicitly say the role does not open their mouth
- treat phone/news/UI/surveillance/file/map text as post overlay with blank screen space

Use `duration_ms` for edit intent. If the video API requires a longer duration, put that value in `generation_duration` or the model-specific manifest's `duration`, and keep `edit_target_duration` for trimming. Fill extra generated time with camera hold, slow push, rack focus, breathing, or handheld drift rather than adding new story action.

## Video Manifest

Create `video/epNN/video-shot-tasks.json` as the model-neutral shot list. Create `video/epNN/seedance-prompts.json` or another model-specific dry-run manifest when the user needs payload validation before assets are approved.

For model-neutral tasks, include:

```json
{
  "shot_id": "ep001_s001",
  "duration": 3,
  "duration_ms": 3000,
  "generation_duration": 5,
  "depends_on_assets": [
    "scene_unfinished_building_room",
    "prop_knife_floor",
    "clue_number_7_wall"
  ],
  "previous_tail_frame": null,
  "start_state": "",
  "single_action": "",
  "end_state": "",
  "next_connection": "",
  "video_prompt": "",
  "resolved_professional_prompt": "分镜1，目标时长3000毫秒。旧城区烂尾楼三层案发房间内，沈砚猛地睁开眼...",
  "negative_prompt": "",
  "acceptance_criteria": [],
  "status": "ready"
}
```

For Seedance-style manifests, preserve compatibility with the local `scripts/seedance_generate.py` shape: `episode`, `title`, `out_dir`, `defaults`, `series_style`, `episode_style`, `negative_prompt`, and `shots`. A shot may also include `edit_target_duration`, `duration_ms`, `generation_duration`, and `resolved_professional_prompt`; the local script will ignore unknown keys but they remain useful for review and trimming. When assets are not yet generated, omit `image_path`, keep asset IDs in the text prompt, and mark the corresponding model-neutral shot status as `blocked_by_missing_asset`.

## One-by-one Video Generation

Use this execution sequence when scripts exist:

1. Write dry-run payloads.
2. Generate one representative shot with locked references.
3. Review the clip and preview frame.
4. If accepted, generate the next 3-5 shots.
5. Move failed clips to `rejected/` only after `🔴 CHECKPOINT: destructive cleanup`.
6. Rewrite only failed shot prompts; keep approved shots unchanged.
7. Continue in small batches until all clips are accepted.
8. Build `concat.txt` and rough cut.

For this project, the existing Seedance command pattern is:

```bash
python3 scripts/seedance_generate.py --manifest video/ep001/seedance-prompts.json --dry-run
python3 scripts/seedance_generate.py --manifest video/ep001/seedance-prompts.json --limit 1
python3 scripts/seedance_generate.py --manifest video/ep001/seedance-prompts.json --shots 2-5 --skip-existing
```

Do not print API keys. Do not write API keys into manifests.

## Retry Rules

Regenerate an image asset when:

- The face, age, costume, scar, or body state differs from the character card.
- The scene direction flips.
- A required entrance, exit, prop, or clue is missing.
- A UI plate contains unreadable generated text instead of blank screen space.

Regenerate a video shot when:

- The shot performs more than one major action.
- The character starts from the wrong position or emotional state.
- A prop state goes backward.
- The camera crosses the established action axis without motivation.
- The shot cannot cut from the previous shot or into the next shot.
- Complex text appears inside the video model output.
- A professional prompt leaves unresolved `<location>`, `<role>`, `<duration-ms>`, prop, or clue placeholders in final model text.
- A POV shot shows the POV owner's face without a mirror/screen/reflection reason.
- Inner monologue makes the character move their mouth when the script says they are only thinking.
