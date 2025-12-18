import discord
import random
import difflib
from discord.ext import commands
import re
import json


with open("responses.json", "r", encoding="utf-8") as f:
   responses = json.load(f)

def save_responses():
    """Save current responses back to JSON file."""
    with open("responses.json", "w", encoding="utf-8") as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)

def fuzzy_match(input_text, options, threshold=0.7):
    match = difflib.get_close_matches(input_text, options, n=1, cutoff=threshold)
    return match[0] if match else None


# Setup intents correctly
intents = discord.Intents.default()
intents.message_content = True  # REQUIRED to read user messages

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)



# Learn command
# ---------------------------
@bot.command()
async def learn(ctx, trigger: str, *, new_response: str):
    print(" learn invoked with:", trigger, "|", new_response) 
    trigger = trigger.lower()  # Normalize trigger to lowercase

    if trigger in responses:
        responses[trigger].append(new_response)
        await ctx.send(f" Learned a new response for **{trigger}**!")
    else:
        responses[trigger] = [new_response]
        await ctx.send(f" Added a new trigger: **{trigger}**!")

    save_responses()  # Save to JSON for persistence


# When bot is ready
@bot.event
async def on_ready():
    print(f" Logged in as {bot.user}")

# Command: !greet NAME
@bot.command()
async def greet(ctx, name: str):
    await ctx.send(f"Hey {name}, welcome!")

# Command: !ping
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Respond to natural messages
@bot.event
async def on_message(message):
    if message.author.bot:
        return


    msg = message.content.lower().strip()
    msg = re.sub(r'[^a-z\s]', '', msg)  # remove punctuation, keep letters and spaces

# Fuzzy match against keys in JSON
    matched_key = fuzzy_match(msg, responses.keys())
    if matched_key:
        reply = random.choice(responses[matched_key])
        await message.channel.send(
            f"{reply} "
            f"{message.author.display_name if matched_key in ['hello','hi','hey'] else ''}"
        .strip()
        )



# Must include this so commands still work!
    await bot.process_commands(message)




bot.run("")