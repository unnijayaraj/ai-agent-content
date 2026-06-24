import os
from moviepy import ImageClip, concatenate_videoclips, vfx

# --- SETTINGS ---
SLIDES_FOLDER  = "slides"
OUTPUT_FILE    = "reel.mp4"
SECONDS_PER_SLIDE = 2.5      # how long each slide stays on screen
FPS = 30

# Load all slide images in order
slide_files = sorted([
    os.path.join(SLIDES_FOLDER, f)
    for f in os.listdir(SLIDES_FOLDER)
    if f.endswith(".png")
])

print(f"Found {len(slide_files)} slides. Building video...\n")

# Turn each image into a video clip with a fade-in effect
clips = []
for path in slide_files:
    clip = (
        ImageClip(path)
        .with_duration(SECONDS_PER_SLIDE)
        .with_effects([vfx.FadeIn(0.3)])
    )
    clips.append(clip)
    print(f"Added: {path}")

# Stitch all clips together
final = concatenate_videoclips(clips, method="compose")

# Export as MP4
print(f"\nExporting to {OUTPUT_FILE} ...")
final.write_videofile(OUTPUT_FILE, fps=FPS, codec="libx264", audio=False)

print(f"\nDone! Your reel is ready: {OUTPUT_FILE}")
print(f"Total duration: {final.duration:.1f} seconds")
