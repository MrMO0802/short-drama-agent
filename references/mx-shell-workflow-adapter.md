# Mx-Shell Workflow Adapter

Use this reference when the user mentions Mx-Shell, `ai-shortfilm-prompts`, Zombie Scavenger, Seedance 2.0 immersive shorts, 5-stage cinematic prompts, or asks to polish short-drama video prompts with a professional shortfilm workflow.

## Source Adaptation Rule

Do not copy Mx-Shell source prompts or templates verbatim. Extract the method and adapt it to this skill's continuity-first episode pipeline.

Mx-Shell's workflow is strongest at cinematic prompt control for one short clip. `short-drama-agent` must keep its own higher priority: asset locks, story causality, spatial continuity, prop state, clue reveal order, and one-shot-at-a-time generation.

## Episode-Compatible 5-Stage Layer

For each video-model prompt or resolved professional shot, add a compact 5-stage prompt layer after the continuity shot card:

1. `core_theme_tags`: 3-6 concrete tags that move from format to genre to aesthetic. Avoid vague praise words.
2. `locked_character_scene`: face/hair/costume/state, material, scene geography, active environment, and current prop/clue state.
3. `atmosphere_quality`: real camera and lens profile, color palette, lighting, film grain or physical texture.
4. `camera_rules`: shot type, shot size, angle, movement, screen direction, and subtle camera float when handheld.
5. `storyboard_slice`: one action only, written as either per-second beat or per-shot beat with action, camera, sound, and optional VFX.

This 5-stage layer is not a replacement for the 21-section production plan. It is the final copy-ready video prompt polish layer.

## Concrete Visual Anchors

Every copy-ready video prompt should include:

- `camera_lens_profile`: a real or real-sounding production anchor such as IMAX film camera + Panavision C-series 35mm f/4, Sony Venice + Canon K-35, Kodak 35mm bleach-bypass, or Canon EF 85mm f/1.2 for portrait/reference images.
- `palette_lighting`: low-saturation grey-blue, low-light high-contrast, teal-orange contrast, warm practical light, side light, rim light, volume fog, or other concrete light behavior.
- `physical_texture`: wet concrete, worn metal, oil in joints, fabric dust, skin blemishes, cracked glass, film grain, light haze, imperfect reflections.
- `imperfection_anchors`: at least two imperfections for character, costume, prop, environment, or equipment when realism matters.

Do not rely on words like cinematic, epic, premium, stunning, high quality, 4K, perfect, cool, or advanced unless they are paired with physical camera, lighting, material, or motion details.

## Camera Float Rule

When a shot is handheld or subjective, include a controlled subtle float:

```text
手持拍摄，全程保持极其轻微的、如呼吸般的镜头浮动，增强临场感；不要变成剧烈晃动。
```

Use heavier shake only when the script explicitly requires panic, impact, running, or loss of control. For locked-off surveillance, evidence inserts, or precise clue shots, use a fixed camera instead.

## Sound Rule

Every copy-ready video prompt should include a sound policy:

```text
Sound: No score. Production audio only.
```

Then enumerate scene-specific sounds when useful: breath, footsteps, cloth friction, glass crack, rain, distant siren, phone vibration, fluorescent buzz, metal scrape, low-frequency hum, door hinge, or crowd murmur.

If the shot contains inner monologue, treat it as thought or post voiceover and state that the character does not open their mouth.

## Per-Second Vs Per-Shot

Use per-second slices for one-take transformations, weapon charging, energy build-up, or a single continuous action:

```text
0-2s · 发现
Action: ...
Camera: ...
Sound: ...
VFX: ...
```

Use per-shot slices for edited narrative shorts and short-drama episodes:

```text
Shot 1:
Shot size:
Composition:
Camera move:
Action:
Sound:
End state:
```

For short-drama continuity, the per-shot style is the default. Per-second slices can be embedded inside a single 5-8 second generation item only when the model requires a longer clip than the edit target and no extra story action is added.

## Composition Rules

Describe foreground, middle ground, background, screen direction, and entry/exit paths when the shot depends on spatial clarity.

Prefer:

- foreground / middle ground / background layers
- left-to-right or right-to-left movement continuity
- over-shoulder relation for confrontation
- empty frame plus offscreen sound for unseen threat
- expression change as a valid shot endpoint

Reject composition that says only "beautiful frame" or "movie composition" without layer, subject, and direction.

## Reference Image Rule

Use reference images when continuity requires identity, costume, scene geography, prop shape, or clue placement.

Avoid low-quality or stylized reference images for invented armor, monsters, machinery, or heavy VFX if the reference would contaminate the output style. In those cases, describe design, material, scratches, damage, scale, and three-view needs in text or generate a higher-quality reference asset first.

## Restrained Ending Rule

Do not end a shot by piling on explosions, blinding light, victory poses, or new plot actions unless the script requires them.

Default ending strategy:

- hold on the changed state
- let environment sound continue
- keep a damaged, incomplete, or uneasy detail visible
- cut on gaze, sound, prop state, or unresolved threat

This supports editability and avoids AI overacting.

## IP And Filter Rule

Avoid IP names, brand names, character names, and direct copyrighted style labels in final video-model prompts when using models with strict filters such as Seedance.

Replace direct IP labels with design language:

- superhero armor -> retro-futurist red-and-gold combat suit
- famous dance style -> 1980s beat-synced shoulder rolls and backward glide
- named film look -> gritty dark battle-damaged practical-effects aesthetic

If the user explicitly requires an IP name, keep it only if necessary and add a model filter warning in the post notes.

## Quality Self-Check

Before accepting a prompt, check:

1. Does it preserve the shot card's start state, one action, end state, and next connection?
2. Does it include `core_theme_tags` or an equivalent concrete style line?
3. Does it include `camera_lens_profile`?
4. Does it include controlled camera float or an explicit fixed-camera reason?
5. Does it include `Sound: No score. Production audio only.` or a deliberate sound bridge policy?
6. Does it include at least two realism imperfections when faces, costumes, props, or environments matter?
7. Does it avoid vague praise words that cannot form a concrete image?
8. Does it avoid IP/filter-risk terms or flag them?
9. Does the ending hold a state instead of adding extra action?
10. Does movement direction match the previous and next shots?

If any item fails, rewrite the prompt before dry-run or paid generation.
