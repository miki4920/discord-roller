import discord
import os
from Roller import DiceRoll

client = discord.Client()
roller = DiceRoll()

token = os.getenv("TOKEN")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!r'):
        message_content = message.content[2:]
        result, dice_rolls = roller.roll_dice(message_content)
        await message.channel.send(f"{result}\n"
                                   f"Details: {message_content} {dice_rolls}")
    elif message.content.startswith('!gr'):
        message_content = message.content[3:]
        result, dice_rolls = roller.roll_dice(message_content)
        await message.author.send(f"{result}\n"
                                   f"Details: {message_content} {dice_rolls}")
client.run(token)
