---
name: pose-reference
description: Find human pose reference images and photo pose ideas for AI image generation, drawing, 3D, and photography. Use when someone asks for pose references, posing ideas, drawing poses, 拍照姿势, 人体姿势参考 or AI 绘画姿势.
---

# Pose Reference

Find existing pose references from the bundled Chinese-language catalogue and local image collection. Each result includes local image paths, source links, the pose name, category, angle, and ID. The catalogue covers single-person full-body and upper-body poses and couples, with multiple viewing angles.

## Workflow

1. Identify the requested pose, number of people, body framing and angle. If the request is broad, suggest a small varied selection; ask a question only when the answer is necessary to choose.
2. Search the catalogue with `python3 <skill-directory>/scripts/search.py`, replacing `<skill-directory>` with this skill's actual directory. Use `--help` for filters and the built-in English vocabulary. Search Chinese pose terms when possible; try related terms or remove filters if there are no matches. Do not invent catalogue entries.
3. Present 3–5 relevant poses with names, angles, local image paths or links and a brief explanation of how each fits. Prefer the local images; the source links require network access and may become unavailable. For more angles, search the same pose ID prefix or pose name.
4. If asked for an image-generation prompt, translate the chosen pose into clear, concrete body positioning and camera direction. Identify it as a suggested prompt, not a guarantee that an image model will reproduce the pose. To generate a similar image from one reference, use `pose-generator` when available. For a multi-pose image of a supplied person, use `pose-transfer` when available. Otherwise use the available image-generation tool and reference image if supported.

## Boundaries

- Default searches exclude catalogue entries labelled as adult or sexual; use `--adult` only when the user explicitly requests adult reference material. Adult results are not appropriate for minors.
- The catalogue is a reference collection, not a photography shoot planner or a guarantee of anatomically correct poses. Do not claim to have visually inspected an image unless you actually have.
- Image and original metadata rights belong to the original creator, ギア. The repository's MIT code license does not cover these assets. Attribute the source, and do not assert commercial reuse rights; see `references/source.md`.

Example: `python3 <skill-directory>/scripts/search.py --query standing --angle front --limit 3`
