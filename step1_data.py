# Step 1: Structure your Instagram analytics data
# This is where you paste your weekly stats before turning them into a reel

# --- YOUR STATS (edit these each week) ---
my_stats = {
    "week": "June 16–22",
    "followers_gained": 412,
    "top_post_reach": 84000,
    "top_post_topic": "AI tools for creators",
    "reel_views": 210000,
    "profile_visits": 3100,
    "accounts_reached": 95000,
}

# --- WHAT WE WANT ON EACH SLIDE ---
slides = [
    f"Week of {my_stats['week']}",
    f"I gained {my_stats['followers_gained']} new followers this week",
    f"My top post reached {my_stats['top_post_reach']:,} accounts\nTopic: {my_stats['top_post_topic']}",
    f"Total reel views: {my_stats['reel_views']:,}",
    f"Profile visits: {my_stats['profile_visits']:,}",
    f"Total accounts reached: {my_stats['accounts_reached']:,}",
    "Follow for weekly creator analytics breakdowns",
]

# --- PRINT TO SEE THE OUTPUT ---
print("=== YOUR REEL SLIDES ===\n")
for i, slide in enumerate(slides):
    print(f"Slide {i+1}: {slide}")
    print("---")
