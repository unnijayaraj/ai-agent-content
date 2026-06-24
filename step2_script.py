import os
from dotenv import load_dotenv
import anthropic

# Load your API key from .env file
load_dotenv()

# Connect to Claude
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# --- YOUR STATS (same as step 1, edit these each week) ---
my_stats = {
    "week": "June 16–22",
    "followers_gained": 412,
    "top_post_reach": 84000,
    "top_post_topic": "AI tools for creators",
    "reel_views": 210000,
    "profile_visits": 3100,
    "accounts_reached": 95000,
}

# --- ASK CLAUDE TO WRITE THE REEL SCRIPT ---
prompt = f"""
You are a viral Instagram content writer for a creator who posts data-driven reels.

Here are this week's Instagram analytics:
- Week: {my_stats['week']}
- New followers: {my_stats['followers_gained']}
- Top post reach: {my_stats['top_post_reach']:,} (topic: {my_stats['top_post_topic']})
- Reel views: {my_stats['reel_views']:,}
- Profile visits: {my_stats['profile_visits']:,}
- Accounts reached: {my_stats['accounts_reached']:,}

Write exactly 7 slides for an Instagram Reel. Each slide is short (max 8 words).
Format your response exactly like this:
SLIDE 1: [text]
SLIDE 2: [text]
SLIDE 3: [text]
SLIDE 4: [text]
SLIDE 5: [text]
SLIDE 6: [text]
SLIDE 7: [text]
CAPTION: [1-2 sentence caption with relevant hashtags]

Make slide 1 a strong hook. Make slide 7 a follow CTA.
"""

print("Asking Claude to write your reel script...\n")

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}]
)

response = message.content[0].text
print("=== YOUR REEL SCRIPT ===\n")
print(response)
