# AI Video Production Plan Contract

Use this contract for full short-drama episode conversion. Keep the section order fixed.

## Core Rule

The output must serve one goal: make the episode generatable, editable, and continuous. Every shot must have causality, space, action, information, and connection.

Do not output empty style words such as "cinematic", "高级", "紧张", or "悬疑感" unless paired with concrete visual instructions.

## Section Order

### 1. 本集一句话故事核心

Write one sentence explaining what the episode is truly about. Do not merely retell the plot.

### 2. 本集主线链条

Write a causal/lead chain:

`事件 A -> 角色发现 B -> 导致 C -> 暴露 D -> 进入 E -> 形成结尾钩子`

Each step must explain how the previous event causes the next. Avoid pure emotion labels.

### 3. 本集观众必须看懂的信息

List the information the audience must understand, such as:

- Where the protagonist is.
- Why the protagonist is in danger.
- Who misunderstands or threatens the protagonist.
- What the key evidence is.
- What abnormal detail the protagonist discovers.
- What suspense remains at the end.

### 4. 本集情绪曲线

Write the protagonist's emotional progression in story order, such as:

`迷茫 -> 恐惧 -> 强迫冷静 -> 发现异常 -> 被误解 -> 逃避危险 -> 确认真相 -> 被逼入绝境 -> 进入主动思考`

### 5. 本集视觉锚点

List the visual anchors that must remain consistent across the episode:

- Rooms, doors, windows, corridors, staircases, vehicles.
- Corpses, weapons, phones, scars, symbols, colors, light sources.
- Screen directions, entrances, exits, danger direction, escape direction.

These anchors must later appear in the space table, prop table, and prohibited-change rules.

### 5A. 资产抽取总表

Before writing image prompts or video shots, extract every visual asset required to generate the episode.

Group assets by:

- 角色图: front face, half-body, full-body, special state variants such as wet clothes, injury, disguise, age flashback.
- 场景图: master geography for each major scene, including entrance, exit, danger direction, escape direction, and fixed prop locations.
- 物品图: weapons, phones, keys, letters, files, medicine, vehicles, corpse covers, footprints, symbols, photos.
- 线索图: evidence that the audience must notice in a specific order.
- UI 留白图: phone, news, SMS, surveillance, chat, map, computer, file, timecode plates for post overlay.
- 关键帧图: 8-16 story frames that lock character positions, prop state, scene direction, and clue visibility.

For each asset, include:

- asset_id
- asset_type
- asset_name
- first_needed_by
- depends_on
- target_path
- purpose
- must_keep_consistent
- acceptance_criteria
- status: `existing`, `to-generate`, `approved`, `needs_regeneration`, or `missing`

### 5B. 资产生成队列与模型调用计划

Create an image-generation queue before video-generation tasks.

For each image task, include:

- task_id
- asset_id
- model_family: Seedream or other image model
- output_path
- prompt
- negative_prompt
- reference_images
- required_blank_space_for_post
- acceptance_criteria
- retry_rule

Generation order:

1. Style bible or mood plate.
2. Character references.
3. Scene master images.
4. Prop and clue close-ups.
5. UI blank plates.
6. Keyframes from approved references.

Add `🔴 CHECKPOINT: paid generation` before calling image APIs and `🔴 CHECKPOINT: asset approval` before using generated assets for paid video tasks. Planning and dry-run manifests can reference missing assets only when affected video items are marked `blocked_by_missing_asset`.

### 6. 场景空间表

For each major scene, include:

- 场景名称
- 时间
- 地点
- 整体氛围
- 主要入口
- 主要出口
- 画面左侧有什么
- 画面右侧有什么
- 画面中后方有什么
- 画面前景可以有什么
- 角色通常从哪里进入
- 角色通常往哪里移动
- 危险来自哪个方向
- 逃生方向在哪里
- 关键道具固定在哪里
- 推荐动作轴线
- 禁止改变的空间关系

If the script does not define left/right direction, assign stable screen direction and explicitly state it was chosen to preserve continuity.

### 7. 角色连续性表

For each major role, include:

- 角色姓名
- 身份
- 年龄或年龄感
- 外貌关键词
- 发型
- 服装
- 身体特征
- 当前状态
- 本集目标
- 本集误会或冲突
- 情绪变化
- 动作习惯
- 与其他角色的空间关系
- 与关键道具的关系
- 禁止变化

This is not a general character bio. It is a video-generation continuity card.

### 8. 道具状态表

Extract important props and clues. Include weapons, phones, keys, wounds, blood traces, files, photos, surveillance screens, corpses, vehicles, doors, windows, footprints, medicine, letters, symbols, and screen text.

For each item, include:

- 道具名称
- 第一次出现在哪个场景
- 第一次出现时的位置
- 第一次出现时的状态
- 后续状态如何变化
- 谁接触过它
- 它对剧情有什么作用
- 它什么时候不能再出现
- 它什么时候必须出现
- 禁止错误

Prop state must behave like a timeline. If a knife falls to the ground, it cannot return to a character's hand unless a shot shows that character picking it up.

### 9. 线索 / 信息揭示表

For each clue, include:

- 线索名称
- 观众第一次看到它的镜头
- 角色什么时候注意到它
- 它说明什么
- 它是否会误导观众
- 它后面如何被验证
- 它和结尾钩子有什么关系
- 推荐用什么镜头表现
- 禁止提前暴露什么

Make clues visible through shots, not only explained by dialogue.

### 10. 动作因果表

Break the episode into action-causality units:

- 动作 N
- 角色做了什么
- 为什么做
- 造成什么结果
- 下一步被什么触发

If an action does not advance plot, reveal information, change danger, establish space, or alter emotion, mark it as deletable or mergeable.

### 11. 镜头转场动机表

For important cuts, explain why the cut happens. Use specific transition motives:

- 视线转场
- 动作转场
- 声音转场
- 道具转场
- 情绪转场
- 信息转场
- 空间转场
- 危险转场

Never write only "切到下一镜". Explain the edit reason.

### 12. 角色参考图提示词

For each major role, include:

- 角色姓名
- 用途
- 图像提示词
- 禁止项

Prompts must include age impression, facial features, hairstyle, clothing, temperament, current state, style, lighting, half/full body, clear face, and low-distraction background.

Prohibitions must include no age change, no costume change, no exaggerated expression, no unrelated props, and no identity/temperament change.

### 13. 场景母版图提示词

For each major scene, include:

- 场景名称
- 用途
- 空间方向
- 关键物体位置
- 图像提示词
- 禁止项

Scene master images lock geography. They are not beauty shots. Always specify entrance, exit, key props, usual character entry direction, and movement direction.

### 14. 关键道具 / 线索参考图提示词

For important props/clues, include:

- 道具或线索名称
- 外观
- 状态
- 位置
- 材质
- 使用方式
- 是否需要留白给后期
- 图像提示词
- 禁止变化

For phones, news, UI, files, maps, and surveillance footage, reserve clean blank areas for post-production text overlays.

### 15. 8-16 张关键帧提示词

Design 8-16 keyframes before video generation. They must cover:

1. 开场钩子画面
2. 主角第一次出现
3. 核心危险或冲突
4. 关键空间全景
5. 重要对峙关系
6. 第一条关键线索
7. 第二条关键线索
8. 主角做出关键选择
9. 身份或情绪反转
10. 结尾钩子

For each keyframe, include:

- 关键帧编号
- 对应剧情
- 所属场景
- 画面内容
- 景别
- 角色位置
- 道具位置
- 观众应获得的信息
- 后续会扩展成哪些视频镜头
- 图像生成提示词
- 禁止变化

If a keyframe cannot explain what information the audience gains, mark it unnecessary.

### 16. 视频镜头任务卡

Split the episode into 2-4 second AI video tasks. Each shot must happen as one visible action.

For each shot, include:

- 镜头编号
- 时长
- 所属段落
- 所属场景
- 使用参考图
- 依赖资产ID
- 是否需要上一镜尾帧
- 上一镜结束状态
- 本镜头开始状态
- 景别
- 镜头运动
- 人物位置
- 人物朝向
- 关键道具状态
- 本镜头唯一动作
- 观众获得的新信息
- 本镜头结束状态
- 下一镜如何衔接
- 声音建议
- 后期建议
- 禁止变化

If screen text, SMS, news, subtitles, or UI appears, write: `视频中只保留屏幕留白，文字后期叠加`.

### 16A. 视频模型逐镜生成清单

After writing the shot task cards, produce a model-neutral generation queue.

For each video generation item, include:

- shot_id
- duration
- model_family: Seedance or other video model
- depends_on_assets
- first_frame_asset
- previous_tail_frame
- prompt_source_section
- output_path
- dry_run_payload_path
- acceptance_criteria
- retry_rule
- generation_status: `blocked_by_missing_asset`, `ready`, `dry_run_written`, `submitted`, `accepted`, `needs_regeneration`

Execution order:

1. Write dry-run payloads.
2. Generate one representative shot.
3. Review the shot against acceptance criteria.
4. Generate the next 3-5 shots with `skip existing` behavior.
5. Keep accepted clips unchanged and rewrite only failed shot prompts.

### 16B. 专业镜头语言与占位符解析

After the generation queue, write a professional cinematography prompt layer when video prompts will be copied to a model interface or when the user provides an example with placeholder tags. Read `references/tagged-storyboard-format.md` before writing this section.

First define stable placeholder maps:

- Location Map: `L1`, `L2`, etc. mapped to scene asset IDs and fixed geography.
- Role Map: `R1`, `R2`, etc. mapped to character asset IDs, reference images, and continuity descriptions.
- Prop/Clue Map: `P1`, `C1`, etc. mapped to locked prop and clue assets when needed.

Then write resolved professional prompts. Do not keep literal XML-like tags in final prompts unless a target API explicitly requires them. Replace placeholders with concrete scene, role, duration, camera, lighting, and performance content:

```text
分镜1，目标时长3000毫秒。恐怖电影风格真人写实，低饱和冷蓝色调，局部硬光制造戏剧性阴影。荷兰角，极端近景，机位贴近旧城区烂尾楼三层案发房间的潮湿水泥地，拍摄沈砚猛地睁开眼...
分镜2，目标时长4000毫秒。主观视点镜头，来自沈砚的视角，在同一案发房间内惊恐扫过冰冷混凝土地面...
```

Each resolved professional shot must include:

- target edit duration in milliseconds.
- resolved locked scene reference, not a bare `L1` tag.
- resolved visible roles or POV-owning roles, not a bare `R5` tag.
- style family, palette, lighting, camera angle, shot size, camera height or POV, lens/focal length, motion, focus behavior, and blur when relevant.
- the exact location geography and prop/clue state that must remain continuous.
- one visible action only.
- body position and gaze direction, or a clear empty-frame rule.
- inner monologue as thought/post voiceover, with `此时他没有张嘴` or `画面中所有角色全程不说话`.
- `视频中只保留屏幕留白，文字后期叠加` for phones, UI, news, SMS, maps, files, surveillance, or timecodes.
- prohibitions for high-risk continuity failures.

If a video model requires 5-6 second generation but the edit target is 2-4 seconds, preserve both values: `duration_ms` for edit intent and `generation_duration` in the manifest for model submission. Do not add extra plot actions to fill model time.

### 17. 每个镜头可直接复制给视频 AI 的提示词

After each shot task card, include this prompt block:

```text
【项目风格】
{one concrete style line based on genre, environment, lighting, texture, and camera feel}

【参考】
使用上传的角色参考图、场景母版图、上一镜最后一帧。保持人物脸、服装、发型、空间方向和道具状态连续。

【依赖资产】
列出本镜头使用的 asset_id，包括角色图、场景图、物品图、线索图、关键帧图和上一镜尾帧。

【固定连续性】
{specific character state, screen direction, prop state, and spatial relation}

【本镜头】
镜头编号：
时长：
景别：
镜头运动：
动作：
只发生一件事。

【本镜头结束状态】
{where the image stops, where characters end, and prop state}

【下一镜衔接】
{what the next shot connects to}

【禁止变化】
不要换场景。不要新增无关角色。不要改变人物服装。不要改变关键道具状态。不要改变空间方向。不要让人物瞬移。不要生成乱码文字。不要提前暴露后面线索。不要让角色做出与剧情不符的动作。
```

### 18. 剪辑声音桥建议

Include:

- 镜头节奏: which segments slow down, speed up, or need pause.
- 声音桥设计 using breath, footsteps, siren, phone vibration, door sound, rain, heartbeat, machine sound, distant voices, broadcast, or ambience.
- Format for sound bridges:
  - 上一镜 -> 下一镜
  - 声音如何提前进入
  - 为什么这样接

### 19. 后期叠加建议

List information to add in post rather than AI video:

- Phone text
- News push
- SMS
- Subtitles
- Surveillance timecode
- Chat records
- Computer UI
- Maps/location
- Popups
- File content

Also include where the frame leaves clean space.

### 20. AI 生成风险清单

List at least 10 risks. Each risk must include:

- 风险
- 为什么会出错
- 会造成什么问题
- 如何在提示词里避免

Common risks: face changes, costume changes, swapped positions, disappearing props, prop state reset, phone appearing too early, weapon returning to hand,乱码文字, flipped screen direction, entrance/exit confusion, tiny clues, atmosphere-only shots, unmotivated behavior, missing establishing shots, confusing chase direction, premature end hook reveal.

### 21. 最终检查清单

Check:

1. 这一镜是否只发生一件事？
2. 这一镜是否给观众新增信息？
3. 这一镜是否能接上上一镜？
4. 这一镜是否能引出下一镜？
5. 人物位置是否连续？
6. 人物服装是否连续？
7. 人物情绪是否连续？
8. 道具状态是否连续？
9. 空间方向是否连续？
10. 重要线索是否按顺序出现？
11. 是否有建立空间的全景？
12. 是否有足够的细节镜头展示线索？
13. 是否有声音桥帮助转场？
14. 是否避免让视频 AI 生成复杂文字？
15. 是否把屏幕文字留给后期？
16. 是否标注了禁止变化？
17. 是否避免了无意义的气氛镜头？
18. 是否避免了重复镜头？
19. 是否每个段落都有明确目的？
20. 是否有一个清楚的结尾钩子？
21. 是否先完成资产抽取，再进入镜头任务？
22. 每个镜头是否列出依赖资产 ID？
23. 是否先生成角色图、场景图、物品图、线索图，再生成关键帧？
24. 是否经过资产验收后才调用视频模型？
25. 是否按 dry-run、单镜测试、小批量生成的顺序执行？
26. 专业镜头提示词是否定义并使用了 Location/Role/Prop placeholder map？
27. 每个专业镜头提示词是否把 `<duration-ms>`、`<location>`、`<role>` 等占位符解析成了具体时长、场景和角色？
28. 内心独白是否明确为心里想/后期旁白，并禁止角色张嘴？
29. POV 或无人空镜是否明确了视角归属？
30. 专业镜头提示词是否没有用额外动作填充模型生成时长？
