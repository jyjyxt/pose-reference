#!/usr/bin/env python3
"""Build one pose-reference sheet from the shared catalogue using ffmpeg."""
import argparse
import json
import math
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Output PNG path; existing files are not overwritten")
    parser.add_argument("--count", type=int, default=None, help="Number of poses (1–9; defaults to 5 without IDs)")
    parser.add_argument("--framing", choices=("mixed", "full", "upper"), default="mixed")
    parser.add_argument("--id", action="append", default=[], help="Exact pose ID; repeat in the desired order")
    parser.add_argument("--adult", action="store_true", help="Allow adult-labelled references")
    args = parser.parse_args()
    selector = Path(__file__).resolve().with_name("select_poses.py")
    command = [sys.executable, str(selector), "--framing", args.framing]
    if args.count is not None:
        command += ["--count", str(args.count)]
    for pose_id in args.id:
        command += ["--id", pose_id]
    if args.adult:
        command.append("--adult")
    selected = subprocess.run(command, capture_output=True, text=True)
    if selected.returncode:
        parser.error(selected.stderr.strip())
    poses = json.loads(selected.stdout)["poses"]
    if args.output.exists():
        parser.error("output already exists: " + str(args.output))
    if args.output.suffix.lower() != ".png":
        parser.error("output must be a PNG file")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    columns = min(3, len(poses))
    rows = math.ceil(len(poses) / columns)
    ffmpeg = ["ffmpeg", "-v", "error", "-n"]
    for pose in poses:
        ffmpeg += ["-i", pose["image_path"]]
    filters = [f"[{i}:v]scale=300:400:force_original_aspect_ratio=decrease,pad=300:400:(ow-iw)/2:(oh-ih)/2:white,setsar=1[p{i}]" for i in range(len(poses))]
    inputs = "".join(f"[p{i}]" for i in range(len(poses)))
    layout = "|".join(f"{(i % columns) * 300}_{(i // columns) * 400}" for i in range(len(poses)))
    if len(poses) == 1:
        filters.append("[p0]null[out]")
    else:
        filters.append(f"{inputs}xstack=inputs={len(poses)}:layout={layout}:fill=white[out]")
    ffmpeg += ["-filter_complex", ";".join(filters), "-map", "[out]", "-frames:v", "1", str(args.output)]
    try:
        subprocess.run(ffmpeg, check=True)
    except FileNotFoundError:
        parser.error("ffmpeg is required to build a pose sheet")
    except subprocess.CalledProcessError as error:
        parser.error(f"ffmpeg failed with exit code {error.returncode}")
    print(json.dumps({"sheet_path": str(args.output.resolve()), "rows": rows, "columns": columns, "poses": poses}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
