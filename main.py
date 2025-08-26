import discord
import requests
import os
from dotenv import load_dotenv

# * Load environment variables from .env file
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") or ""
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL") or ""
N8N_BASIC_AUTH_USER = os.getenv("N8N_BASIC_AUTH_USER") or ""
N8N_BASIC_AUTH_PASSWORD = os.getenv("N8N_BASIC_AUTH_PASSWORD") or ""

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None:
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message) -> None:
    # ! Ignore messages not from the specified user or any bots
    if getattr(message.author, "bot", False):
        return

    # * Check if message is a reply
    reply_content = None
    if message.reference and message.reference.message_id:
        try:
            replied_message = await message.channel.fetch_message(
                message.reference.message_id
            )
            reply_content = replied_message.content or ""
        except:
            reply_content = None

    # * Thread starter message
    thread_message = None
    if isinstance(message.channel, discord.Thread):
        thread_message = await message.channel.parent.fetch_message(message.channel.id)  # type: ignore

    payload = {
        "username": str(message.author),
        "content": message.content or "",
        "channel": str(message.channel.id),
        "reply_content": reply_content,
        "thread_starter_message": thread_message.content if thread_message else None,
        "attachments": (
            [att.url for att in message.attachments] if message.attachments else []
        ),
    }

    # * Send to n8n webhook
    try:
        requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            auth=(
                (N8N_BASIC_AUTH_USER, N8N_BASIC_AUTH_PASSWORD)
                if N8N_BASIC_AUTH_USER and N8N_BASIC_AUTH_PASSWORD
                else None
            ),
        )
    except Exception as e:
        print("Error sending to n8n:", e)


client.run(DISCORD_TOKEN)
