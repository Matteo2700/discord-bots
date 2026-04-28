import discord
import asyncio
import os
from flask import Flask
import threading

# --- WEB SERVER (serve per uptime) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot online!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

keep_alive()

# --- BOT SETUP ---
intents = discord.Intents.default()

bot1 = discord.Client(intents=intents)
bot2 = discord.Client(intents=intents)
bot3 = discord.Client(intents=intents)

@bot1.event
async def on_ready():
    print(f"Bot1 online: {bot1.user}")

@bot2.event
async def on_ready():
    print(f"Bot2 online: {bot2.user}")

@bot3.event
async def on_ready():
    print(f"Bot3 online: {bot3.user}")

async def main():
    await asyncio.gather(
        bot1.start(os.getenv("TOKEN1")),
        bot2.start(os.getenv("TOKEN2")),
        bot3.start(os.getenv("TOKEN3"))
    )

asyncio.run(main())
