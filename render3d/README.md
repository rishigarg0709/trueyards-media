# 3D renders

Blender scale models rendered in the cloud by `.github/workflows/render3d.yml` (Cycles on CPU, 20 machines in parallel).

- `fit/`: Forteasia Industrial Township model. `layout.py` measures the township off the developer's site plan D5 and writes `layout.json` (metres); `build.py` builds the model in Blender from it and renders a turntable with a transparent background. Change `job.json` (frames, size, samples, start angle) and push to render again.
- Output: workflow artifact `<model>-webp` (desktop 1600 px and mobile 900 px WebP frames with alpha, plus `sheet.jpg`). Nothing large is committed here.
- Representational model, not the actual site.
