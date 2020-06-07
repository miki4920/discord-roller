import discord
import os
from ErrorHandler import CommandNotExisting, NoDungeonMaster
from Roller import DiceRoll

link = "https://github.com/miki4920/discord-roller/blob/master/ReadMe.md"
client = discord.Client()
roller = DiceRoll()
token = os.getenv("TOKEN")

code_dictionary = {"h": 0,
                   "r": 1,
                   "pr": 2,
                   "gr": 3}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        message.content = message.content.lower()
        try:
            message_code = code_dictionary.get(message.content[1:3].replace(" ", ""))
            if message_code is None:
                raise CommandNotExisting(message.content)
            if message_code == 0:
                await message.author.send(f"The instruction manual is located here: {link}")
            if message_code > 0:
                result, dice_rolls = roller.roll_dice(message.content[3:])
                return_message = f"{result}\nDetails: {message.content[3:]}\n{dice_rolls}"
                if message_code == 1:
                    await message.channel.send(return_message)
                elif message_code == 2:
                    await message.author.send(return_message)
                elif message_code == 3:
                    server_members = message.guild.members
                    for member in server_members:
                        for role in member.roles:
                            if role.name == "DM":
                                await member.send(return_message)
                                return
                    else:
                        raise NoDungeonMaster()
        except Exception as e:
            await message.channel.send(str(e))


client.run(token)
