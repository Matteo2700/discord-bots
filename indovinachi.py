import discord
import random
import os
from datetime import date
from dotenv import load_dotenv

# Carichiamo le chiavi
load_dotenv()
TOKEN_BOT = os.getenv("TOKEN_BOT")
ID_CANALE = int(os.getenv("ID_CANALE"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# DATABASE PILOTI (Aggiornato con date di nascita corrette)
piloti = [
    {"nome":"Lando Norris","naz":"inglese","team":"mclaren","numero":4,"nascita":"1999-11-13"},
    {"nome":"Oscar Piastri","naz":"australiano","team":"mclaren","numero":81,"nascita":"2001-04-06"},
    {"nome":"Kimi Antonelli","naz":"italiano","team":"mercedes","numero":12,"nascita":"2006-08-25"},
    {"nome":"George Russell","naz":"inglese","team":"mercedes","numero":63,"nascita":"1998-02-15"},
    {"nome":"Max Verstappen","naz":"olandese","team":"red bull","numero":1,"nascita":"1997-09-30"},
    {"nome":"Isack Hadjar","naz":"francese","team":"red bull","numero":6,"nascita":"2004-09-28"},
    {"nome":"Charles Leclerc","naz":"monegasco","team":"ferrari","numero":16,"nascita":"1997-10-16"},
    {"nome":"Lewis Hamilton","naz":"inglese","team":"ferrari","numero":44,"nascita":"1985-01-07"},
    {"nome":"Carlos Sainz","naz":"spagnolo","team":"williams","numero":55,"nascita":"1994-09-01"},
    {"nome":"Alex Albon","naz":"tailandese","team":"williams","numero":23,"nascita":"1996-03-23"},
    {"nome":"Liam Lawson","naz":"neozelandese","team":"racing bulls","numero":30,"nascita":"2002-02-11"},
    {"nome":"Arvid Lindblad","naz":"inglese","team":"racing bulls","numero":41,"nascita":"2007-08-08"},
    {"nome":"Fernando Alonso","naz":"spagnolo","team":"aston martin","numero":14,"nascita":"1981-07-29"},
    {"nome":"Lance Stroll","naz":"canadese","team":"aston martin","numero":18,"nascita":"1998-10-29"},
    {"nome":"Oliver Bearman","naz":"inglese","team":"haas","numero":87,"nascita":"2005-05-08"},
    {"nome":"Esteban Ocon","naz":"francese","team":"haas","numero":31,"nascita":"1996-09-17"},
    {"nome":"Nico Hulkenberg","naz":"tedesco","team":"audi","numero":27,"nascita":"1987-08-19"},
    {"nome":"Gabriel Bortoleto","naz":"brasiliano","team":"audi","numero":5,"nascita":"2004-10-14"},
    {"nome":"Pierre Gasly","naz":"francese","team":"alpine","numero":10,"nascita":"1996-02-07"},
    {"nome":"Franco Colapinto","naz":"argentino","team":"alpine","numero":43,"nascita":"2003-05-27"},
    {"nome":"Valtteri Bottas","naz":"finlandese","team":"cadillac","numero":77,"nascita":"1989-08-28"},
    {"nome":"Sergio Perez","naz":"messicano","team":"cadillac","numero":11,"nascita":"1990-01-26"}
]

partite_attive = {}

naz_map = {
    "spagna": "spagnolo", "italia": "italiano", "francia": "francese",
    "germania": "tedesco", "brasile": "brasiliano", "argentina": "argentino",
    "messico": "messicano", "finlandia": "finlandese", "uk": "inglese", 
    "inghilterra": "inglese", "monaco": "monegasco", "monegasco": "monegasco",
    "olanda": "olandese", "netherlands": "olandese", "olandese": "olandese"
}

continenti = {
    "europa": ["inglese","italiano","francese","tedesco","spagnolo","olandese","monegasco","finlandese"],
    "america": ["brasiliano","argentino","messicano","canadese"],
    "asia": ["tailandese"],
    "oceania": ["australiano","neozelandese"]
}

# Funzione per calcolare l'età precisa
def calcola_eta(data_nascita_str):
    oggi = date.today()
    nascita = date.fromisoformat(data_nascita_str)
    return oggi.year - nascita.year - ((oggi.month, oggi.day) < (nascita.month, nascita.day))

@client.event
async def on_ready():
    print(f"Bot Online come {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user: return
    if message.channel.id != ID_CANALE: return

    msg = message.content.lower().strip()
    user_id = message.author.id
    tag = message.author.mention

    if "iniziamo" in msg or "partiamo" in msg:
        partite_attive[user_id] = random.choice(piloti)
        await message.channel.send(f"🏁 {tag}, Ho scelto un pilota")
        return

    if user_id not in partite_attive: return

    driver = partite_attive[user_id]
    eta_pilota = calcola_eta(driver["nascita"])
    nome_corretto = driver["nome"].lower()
    cognome_corretto = nome_corretto.split()[-1]

    # --- CONTROLLO NOME/COGNOME ---
    if msg == nome_corretto or msg == cognome_corretto:
        await message.channel.send(f"🏆 {tag} **Ha preso la bandiera a scacchi!** Il pilota era **{driver['nome']}**!🏎️💨")
        del partite_attive[user_id]
        return

    for p in piloti:
        if msg == p["nome"].lower() or msg == p["nome"].lower().split()[-1]:
            await message.channel.send(f"{tag} ❌ No")
            return

    # --- LOGICA ETÀ (>30, <25, età 29) ---
    if ">" in msg or "<" in msg or "età" in msg or "anni" in msg:
        try:
            # Estraiamo il numero dal messaggio
            num_chiesto = int(''.join(filter(str.isdigit, msg)))
            if ">" in msg:
                risultato = eta_pilota > num_chiesto
            elif "<" in msg:
                risultato = eta_pilota < num_chiesto
            else:
                risultato = eta_pilota == num_chiesto
            
            await message.channel.send(f"{tag} {'✅ Sì!' if risultato else '❌ No'}")
            return
        except: pass

    # --- ALTRE DOMANDE (Nazionalità, Team, Numero) ---
    if "paesi bassi" in msg:
        await message.channel.send(f"{tag} {'✅ Sì!' if driver['naz'] == 'olandese' else '❌ No'}")
        return

    for parola in msg.split():
        if parola in naz_map:
            await message.channel.send(f"{tag} {'✅ Sì!' if driver['naz'] == naz_map[parola] else '❌ No'}")
            return

    for c in ["europa", "america", "asia", "oceania", "europeo", "americano", "asiatico", "oceanico"]:
        if c in msg:
            chiave = c.replace("europeo", "europa").replace("americano", "america").replace("asiatico", "asia").replace("oceanico", "oceania")
            await message.channel.send(f"{tag} {'✅ Sì!' if driver['naz'] in continenti.get(chiave, []) else '❌ No'}")
            return

    for team in ["ferrari","red bull","mercedes","mclaren","aston martin","williams","haas","alpine","audi","cadillac","racing bulls"]:
        if team in msg:
            await message.channel.send(f"{tag} {'✅ Sì!' if driver['team'] == team else '❌ No'}")
            return

    if "numero" in msg:
        try:
            num = int(''.join(filter(str.isdigit, msg)))
            await message.channel.send(f"{tag} {'✅ Sì!' if driver['numero'] == num else '❌ No'}")
        except: pass
        return

client.run(TOKEN_BOT)