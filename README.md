# Pose Skills

一个共享动作图库的 Agent Skills 项目：搜索姿势与动作参考、根据描述或参考生图、将同一人物转成多姿势图片，以及编写动作讲解与练习序列。各能力独立定义在 `skills/`，数据、来源和工具由整个仓库共享。

## 能力与现有数据

| Skill | 用途 |
| --- | --- |
| [pose-search](skills/pose-search/SKILL.md) | 按关键词、类别、标签、人数、景别和视角找参考 |
| [pose-generator](skills/pose-generator/SKILL.md) | 根据文字或参考生成一张图片 |
| [pose-transfer](skills/pose-transfer/SKILL.md) | 用人物图及 1～9 个参考生成一张多动作图片 |
| [form-coach](skills/form-coach/SKILL.md) | 解释动作或根据可观察的材料讨论动作形式 |
| [routine-builder](skills/routine-builder/SKILL.md) | 根据目标、条件和经验编排练习序列 |

[根目录 SKILL.md](SKILL.md) 是分流入口。要保留完整仓库目录才能共享数据和脚本；单独复制一个子 Skill 不包含其依赖。是否自动发现嵌套 Skill 取决于 Agent 环境，可直接指定对应的 `SKILL.md` 或从根入口路由。

- `categories/reference`：现有ギア姿势图库，包括静态线稿及多个视角；部分内容为成人向，默认不显示。
- `categories/fitness`、`categories/sports`、`categories/yoga`：已建立数据结构，**目前没有动作素材或教学数据**。不能将通用参考图库当作训练动作标准。
- 教学和训练建议需要合适的可靠来源；图片生成需要 Agent 环境提供支持参考图的生成工具。

## 示例：一张人物照生成九宫格

| 人物参考 | 动作参考 | 生成结果 |
| --- | --- | --- |
| ![人物参考照](examples/reference/fashion-portrait.webp) | ![九个动作参考](examples/reference/pose-reference-grid-latest.webp) | ![九宫格生成结果](examples/reference/pose-transfer-demo-latest.webp) |

示例人物及结果由 AI 生成。单次生成可改善一致性，但不保证人物和动作完全一致。

## 命令

在仓库根目录运行（或使用脚本绝对路径）；需要 Python 3.9+。拼图需 FFmpeg，图片压缩需 `cwebp`、`ffprobe` 和 FFmpeg：

```bash
python3 shared/scripts/search.py --query 站姿 --people 1 --framing full_body --angle front --distinct
python3 skills/pose-transfer/scripts/select_poses.py --count 9 --framing full
python3 skills/pose-transfer/scripts/build_pose_sheet.py --count 9 --framing full --output /tmp/pose-sheet.png
python3 shared/scripts/validate.py --check-index
```

搜索结果中的 `id` 是动作 ID，`view_id` 是具体视角 ID；重复传入 `--id` 可指定选择顺序。动态动作会返回阶段。按类别或领域筛选可用 `--category`、`--domain` 和重复的 `--tag`；动态阶段和道具可用 `--phase`、`--prop`；各脚本的 `--help` 有完整参数。默认只返回 `general` 内容，明确要求成人素材时可传 `--adult`；`unknown` 数据需先审核分类。

## 扩展数据

1. 复制 `templates/category/` 到 `categories/<类别名>/`，补充 `CATEGORY.md`、`source.md` 和 `sources.json`。每项来源记录需有 `description` 和 `url`；动作或视角通过 `source_id` 关联，可由视角覆盖动作来源。
2. 将图片放到类别的 `assets/`，按 [taxonomy.md](shared/taxonomy.md) 和 [pose.schema.json](shared/schema/pose.schema.json) 编写 `poses.json`。静态姿势使用 `views`，动态动作使用按顺序排列的 `phases`，阶段下的视角提供具体图像。
3. 新图先压缩并检查可读性：`python3 shared/scripts/compress_images.py <图片路径> --output-dir <目标目录>`。脚本输出 WebP、不缩放、不覆盖，并验证尺寸及可解码性；人工检查文字、细节是否仍清晰。
4. 执行 `python3 shared/scripts/validate.py`，再执行 `python3 shared/scripts/build_index.py`。提交前运行 `python3 shared/scripts/validate.py --check-index`；索引是生成产物，不手改。搜索和选择会拒绝过期索引。
5. 检查对应检索、视角和参考拼图。未经验证或没有适用授权的素材与教学数据不应入库。

类别文件是数据真源，分类目录作为维护边界，`domains` 和标签支持跨类别检索。来源记录用于追溯，不能替代核实实际授权。

## 素材来源

现有参考图库及原始数据属于 ギア；中文数据来源及具体使用限制见 [source.md](categories/reference/source.md)。本仓库不声称拥有这些素材的商业使用授权。
