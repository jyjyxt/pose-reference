#!/usr/bin/env python3
"""Search the bundled pose catalogue and return image references as JSON."""
import argparse
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://ai-pose-gallery.anhao.app/"
ALIASES = {
    "standing": "站姿", "stand": "站姿", "sitting": "坐姿", "sit": "坐姿",
    "squatting": "蹲姿", "kneeling": "跪立", "lying": "卧",
    "front": "正面", "side": "侧面", "high angle": "俯视", "low angle": "仰视",
    "upper body": "上半身", "full body": "全身", "couple": "双人",
}
ADULT_LABELS = ("性感", "大胆", "挤胸", "事业线", "缠绵", "后入位", "正常位", "骑乘位", "坐位贴身", "立位贴身", "贴身", "面对面坐位", "背向坐位")


def normalize(value):
    value = value.strip().casefold()
    return ALIASES.get(value, value)


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog="English aliases: " + ", ".join(ALIASES))
    parser.add_argument("--query", default="", help="Keyword or exact English alias; matches ID, category, pose, system or angle")
    parser.add_argument("--angle", default="", help="Angle, e.g. front, side, 正面, 斜侧")
    parser.add_argument("--system", default="", help="System, e.g. full body, upper body, couple")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of results, 1–50")
    parser.add_argument("--distinct", action="store_true", help="Return at most one angle per pose")
    parser.add_argument("--adult", action="store_true", help="Include adult-labelled catalogue entries")
    args = parser.parse_args()
    if not 1 <= args.limit <= 50:
        parser.error("--limit must be between 1 and 50")
    with (ROOT / "references" / "poses.json").open(encoding="utf-8") as f:
        poses = json.load(f)
    query, angle, system = map(normalize, (args.query, args.angle, args.system))
    results = []
    seen_poses = set()
    for pose in poses:
        labels = " ".join(pose[k] for k in ("体系", "分类", "姿势名称"))
        if not args.adult and any(label in labels for label in ADULT_LABELS):
            continue
        if query not in pose["检索"].casefold() or angle not in pose["角度"].casefold() or system not in pose["体系"].casefold():
            continue
        pose_key = (pose["体系"], pose["姿势编号"])
        if args.distinct and pose_key in seen_poses:
            continue
        seen_poses.add(pose_key)
        results.append({"id": pose["id"], "name": pose["姿势名称"], "category": pose["分类"],
                        "system": pose["体系"], "angle": pose["角度"],
                        "thumbnail_path": str((ROOT / "assets" / pose["缩略图"]).with_suffix(".webp")),
                        "image_path": str((ROOT / "assets" / pose["原图"]).with_suffix(".webp")),
                        "thumbnail_url": BASE + quote(pose["缩略图"], safe="/"),
                        "image_url": BASE + quote(pose["原图"], safe="/")})
        if len(results) == args.limit:
            break
    print(json.dumps({"results": results, "count": len(results)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
