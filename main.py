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
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if message is a reply
    reply_content = None
    if message.reference and message.reference.message_id:
        try:
            replied_message = await message.channel.fetch_message(
                message.reference.message_id
            )
            reply_content = replied_message.content or ""
        except:
            reply_content = None

    payload = {
        "username": str(message.author),
        "content": message.content or "",
        "channel": str(message.channel.id),
        "reply_content": reply_content,
        "attachments": (
            [att.url for att in message.attachments] if message.attachments else []
        ),
    }

    # Send to n8n webhook
    try:
        requests.post(N8N_WEBHOOK_URL, json=payload)
    except Exception as e:
        print("Error sending to n8n:", e)


client.run(DISCORD_TOKEN)
