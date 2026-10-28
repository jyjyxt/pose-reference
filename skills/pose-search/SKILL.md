---
name: pose-search
description: Search local human pose and movement references by category, tags, person count, framing, phase, and camera angle.
---

# Pose Search

Identify the requested action, people, framing, and angle. Search using `python3 <repository>/shared/scripts/search.py --help`; use category, domain, repeated tags and keyword filters where relevant. The script outputs exact action and view IDs and local image paths. Use `--distinct` for one result per action. If no results exist, loosen relevant filters and say when the catalogue does not contain the requested action; do not invent entries.

Kungfu actions have permanent `KF` numbers such as `KF001`, listed in `categories/kungfu/numbered-poses.md` and stored as tags. Search a number using `--category kungfu --query KF001`, and confirm an exact tag match. Explicitly specified kungfu number 1 can be normalized to `KF001`; an unqualified list number refers only to a list already shown to the user. Never substitute a different action or an unavailable angle.

Present a small useful selection and identify the action, phase where applicable, view and local image. Do not claim visual inspection unless performed. For images, route generation and transfer requests to the corresponding skills. Default searches return only `general` content; `--adult` additionally permits `adult` only when explicitly requested and appropriate. `unknown` is never returned by default or by `--adult` and must be reviewed and classified before use. Source details are in each category's `source.md` and `sources.json`; don't claim commercial rights.
