import os
import discord
from discord import Embed
from discord.ext import commands
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Carica il token dal file .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Impostiamo il fuso orario italiano (gestisce lui ora solare/legale)
italy_tz = pytz.timezone("Europe/Rome")

# Lista GP 2026 (Orari basati sul fuso italiano)
gps = [
    {"sigla": "MIA", "nome": "Miami", "sessions": [
        {"name": "FP1", "time": italy_tz.localize(datetime(2026, 5, 1, 18, 30))},
        {"name": "Qualifica Sprint", "time": italy_tz.localize(datetime(2026, 5, 1, 22, 30))},
        {"name": "Sprint Race", "time": italy_tz.localize(datetime(2026, 5, 2, 18, 0))},
        {"name": "Qualifica", "time": italy_tz.localize(datetime(2026, 5, 2, 22, 0))},
        {"name": "Gara", "time": italy_tz.localize(datetime(2026, 5, 3, 22, 0))},
    ]},
]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def get_next_event():
    # Otteniamo l'ora attuale "localizzata" in Italia
    now = datetime.now(italy_tz)
    for gp in gps:
        for session in gp["sessions"]:
            if session["time"] > now:
                return gp, session
    return None, None

def format_time(delta):
    d = delta.days
    h = delta.seconds // 3600
    m = (delta.seconds // 60) % 60
    s = delta.seconds % 60
    return f"{d}g {h}h {m}m {s}s"

@bot.event
async def on_ready():
    print(f"Countdown Bot online come {bot.user}")

@bot.command(name="countdown")
async def countdown(ctx):
    gp, session = get_next_event()
    if gp and session:
        now = datetime.now(italy_tz)
        diff = session["time"] - now
        countdown_text = f"⏳ {format_time(diff)}"
        
        embed = Embed(
            title=f"PROSSIMO EVENTO: {gp['nome']}",
            description=f"**Sessione:** {session['name']}\n**Mancano:** {countdown_text}",
            color=0xFF0000 # Rosso F1
        )
        embed.set_footer(text="Orari calcolati su fuso orario italiano")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Nessuna sessione futura trovata in archivio!")

bot.run(TOKEN)