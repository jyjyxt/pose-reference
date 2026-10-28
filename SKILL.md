---
name: pose-skills
description: Route requests for human pose references, pose-based image generation, movement guidance, or exercise routines to the appropriate bundled skill.
---

# Pose Skills

Choose the capability that matches the user's request and read its `SKILL.md` from this repository:

- Find pose or movement references: [pose-search](skills/pose-search/SKILL.md).
- Generate one image from a description or reference: [pose-generator](skills/pose-generator/SKILL.md).
- Put a supplied person into 1–9 different poses: [pose-transfer](skills/pose-transfer/SKILL.md).
- Explain or assess a movement: [form-coach](skills/form-coach/SKILL.md).
- Assemble a training or practice sequence: [routine-builder](skills/routine-builder/SKILL.md).

The repository must remain together: these skills share `shared/` and `categories/`. Use the actual repository path, not the current working directory. Current reference data is limited to the categories listed by `shared/scripts/search.py`; empty categories do not imply available training knowledge. Respect the source and content classification of each reference.
