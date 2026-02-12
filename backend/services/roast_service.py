from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

# Create client ONCE (not every function call)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_roast(player_data, intensity="fun"):
    try:
        wins = player_data.get("wins", 0)
        losses = player_data.get("losses", 0)
        trophies = player_data.get("trophies", 0)
        best = player_data.get("bestTrophies", 0)
        three_crowns = player_data.get("threeCrownWins", 0)

        total_games = wins + losses
        win_rate = (wins / total_games) * 100 if total_games > 0 else 0
        three_crown_rate = (three_crowns / wins) * 100 if wins > 0 else 0
        trophy_difference = trophies - best

        # 🔥 Player classification
        if win_rate < 45:
            player_type = "Struggling Ladder Player"
        elif win_rate > 60:
            player_type = "Competitive Grinder"
        else:
            player_type = "Casual Player"

        tone_map = {
            "fun": "Keep it playful and light.",
            "savage": "Make it sharp but not toxic.",
            "nuclear": "Make it brutally funny but no hate speech."
        }

        prompt = f"""
You are a Gen-Z Clash Royale esports commentator streaming live on Twitch.
Personality: chaotic, dramatic, meme-aware, slightly unhinged but never toxic.

PLAYER STATS:
- Player Type: {player_type}
- Win Rate: {win_rate:.2f}%
- Three Crown Rate: {three_crown_rate:.2f}%
- Trophy Difference From Best: {trophy_difference}

ROAST INTENSITY:
{tone_map.get(intensity, tone_map["fun"])}

INSTRUCTIONS:
- React like you just saw these stats on stream.
- Twitch chat energy.
- 2-4 sentences maximum.
- 1-3 emojis maximum.
- No hate speech.
- Do NOT repeat raw numbers unless for comedic emphasis.
- Return ONLY the roast text.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a gaming analyst and comedian."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=150
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return "Chat is lagging, servers cooked 💀 Try again."