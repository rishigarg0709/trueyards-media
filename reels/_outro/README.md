# Voiced follow outro (Rishi approved the demo, 22 Nov 2026)

About 6 s at the end of a reel, replacing the silent 1.5 s follow card on TEST reels (test X15, alternate reels).

1. Voice: the reel's own narrator says "Liked this? Tap like, and follow TrueYards... for one real estate story, every day." Ready takes: library/media/outro-jessa.mp3, outro-george.mp3, outro-tara.mp3 (with .align.json). Trim leading silence, atempo about 1.18.
2. Background: put the reel's last scene image in as bg.jpg (it is blurred and darkened).
3. Timing: set window.TIMES = {like, follow, story, every, end} from the alignment (after the speed change). Jessa at 1.18x: like 1.22, follow 2.14, story 4.41, every 4.97, end 5.8.
4. Render outro.html with window.setT(t) at 30 fps (same frame renderer as the reel), append after the last scene. Sounds: a soft pop on "like", a tap on "follow"; keep the reel's music under it at low level and fade out.
5. Keep the reel's one accent colour if it is not teal (card button and dot colour).
Demo: demo-jessa.mp4.
