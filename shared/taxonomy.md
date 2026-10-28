# 动作数据和标签约定

`categories/` 是素材管理边界，不代表互斥的知识分类。`domains` 表示应用领域，如 `portrait`、`fitness`、`sports`、`yoga`；一个动作可有多个领域。`tags` 使用简短、具体的中文或英文术语，描述身体姿态、部位、场景、器械和动作特征；不要用标签代替结构化字段。

- `kind: pose` 是静态姿势，使用 `views`；`kind: movement` 是动态动作，按顺序使用 `phases`，每个阶段具有自己的视角图。阶段名称可为准备、发力、收尾等，以动作实际情况为准。序列或训练计划由 routine-builder 输出，不存成伪装成单个动作的记录。
- `people` 是人数；`framing` 为 `full_body`、`upper_body`、`mixed` 或 `other`。`content_rating` 必须明确为 `general`、`adult`、`unknown`；默认检索只返回 general。
- 视角 `angle` 使用 `front`、`side`、`diagonal`、`high`、`low`、`back`、`other`。角度描述基于可见事实；不知道时填 `other`。
- `difficulty` 是可选的粗略分类，不可代替针对个人的训练强度判断。`props` 是可选的道具名称。`extensions` 中健身、运动、瑜伽字段均为可选，内容须有可靠来源；空缺保持未填写。
- 可选 `keypoints` 为图片上归一化到 0–1 的二维坐标，原点为左上角；它们不是三维骨骼或自动的动作正确性判断。
- 动作 ID 采用 `类别:编号`，全局唯一、长期稳定。视角 ID 也须全局唯一。图片路径相对类别目录；不得越出类别目录。每条动作或视角须关联本类别 `sources.json` 中的来源；视角的来源可覆盖动作来源。
