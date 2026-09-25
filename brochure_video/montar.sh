#!/bin/bash
set -e
FPS=30
# escena:duracion:+margen
declare -A DUR
DUR[escena_01]=$(echo "13.3+0.5"|bc)
DUR[escena_02]=$(echo "17.3+0.5"|bc)
DUR[escena_03]=$(echo "17.7+0.5"|bc)
DUR[escena_04]=$(echo "19.3+0.5"|bc)
DUR[escena_05]=$(echo "12.8+0.5"|bc)
DUR[escena_cierre]=$(echo "9.6+0.5"|bc)

for s in escena_01 escena_02 escena_03 escena_04 escena_05 escena_cierre; do
  d=${DUR[$s]}; N=$(echo "$d*$FPS/1"|bc)
  echo ">> clip $s dur=$d frames=$N"
  ffmpeg -y -v error -loop 1 -i $s.png \
    -filter_complex "zoompan=z='min(zoom+0.0008,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=$FPS,format=yuv420p" \
    -t $d -r $FPS clip_$s.mp4
done
echo "CLIPS OK"
ls -la clip_*.mp4
