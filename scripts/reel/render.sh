#!/bin/bash
# usage: scripts/reel/render.sh <reel_dir>   -> renders frames in 5 parallel batches and encodes <dir>/reel.mp4 with <dir>/audio.wav
set -e; D=$(cd "$1" && pwd); S=$(cd "$(dirname "$0")" && pwd)
END=$(python3 -c "import json;w=json.load(open('$D/words.json'));print(round(w[-1][2]+2.3,3))")
rm -rf "$D/frames"; mkdir -p "$D/frames"
STEP=$(python3 -c "print(round($END/5+0.034,3))")
for i in 0 1 2 3 4; do A=$(python3 -c "print(round($i*$STEP,3))"); B=$(python3 -c "print(min(round(($i+1)*$STEP,3),$END))"); node "$S/shot.cjs" "$D" $A $B 2>&1 | grep ERR & done; wait || true
ffmpeg -y -v error -framerate 30 -i "$D/frames/f%05d.jpg" -i "$D/audio.wav" -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$D/reel.mp4"
rm -rf "$D/frames"; ls -la "$D/reel.mp4"
