import os
from PIL import Image, ImageDraw, ImageFont

# --- YOUR 7 SLIDES (copy from step2 output, or we'll auto-connect later) ---
slides = [
    "We hit 210K views\nthis week.\nHere's why.",
    "AI tools for creators\ndominated.\n84K reach.",
    "95K accounts discovered\nour content organically.",
    "3,100 profile visits\nin seven days.",
    "412 new followers\njoined the data squad.",
    "Data-driven content wins.\nAlways.",
    "Follow for weekly\nanalytics breakdowns.",
]

# --- SETTINGS ---
WIDTH, HEIGHT = 1080, 1920       # Instagram Reel size (9:16)
OUTPUT_FOLDER = "slides"         # Folder where images will be saved
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Brand colors (feel free to change these hex codes)
BACKGROUND_TOP    = (15, 15, 30)     # dark navy
BACKGROUND_BOTTOM = (40, 10, 60)     # deep purple
TEXT_COLOR        = (255, 255, 255)  # white
ACCENT_COLOR      = (180, 100, 255)  # purple accent

# Font paths
FONT_BOLD   = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_LIGHT  = "/System/Library/Fonts/Helvetica.ttc"


def make_gradient(width, height, top_color, bottom_color):
    """Creates a top-to-bottom gradient background."""
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return image


def make_slide(text, slide_number, total_slides):
    """Creates a single slide image."""
    image = make_gradient(WIDTH, HEIGHT, BACKGROUND_TOP, BACKGROUND_BOTTOM)
    draw = ImageDraw.Draw(image)

    # Slide counter (top right)
    try:
        small_font = ImageFont.truetype(FONT_LIGHT, 40)
    except Exception:
        small_font = ImageFont.load_default()

    counter_text = f"{slide_number}/{total_slides}"
    draw.text((WIDTH - 120, 80), counter_text, font=small_font, fill=(150, 150, 180))

    # Accent line (left side)
    draw.rectangle([(80, HEIGHT // 2 - 200), (90, HEIGHT // 2 + 200)], fill=ACCENT_COLOR)

    # Main text (centered)
    try:
        main_font = ImageFont.truetype(FONT_BOLD, 90)
    except Exception:
        main_font = ImageFont.load_default()

    # Word-wrap and center the text block
    lines = text.strip().split("\n")
    line_height = 110
    total_text_height = len(lines) * line_height
    y_start = (HEIGHT - total_text_height) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=main_font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        y = y_start + i * line_height
        draw.text((x, y), line, font=main_font, fill=TEXT_COLOR)

    # Bottom accent dot row
    for dot in range(total_slides):
        cx = (WIDTH // 2) - (total_slides * 30 // 2) + dot * 30 + 15
        cy = HEIGHT - 120
        color = ACCENT_COLOR if (dot + 1) == slide_number else (80, 80, 100)
        draw.ellipse([(cx - 8, cy - 8), (cx + 8, cy + 8)], fill=color)

    filename = f"{OUTPUT_FOLDER}/slide_{slide_number:02d}.png"
    image.save(filename)
    print(f"Saved: {filename}")
    return filename


# --- RUN IT ---
print("Creating slides...\n")
saved_files = []
for i, slide_text in enumerate(slides):
    path = make_slide(slide_text, i + 1, len(slides))
    saved_files.append(path)

print(f"\nDone! {len(saved_files)} slides saved to the '{OUTPUT_FOLDER}' folder.")
