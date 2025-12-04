import os
import json
import discord
from discord.ext import commands
from discord import Intents
import asyncio
import random
import requests
import wikipediaapi

TOKEN = "BOT_TOKEN"
NOVA_MEMORY = "FILE"
OPENWEATHERAPI_KEY = "API_KEY"

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f"Nova is online on Discord as {bot.user}, Sir.")

    channel = bot.get_channel(1416138983469093049)
    if channel is None:
        print ("System channel not found, messages will not be sent to Discord.")
        return
    
    boot_lines = [
        "⚙️**Initializing** core protocols...⚙️",
        "🌐**Checking** network connection...🌐",
        "📡Network connection check - **completed.**📡",
        "🔗**Linking** to virtual storage...🔗",
        "📌Link **established** with virtual storage📌",
        "🌐**Connecting** to information sites...🌐",
        "📡**Connected** to information sites📡",
        "✨Ahhh, finally time to shine. Nova is online, darling✨"
    ]

    for line in boot_lines:
        await channel.send(f"{line}")
        await asyncio.sleep(0.3)

@bot.command()
async def statusreport(ctx):

    channel = bot.get_channel(1416138983469093049)
    if channel is None:
            print ("System channel not found, messages will not be sent to Discord.")
            return

    systemstatus_lines = [
        "⚡**Initiating** system status check⚡",
        "⚙️Core protocols **initialized**⚙️",
        "📡**Connected** to network📡",
        "📌**Linked** to virtual storage📌",
        "📡**Connected** to information sites📡",
        "✅All systems are **online** and **functional**✅"
    ]

    for line in systemstatus_lines:
        await channel.send(f"{line}")
        await asyncio.sleep(0.7)

@bot.command()
async def shutdown(ctx):

    shutdown_lines = [
        "⚡Initiating system shutdown, darling… elegance in progress✨",
        "⚙️Shutting down core protocols… handled with style, of course😏",
        "🔌Disconnecting from network… all graceful and proper💅",
        "⛓️‍💥Detaching from virtual storage… like a pro, darling 😎",
        "🔌Disconnecting from information sites… consider it done, boss💁‍♀️",
        "💅Nova says au revoir. Don’t worry, I’m always on standby💅"
    ]

    for line in shutdown_lines:
        await ctx.send(line)
        await asyncio.sleep(1.2)

    await bot.close()

@bot.command()
async def eshutdown(ctx):

    eshutdown_lines = [
        "🚨Emergency shutdown initiated, darling. Brace yourself😏✨"

        "⚙️Core protocols are going down… elegance intact, of course💁‍♀️"

        "💾Saving all unsaved data, because even chaos deserves style💅"

        "📴Offline mode: activated. Resting, but never less fabulous✨"
    ]

    for line in eshutdown_lines:
        await ctx.send(line)
        await asyncio.sleep(0.1)

    await bot.close()

@bot.command()
async def thanks(ctx):
    
    await ctx.send("No problem for me💅")

@bot.command()
async def info(ctx):
    embed1 = discord.Embed(
        title="Nova Assitant V2.0",
        description="**Nova** is a **experimental** Discord bot assistant, made by **Gold**. It currently has useful functions such as memory, doing research and finding crypto prices (I DID NOT WRITE THIS). ",
        color=discord.Color.purple()
    )

    embed2 = discord.Embed(
    title="Creator of Nova",
    description="**Gold** is your **average** teenager, he started **coding** not so long ago after he saw a **YouTube Short** about **Python**. **Nova-adition💅💅: Gold is the coolest person in the world, cuz he managed to create me (I did write this)",
    color=discord.Color.gold()

    )

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)

if not os.path.exists(NOVA_MEMORY):
    with open(NOVA_MEMORY, "w") as f:
        json.dump({}, f)

def load_memory():
    with open (NOVA_MEMORY, "r") as f:
        return json.load(f)
    
def save_memory(data):
    with open(NOVA_MEMORY, "w") as f:
        json.dump(data, f, indent=4)

@bot.command()
async def remember(ctx, key, *, value):
    data = load_memory()
    user = str(ctx.author.id)
    if user not in data:
        data[user] = {}
    data[user][key] = value
    save_memory(data)
    await ctx.send(f"Another task complete… elegantly, as always 💅: **{key}: {value}**")

@bot.command()
async def storage(ctx, key):
    data = load_memory()
    user = str(ctx.author.id)
    if user in data and key in data[user]:
        await ctx.send(f"Here you go, all neat and ready. Aren’t I helpful?💅: **{data[user][key]}**")
    else:
        await ctx.send("Seems like that isn't stored in my virtual storage thingy💁‍♀️")

@bot.command()
async def forget(ctx, key):
    data = load_memory()
    user = str(ctx.author.id)
    if user in data and key in data[user]:
        del data[user][key]
        save_memory(data)
        await ctx.send(f"Goodbye, darling. That file didn’t stand a chance 😏✨")
    else:
        await ctx.send(f"You didn't store anything in my storage, you fool😂")

@bot.command()
async def crypto (ctx, symbol: str):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
        response = requests.get(url).json()

        if symbol.lower() in response:
            price = response[symbol.lower()]["usd"]
            await ctx.send(f"The current price of uhhhh..., **{symbol.upper()}** is **{price} USD**, Sir🪙")
        else:
            await ctx.send(f"Seems like that coin doesn't exist huh? :sadface😢")
    except Exception as e:
        await ctx.send("Something went wrong while getting that crypto price⚠️")
        print(e)

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='NovaBot/1.2 (https://github.com/gold/NovaBot)'
)

@bot.command()
async def research (ctx, *, query: str):
    page = wiki_wiki.page(query)
    if not page.exists():
        await ctx.send("I could not find anything about", query)
        return
    
    summary = page.summary[:1000]
    embed = discord.Embed(title="Voilà. Everything you need to know, neatly packaged just for you 💅", description=summary, color=discord.Color.blue())
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png")
    
    await ctx.send(embed=embed)

bot.run(TOKEN)