import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from game_logic import FishingGame

load_dotenv()

description = "This is a little fishing game designed to help and motivate you to form and keep habits."

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # This is used to access user information

bot = commands.Bot(command_prefix="!", description=description, intents=intents)

game = FishingGame()

POND_SIZE = 3

# ---- VIEWS ----


# Create a view with a button
class ButtonView(discord.ui.View):
    def __init__(self, buttons_info: list):
        super().__init__()
        self.buttons_info = buttons_info

        for label in self.buttons_info:
            # Create the button dynamically
            button = discord.ui.Button(label=label, style=discord.ButtonStyle.primary)
            button.callback = self.create_button_callback(label)
            self.add_item(button)

    def create_button_callback(self, label: str):
        # Using nested functions, we don't need to create a new function for each button
        async def button_callback(interaction: discord.Interaction):
            fish_caught = game.catch_fish(label)
            if fish_caught:
                response = f"You caught a {label}"
                await interaction.response.edit_message(content=response, view=None)
            else:
                response = "It got away"
                await interaction.response.edit_message(content=response, view=None)

        return button_callback


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    # SPAWN FISH WHEN LOADING THE BOT. This will change when considering multiple users
    game.spawn_fish(POND_SIZE)


# ---- COMMANDS ----


@bot.command()
async def hello(ctx):
    """
    Hi!
    """
    await ctx.send("Hello!")


@bot.command()
async def inventory(ctx):
    """
    Shows the items in your inventory"
    """
    inventory = ", ".join(game.get_inventory())
    await ctx.send(f"Here is your inventory: {inventory}!")


@bot.command()
async def see_pond(ctx):
    """
    Shows current fish in the pond.
    """
    pond_fish = ", ".join(game.see_pond())
    await ctx.send(f"Here are the fish in the pond: {pond_fish}")


# Command to send a message with the button
@bot.command()
async def catch_fish(ctx):
    """
    Try fishing from the current fish in the pond
    """
    pond_fish = game.see_pond()  # Maybe fetch this once
    # Show all fish currently in pond and give the option to fish them
    buttons_info = [str(fish) for fish in pond_fish]
    await ctx.send("Click on of the buttons below:", view=ButtonView(buttons_info))


bot.run(os.getenv("DISCORD_TOKEN"))
