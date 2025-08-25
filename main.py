import discord
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load from env
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") or ""
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL") or ""

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    payload = {
        "username": str(message.author),
        "content": message.content,
        "channel": str(message.channel),
        "server": str(message.guild)
    }

    # Send to n8n webhook
    try:
        requests.post(N8N_WEBHOOK_URL, json=payload)
    except Exception as e:
        print("Error sending to n8n:", e)

client.run(DISCORD_TOKEN)
