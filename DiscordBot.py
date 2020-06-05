import discord
import os
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
        message_start = message.content[1:3].replace(" ", "")
        try:
            message_code = code_dictionary[message_start]
        except KeyError:
            await message.channel.send(f"The command you are trying to use does not exist.\n"
                                       f"Please type '!h' for further information.")
            return
        if message_code == 0:
            await message.author.send(f"The manual is located here: {link}")
        if message_code > 0:
            try:
                result, dice_rolls = roller.roll_dice(message.content[3:])
                return_message = f"{result}\nDetails: {message.content[3:]}\n{dice_rolls}"
            except ValueError:
                await message.channel.send(f"The command you tried to use: '{message.content}' is incorrect.\n"
                                           f"Please type '!h' for further information.")
                return
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
                    await message.channel.send("There is nobody who has a rank of 'DM' on your server.")


client.run(token)
