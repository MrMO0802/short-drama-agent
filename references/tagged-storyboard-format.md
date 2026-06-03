# Professional Placeholder Resolution And Shot Language

Use this reference when the user shows a professional short-drama agent example that contains placeholder tags such as `<location>L1</location>`, `<role>R5</role>`, or `<duration-ms>6000</duration-ms>`.

## Core Correction

The tags in these examples are placeholders, not a required final output format. The skill must parse them, map them to concrete assets, and replace them with natural professional shot language.

Do not mechanically output XML-like tags unless the target video interface explicitly requires them. Final prompts should usually say the actual scene, role, duration, camera, lighting, and performance content.

## Placeholder Maps

Before resolving professional prompts, define stable maps:

```text
Location Map
L1 = scene_crime_room_master: 旧城区烂尾楼三层案发房间；门在画面左侧，破窗在右后方，白布尸体和数字7固定在右后方。
L2 = scene_corridor_master: 三层走廊；脚印从左后通向右前消防门。

Role Map
R5 = char_shenyan: 沈砚，二十七八岁，黑色湿短发，深色湿外套，脸色苍白，左手腕旧疤。
R6 = char_xuzhixia: 许知夏，二十九岁，短发，深色便装，持枪动作稳定。

Prop/Clue Map
P1 = prop_knife_floor: 水果刀，已经落在潮湿水泥地上，不在任何人手里。
C1 = clue_number_7: 尸体旁的巨大数字7，只作为画面线索，不让视频模型生成复杂文字。
```

Use these maps to resolve all placeholders into concrete text and asset IDs.

## Input Example Interpretation

Given:

```text
本片段场景设定在: <location>L1</location>,<location>L2</location>。
分镜1<duration-ms>6000</duration-ms>: ... <role>R5</role> ...
```

Interpret it as:

- This segment uses the concrete scenes mapped by `L1` and `L2`.
- Shot 1 has a target duration of 6000 ms.
- `R5` is the concrete character mapped in the Role Map.
- The final prompt should replace the placeholders with the actual scene and role description.

Resolved output should look like professional natural language, for example:

```text
分镜1，目标时长6000毫秒。恐怖电影风格真人写实，摄影作品质感，紧张失控的表演基调，低饱和冷蓝与病态肤色混合，局部硬光制造戏剧性阴影。荷兰角，极端近景，机位贴近旧城区烂尾楼三层案发房间的潮湿水泥地，拍摄沈砚猛地睁开眼；他二十七八岁，黑色湿短发，深色湿外套，脸色苍白，瞳孔充满惊恐与茫然。镜头以轻微手持晃动从眼睛转焦到他的右手掌，掌心沾着湿滑血迹。28mm广角，浅景深，动态模糊，局部硬光扫过手掌。沈砚面部朝上，视线聚焦自己的手掌。沈砚在心里想：“这不是公司机房！”，此时他没有张嘴。
```

Notice that the final prompt does not preserve `<role>R5</role>` or `<location>L1</location>`; it uses the resolved role and location content.

## Required Professional Shot Fields

Every resolved professional shot should include:

- shot number
- target duration in milliseconds and, if different, generation duration
- resolved scene/location
- resolved visible roles or POV owner
- resolved prop and clue state
- visual style family
- palette and lighting
- camera angle
- shot size
- camera height or point of view
- lens/focal length when useful
- motion and focus behavior
- one visible action only
- body position and gaze direction, or empty-frame rule
- inner thought/no-mouth rule when applicable
- post-overlay rule for screen text/UI
- continuity prohibitions for likely failure points

## Duration Rules

Use the placeholder duration as edit intent:

- `duration_ms`: target edit duration in milliseconds
- `edit_target_duration`: target edit duration in seconds
- `generation_duration`: model-accepted duration such as 5 or 6 seconds

If the model requires more time than the edit target, do not add story actions. Fill extra generation time with camera hold, slow push, rack focus, breathing, handheld drift, or light flicker.

## Inner Thought And No-Mouth Rule

When a line is internal monologue, write it as thought or post voiceover:

```text
沈砚在心里想：“……”，此时他没有张嘴。
```

For POV or empty shots:

```text
这是沈砚的主观视点无人空镜；沈砚在心里想：“……”，画面中所有角色全程不说话。
```

## POV Rules

For POV shots, identify the owner and keep the owner out of frame unless there is a mirror/screen/reflection reason:

- `主观视点镜头，来自沈砚的视角`
- `这是无人空镜`
- `镜头只扫过地面、白布尸体和数字7，不出现沈砚的脸`

## Camera Language Library

Do not limit the skill to the user's sample. Choose terms that serve story clarity and continuity:

- Angles: 荷兰角、贴地低机位、过肩镜头、俯拍、仰拍、平视、主观视点、监控视角、镜面反射视角。
- Shot sizes: 极端近景、特写、中近景、中景、全景、远景、插入特写、证物特写。
- Lens: 18mm超广角、24/28mm广角、35mm标准、50mm人像、85mm压缩空间、微距镜头。
- Movement: 手持晃动、缓慢推进、快速甩镜、视线摇移、跟拍、横移、拉焦、呼吸式微动、短促变焦。
- Lighting: 局部硬光、顶灯闪烁、警灯红蓝反射、窗外冷光、低照度、高对比阴影、背光剪影、实景光源。
- Texture: 潮湿水泥、雨水反光、灰尘漂浮、玻璃裂纹、血迹黏腻但不血腥、低饱和颗粒感。
- Performance: 惊醒、强迫冷静、短暂错愕、压低呼吸、瞳孔收缩、手指僵住、视线躲闪、动作克制。

Use these terms only when they control the generated image. Avoid piling up irrelevant cinematography jargon.

## Continuity Rules

Resolved professional prompts must inherit shot-card continuity:

- Same face, hair, costume, injuries, wetness, and emotional state.
- Same location geography and screen direction.
- Same prop state; a weapon on the ground cannot return to a hand without an explicit pickup shot.
- Same clue reveal order; do not reveal later clues early.
- Screen text/UI remains blank for post overlay unless the user explicitly requests otherwise.

## Reject These Outputs

- Literal placeholder tags remain in final prompts when no API requires them.
- A placeholder ID is used without being mapped to concrete scene/role/asset content.
- A shot performs two or more major actions.
- A POV shot randomly shows the POV owner's face.
- Inner thought makes the character move their mouth.
- Professional terms are copied from the sample even when they do not fit the scene.
- Readable Chinese phone/news/UI text is assigned to the video model.
- A prompt adds unmentioned characters, weapons, police, locations, or prop resets.
