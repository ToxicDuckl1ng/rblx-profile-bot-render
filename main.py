import os
import json
import asyncio
from flask import Flask
import discord
from discord.ext import commands
from threading import Thread

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Flask App is running!"

# Discord bot setup
TOKEN = os.environ.get('TOKEN_BOT')
ROBLOSECURITY_TOKEN = os.environ.get('ROBLOSECURITY_TOKEN')

if not TOKEN:
    raise ValueError("Discord bot token not found. Please set TOKEN_BOT in the environment variables.")
if not ROBLOSECURITY_TOKEN:
    raise ValueError("Roblosecurity token not found. Please set ROBLOSECURITY_TOKEN in the environment variables.")

HEADERS = {'Cookie': f'.ROBLOSECURITY={ROBLOSECURITY_TOKEN}'}

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="ping", description="Responds with Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# Run the Flask app in a separate thread
def run_flask():
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    print(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, threaded=True)

# Run both Flask and Discord bot concurrently
async def start_bot():
    # Start the Flask app in a separate thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Run the Discord bot
    await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except Exception as e:
        print(f"Error running the bot: {e}")
