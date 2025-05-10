import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from fishbot.bot.game_logic import FishingGame

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


# ---- COMMANDS ----


@bot.command()
async def hello(ctx):
    """
    Hi!
    """
    await ctx.send("Hello!")


@bot.command()
async def register(ctx):
    """
    Register to use the habit fishing bot!
    """

    user_id = str(ctx.author.id)
    username = ctx.author.name

    success, message = game.register_user(user_id, username)

    if success:
        embed = discord.Embed(
            title="Welcome to Fish Habit Game",
            description=message,
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="How to play",
            value=(
                "1. Create habits with `!habit add [name]`\n"
                "2. Complete habits daily with `!habit complete [name]`\n"
                "3. Use your fishing attempts with `!catch_fish`\n"
                "4. Build your collection and earn rewards!"
            ),
        )
    else:
        embed = discord.Embed(
            title="Registration issue", description=message, color=discord.Color.red()
        )

    await ctx.send(embed=embed)


@bot.command()
async def inventory(ctx):
    """
    Shows the items in your inventory
    """
    inventory = ", ".join(game.get_inventory())
    await ctx.send(f"Here is your inventory: {inventory}!")


@bot.command()
async def see_pond(ctx):
    """
    Shows current fish in the pond.
    """
    user_id = str(ctx.author.id)
    pond_fish = game.see_pond(user_id)
    pond_fish = ", ".join(pond_fish)
    await ctx.send(f"Here are the fish in the pond: {pond_fish}")


# Command to send a message with the button
@bot.command()
async def catch_fish(ctx):
    """
    Try fishing from the current fish in the pond
    """
    user_id = str(ctx.author.id)
    pond_fish = game.see_pond(user_id)  # Maybe fetch this once
    # Show all fish currently in pond and give the option to fish them
    buttons_info = [str(fish) for fish in pond_fish]
    await ctx.send("Click on of the buttons below:", view=ButtonView(buttons_info))


bot.run(os.getenv("DISCORD_TOKEN"))
