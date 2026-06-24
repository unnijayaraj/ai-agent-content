import os
from dotenv import load_dotenv
import anthropic
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, concatenate_videoclips, vfx

load_dotenv()

# ─────────────────────────────────────────
#  YOUR WEEKLY STATS — edit this each week
# ─────────────────────────────────────────
STATS = {
    "week": "June 16–22",
    "followers_gained": 412,
    "top_post_reach": 84000,
    "top_post_topic": "AI tools for creators",
    "reel_views": 210000,
    "profile_visits": 3100,
    "accounts_reached": 95000,
}

# ─────────────────────────────────────────
#  SETTINGS
# ─────────────────────────────────────────
SLIDES_FOLDER = "slides"
OUTPUT_FILE   = "reel.mp4"
WIDTH, HEIGHT = 1080, 1920
SECONDS_PER_SLIDE = 2.5
FPS = 30

BG_TOP      = (15, 15, 30)
BG_BOTTOM   = (40, 10, 60)
TEXT_COLOR  = (255, 255, 255)
ACCENT      = (180, 100, 255)
FONT_PATH   = "/System/Library/Fonts/HelveticaNeue.ttc"


# ─────────────────────────────────────────
#  STEP 1 — Generate slide text with Claude
# ─────────────────────────────────────────
def generate_slides(stats: dict) -> list[str]:
    print("Step 1: Asking Claude to write your slide script...")

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""
You are a viral Instagram content writer for a creator who posts data-driven reels.

Here are this week's Instagram analytics:
- Week: {stats['week']}
- New followers: {stats['followers_gained']}
- Top post reach: {stats['top_post_reach']:,} (topic: {stats['top_post_topic']})
- Reel views: {stats['reel_views']:,}
- Profile visits: {stats['profile_visits']:,}
- Accounts reached: {stats['accounts_reached']:,}

Write exactly 7 slides for an Instagram Reel. Each slide is short (max 8 words).
Use line breaks (\\n) to split long slides across 2 lines.
Format your response exactly like this, nothing else:
SLIDE 1: [text]
SLIDE 2: [text]
SLIDE 3: [text]
SLIDE 4: [text]
SLIDE 5: [text]
SLIDE 6: [text]
SLIDE 7: [text]
CAPTION: [1-2 sentence caption with hashtags]

Make slide 1 a strong hook. Make slide 7 a follow CTA.
"""
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    slides = []
    caption = ""

    for line in raw.strip().split("\n"):
        if line.startswith("SLIDE") and ":" in line:
            text = line.split(":", 1)[1].strip()
            slides.append(text)
        elif line.startswith("CAPTION") and ":" in line:
            caption = line.split(":", 1)[1].strip()

    print(f"  Got {len(slides)} slides from Claude.")
    print(f"  Caption: {caption}\n")
    return slides, caption


# ─────────────────────────────────────────
#  STEP 2 — Render each slide as an image
# ─────────────────────────────────────────
def render_images(slides: list[str]) -> list[str]:
    print("Step 2: Rendering slide images...")
    os.makedirs(SLIDES_FOLDER, exist_ok=True)

    saved = []
    for i, text in enumerate(slides):
        path = _draw_slide(text, i + 1, len(slides))
        saved.append(path)
        print(f"  Saved: {path}")

    print()
    return saved


def _draw_slide(text: str, slide_num: int, total: int) -> str:
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(HEIGHT):
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * y / HEIGHT)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * y / HEIGHT)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * y / HEIGHT)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

    try:
        font_main  = ImageFont.truetype(FONT_PATH, 90)
        font_small = ImageFont.truetype(FONT_PATH, 40)
    except Exception:
        font_main  = ImageFont.load_default()
        font_small = font_main

    # Slide counter
    draw.text((WIDTH - 120, 80), f"{slide_num}/{total}", font=font_small, fill=(150, 150, 180))

    # Accent bar
    draw.rectangle([(80, HEIGHT // 2 - 200), (90, HEIGHT // 2 + 200)], fill=ACCENT)

    # Main text
    lines = text.strip().split("\\n")
    line_h = 110
    y_start = (HEIGHT - len(lines) * line_h) // 2
    for j, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_main)
        x = (WIDTH - (bbox[2] - bbox[0])) // 2
        draw.text((x, y_start + j * line_h), line, font=font_main, fill=TEXT_COLOR)

    # Progress dots
    for d in range(total):
        cx = (WIDTH // 2) - (total * 30 // 2) + d * 30 + 15
        color = ACCENT if (d + 1) == slide_num else (80, 80, 100)
        draw.ellipse([(cx - 8, HEIGHT - 128), (cx + 8, HEIGHT - 112)], fill=color)

    path = f"{SLIDES_FOLDER}/slide_{slide_num:02d}.png"
    img.save(path)
    return path


# ─────────────────────────────────────────
#  STEP 3 — Stitch images into a video
# ─────────────────────────────────────────
def create_video(image_paths: list[str]) -> str:
    print("Step 3: Creating video...")

    clips = [
        ImageClip(p).with_duration(SECONDS_PER_SLIDE).with_effects([vfx.FadeIn(0.3)])
        for p in image_paths
    ]
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(OUTPUT_FILE, fps=FPS, codec="libx264", audio=False, logger=None)

    print(f"  Video saved: {OUTPUT_FILE} ({final.duration:.1f}s)\n")
    return OUTPUT_FILE


# ─────────────────────────────────────────
#  PIPELINE — runs all 3 steps in order
# ─────────────────────────────────────────
def run_pipeline(stats: dict):
    print("=" * 40)
    print("   REEL PIPELINE STARTING")
    print("=" * 40 + "\n")

    slides, caption = generate_slides(stats)   # Step 1
    image_paths     = render_images(slides)    # Step 2
    video_path      = create_video(image_paths) # Step 3

    print("=" * 40)
    print("   DONE!")
    print("=" * 40)
    print(f"\nVideo:   {video_path}")
    print(f"Caption: {caption}")


if __name__ == "__main__":
    run_pipeline(STATS)
