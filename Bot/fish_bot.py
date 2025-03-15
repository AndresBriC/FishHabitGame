import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from game_logic import FishingGame

load_dotenv()

description = "This is a little fishing game designed to help and motivate you to form and keep habits."

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)

game = FishingGame()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    # SPAWN FISH WHEN LOADING THE BOT
    game.spawn_fish(3)


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


@bot.command()
async def fish(ctx):
    caught_fish = game.catch_fish()
    await ctx.send(f"You caught a {caught_fish}!")


@bot.command()
async def inventory(ctx):
    inventory = game.get_inventory()
    await ctx.send(f"Here is your inventory: {inventory}!")


@bot.command()
async def see_pond(ctx):
    pond_fish = game.see_pond()
    await ctx.send(f"Here are the fish in the pond: {pond_fish}")


bot.run(os.getenv("DISCORD_TOKEN"))
