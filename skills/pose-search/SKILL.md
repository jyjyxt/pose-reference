---
name: pose-search
description: Search local human pose and movement references by category, tags, person count, framing, phase, and camera angle.
---

# Pose Search

Identify the requested action, people, framing, and angle. Search using `python3 <repository>/shared/scripts/search.py --help`; use category, domain, repeated tags and keyword filters where relevant. The script outputs exact action and view IDs and local image paths. Use `--distinct` for one result per action. If no results exist, loosen relevant filters and say when the catalogue does not contain the requested action; do not invent entries.

Present a small useful selection and identify the action, phase where applicable, view and local image. Do not claim visual inspection unless performed. For images, route generation and transfer requests to the corresponding skills. Default searches return only `general` content; `--adult` additionally permits `adult` only when explicitly requested and appropriate. `unknown` is never returned by default or by `--adult` and must be reviewed and classified before use. Source details are in each category's `source.md` and `sources.json`; don't claim commercial rights.
