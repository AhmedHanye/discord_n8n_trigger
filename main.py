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


# * Log when bot is ready
@client.event
async def on_ready() -> None:
    print(f"Logged in as {client.user}")


# * Response to each message
@client.event
async def on_message(message) -> None:
    """
        # ! Ignore messages:
            - it must be the default message (normal user messages)
            - From bots
            - one of these values empty (author - content)
    """
    if (
        message.type != discord.MessageType.default
        or getattr(message.author, "bot", False)
        or not message.author
        or not message.content
    ):
        return

    # * Get reply message content if it exists
    reply_content = None
    if message.reference and message.reference.message_id:
        try:
            replied_message = await message.channel.fetch_message(
                message.reference.message_id
            )
            reply_content = replied_message.content or ""
        except:
            reply_content = None

    # * Get Thread starter message if it exists
    thread_message = None
    if isinstance(message.channel, discord.Thread):
        try:
            thread_message = await message.channel.parent.fetch_message(message.channel.id)  # type: ignore
        except:
            thread_message = None

    # * Prepare payload
    payload = {
        "username": message.author.display_name,
        "content": message.content or "",
        "channel": str(message.channel.id),
        "reply_content": reply_content,
        "thread_starter_message": thread_message.content if thread_message else None,
        "attachments": (
            [att.url for att in message.attachments] if message.attachments else []
        ),
    }

    # * Show typing indicator while waiting for webhook
    async with message.channel.typing():
        # * Send payload to n8n webhook
        try:
            response = requests.post(
                N8N_WEBHOOK_URL,
                json=payload,
                auth=(
                    (N8N_BASIC_AUTH_USER, N8N_BASIC_AUTH_PASSWORD)
                    if N8N_BASIC_AUTH_USER and N8N_BASIC_AUTH_PASSWORD
                    else None
                ),
                timeout=10,  # avoid hanging
            )

            # * Get reply text from JSON response
            try:
                reply_text = response.json()[0]["reply"]

                # If we got a reply, send it back to Discord
                if reply_text:
                    await message.channel.send(reply_text)

            except Exception:
                await message.channel.send("Couldn't parse response.")

        except Exception as e:
            await message.channel.send(f"Error: {str(e)}")


client.run(DISCORD_TOKEN)
