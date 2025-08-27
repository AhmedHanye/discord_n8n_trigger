import discord
from discord.ext import commands
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
bot = commands.Bot(command_prefix="!", intents=intents)


# * Log when bot is ready
@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


# * Slash command /ask
@bot.tree.command(name="ask", description="Ask a question to the AI")
async def ask_command(interaction: discord.Interaction, question: str):
    """
    Handle /ask slash command
    """
    # * Defer the response to avoid timeout
    await interaction.response.defer()

    # * Get Thread starter message if in a thread
    thread_message = None
    if isinstance(interaction.channel, discord.Thread):
        try:
            thread_message = await interaction.channel.parent.fetch_message(interaction.channel.id)  # type: ignore
        except:
            thread_message = None

    # * Prepare payload
    payload = {
        "username": interaction.user.display_name,
        "content": question,
        "channel": str(interaction.channel.id),  # type: ignore
        "reply_content": None,  # No reply context for slash commands
        "thread_starter_message": thread_message.content if thread_message else None,
    }

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

            # If we got a reply, send it as followup
            if reply_text:
                await interaction.followup.send(reply_text)
            else:
                await interaction.followup.send("No response received.")

        except Exception:
            await interaction.followup.send("Couldn't parse response.")

    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}")


bot.run(DISCORD_TOKEN)
