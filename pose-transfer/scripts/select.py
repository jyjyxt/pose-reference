#!/usr/bin/env python3
"""Select up to nine local pose references for one multi-pose image."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts"))
try:
    from search import ADULT_LABELS  # shared catalogue policy
except ModuleNotFoundError:
    sys.exit("pose-reference catalogue not found; install it alongside this skill")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, help="Number of poses, 1–9 (default: 5)")
    parser.add_argument("--framing", choices=("mixed", "full", "upper"), default="mixed")
    parser.add_argument("--id", action="append", default=[], help="Exact catalogue ID; repeat for each selected pose")
    parser.add_argument("--adult", action="store_true", help="Allow adult-labelled references")
    args = parser.parse_args()
    if args.count is not None and not 1 <= args.count <= 9:
        parser.error("--count must be between 1 and 9")
    if len(args.id) > 9 or len(args.id) != len(set(args.id)):
        parser.error("provide at most 9 unique IDs")
    if args.id and args.count is not None and args.count != len(args.id):
        parser.error("--count must equal the number of IDs")
    data_path = ROOT / "references" / "poses.json"
    if not data_path.is_file():
        parser.error("pose-reference catalogue not found; install it alongside this skill")
    records = json.loads(data_path.read_text(encoding="utf-8"))
    def allowed(pose):
        labels = " ".join(pose[k] for k in ("体系", "分类", "姿势名称"))
        return args.adult or not any(label in labels for label in ADULT_LABELS)
    records = [p for p in records if allowed(p)]
    if args.id:
        by_id = {p["id"]: p for p in records}
        missing = [pose_id for pose_id in args.id if pose_id not in by_id]
        if missing:
            parser.error("IDs not found or excluded by the adult filter: " + ", ".join(missing))
        selected = [by_id[pose_id] for pose_id in args.id]
    else:
        count = args.count if args.count is not None else 5
        categories = ["站姿", "坐姿", "蹲姿", "跪立", "可爱系"]
        if args.framing == "full":
            categories.remove("可爱系")
        elif args.framing == "upper":
            categories = ["可爱系"]
        pools = {category: [] for category in categories}
        seen = set()
        # Prefer front-facing views while retaining poses that lack one.
        for pose in sorted(records, key=lambda p: p["角度"] != "正面"):
            category = pose["分类"]
            key = (pose["体系"], pose["姿势编号"])
            if category in pools and key not in seen:
                pools[category].append(pose)
                seen.add(key)
        selected = []
        while len(selected) < count and any(pools.values()):
            for category in categories:
                if pools[category] and len(selected) < count:
                    selected.append(pools[category].pop(0))
        if len(selected) < count:
            parser.error("not enough poses available for the requested framing")
    result = []
    for number, pose in enumerate(selected, 1):
        image_path = (ROOT / "assets" / pose["原图"]).with_suffix(".webp")
        thumbnail_path = (ROOT / "assets" / pose["缩略图"]).with_suffix(".webp")
        if not image_path.is_file() or not thumbnail_path.is_file():
            parser.error("missing local reference image for " + pose["id"])
        result.append({"number": number, "id": pose["id"], "name": pose["姿势名称"],
                       "category": pose["分类"], "angle": pose["角度"],
                       "image_path": str(image_path), "thumbnail_path": str(thumbnail_path)})
    print(json.dumps({"poses": result, "count": len(result)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
