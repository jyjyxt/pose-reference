#!/usr/bin/env python3
"""Convert images to WebP without resizing or overwriting existing files."""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)

def dimensions(path):
    data=json.loads(run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(path)]).stdout)
    stream=data['streams'][0]
    return stream['width'],stream['height']

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('images',nargs='+',type=Path); p.add_argument('--output-dir',required=True,type=Path); p.add_argument('--quality',type=int,default=85)
    a=p.parse_args()
    if not 0<=a.quality<=100: p.error('--quality must be 0–100')
    outputs=[a.output_dir/(x.stem+'.webp') for x in a.images]
    if len(set(outputs))!=len(outputs): p.error('input names produce duplicate output names')
    if any(x.exists() for x in outputs): p.error('an output already exists; refusing to overwrite')
    if any(not x.is_file() for x in a.images): p.error('an input image does not exist')
    a.output_dir.mkdir(parents=True,exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(dir=a.output_dir) as tmp:
            staged=[]
            for source,out in zip(a.images,outputs):
                target=Path(tmp)/out.name
                size=dimensions(source)
                run(['cwebp','-quiet','-q',str(a.quality),str(source),'-o',str(target)])
                if dimensions(target)!=size: raise ValueError(f'dimensions changed for {source}')
                run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'])
                staged.append(target)
            for src,out in zip(staged,outputs):
                # Exclusive creation avoids replacing an existing file.
                with out.open('xb') as f: f.write(src.read_bytes())
    except (OSError, ValueError, IndexError, KeyError, subprocess.CalledProcessError) as exc:
        print(f'image conversion failed: {exc}',file=sys.stderr); return 1
    print(json.dumps({'images':[str(x.resolve()) for x in outputs]},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': sys.exit(main())
