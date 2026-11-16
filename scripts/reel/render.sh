#!/bin/bash
# usage: scripts/reel/render.sh <reel_dir>
# Renders 2160x3840 (4K UHD vertical) frames in 5 parallel batches, then encodes one master and per-platform exports:
#   reel-4k.mp4   2160x3840  master, YouTube Shorts (YouTube plays 4K)
#   reel.mp4      1440x2560  Instagram, Facebook, Threads, LinkedIn (Meta API caps width at 1920 and 25 Mbps)
#   reel-x.mp4    1068x1900  X (caps portrait video at 1200x1900)
# All: H.264 High, closed GOP, 30 fps, yuv420p, AAC 48 kHz. Set SCALE=1 for a fast 1080p draft.
set -e; D=$(cd "$1" && pwd); S=$(cd "$(dirname "$0")" && pwd)
END=$(python3 -c "import json;w=json.load(open('$D/words.json'));print(round(w[-1][2]+2.3,3))")
rm -rf "$D/frames"; mkdir -p "$D/frames"
STEP=$(python3 -c "print(round($END/5+0.034,3))")
for i in 0 1 2 3 4; do A=$(python3 -c "print(round($i*$STEP,3))"); B=$(python3 -c "print(min(round(($i+1)*$STEP,3),$END))"); node "$S/shot.cjs" "$D" $A $B 2>&1 | grep ERR & done; wait || true
V="-c:v libx264 -profile:v high -level:v 5.1 -pix_fmt yuv420p -r 30 -g 60 -keyint_min 60 -sc_threshold 0 -flags +cgop -movflags +faststart"
A="-c:a aac -ar 48000 -ac 2"
ffmpeg -y -v error -framerate 30 -i "$D/frames/f%05d.jpg" -i "$D/audio.wav" $V -preset slow -crf 14 -maxrate 60M -bufsize 120M $A -b:a 256k -shortest "$D/reel-4k.tmp.mp4"
mv "$D/reel-4k.tmp.mp4" "$D/reel-4k.mp4"; rm -rf "$D/frames"
ffmpeg -y -v error -i "$D/reel-4k.mp4" -vf "scale=1440:2560:flags=lanczos" $V -preset slow -crf 15 -maxrate 24M -bufsize 48M $A -b:a 128k "$D/reel.tmp.mp4" && mv "$D/reel.tmp.mp4" "$D/reel.mp4"
ffmpeg -y -v error -i "$D/reel-4k.mp4" -vf "scale=1068:1900:flags=lanczos" $V -preset slow -crf 17 -maxrate 20M -bufsize 40M $A -b:a 128k "$D/reel-x.tmp.mp4" && mv "$D/reel-x.tmp.mp4" "$D/reel-x.mp4"
ls -la "$D"/reel*.mp4
