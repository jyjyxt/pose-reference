# 类别名称

说明素材范围、适用场景、内容边界和类别维护规则。

## 添加数据

将本模板复制到 `categories/<类别名>/`；将 `category` 和 ID 前缀设成这个目录名。在 `sources.json` 填写来源 ID、描述和原始链接，并在 `source.md` 记录作者、许可范围和限制。下例是格式示意，路径、来源和动作内容必须替换为已核实的实际素材；不要把示例数据直接当成事实。

静态姿势：

```json
{
  "id": "mycategory:pose-001",
  "name": "动作名称",
  "kind": "pose",
  "category": "mycategory",
  "domains": ["fitness"],
  "tags": ["站姿"],
  "people": 1,
  "framing": "full_body",
  "content_rating": "unknown",
  "source_id": "source-001",
  "views": [
    {"id": "mycategory:pose-001:front", "angle": "front", "image": "img/pose-001-front.webp"}
  ]
}
```

动态动作将 `kind` 设为 `movement`，并将 `views` 替换为有序的 `phases`：

```json
"phases": [
  {
    "id": "preparation",
    "name": "准备",
    "views": [{"id": "mycategory:move-001:preparation:side", "angle": "side", "image": "img/move-001-preparation.webp"}]
  },
  {
    "id": "finish",
    "name": "收尾",
    "views": [{"id": "mycategory:move-001:finish:side", "angle": "side", "image": "img/move-001-finish.webp"}]
  }
]
```

来源示例（必须替换为真实来源）：

```json
{"source-001": {"description": "作者及来源说明", "url": "https://example.org/source"}}
```

按仓库 README 运行校验、建立索引并检查图片；`unknown` 在审核并明确分类前不会出现在搜索结果中。更多字段和标注约定见 `shared/pose.schema.json` 和 `shared/taxonomy.md`。
