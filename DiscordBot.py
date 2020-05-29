import discord
import os
from Roller import DiceRoll

link = "https://github.com/miki4920/discord-roller/blob/master/ReadMe.md"
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
    server_members = message.guild.members
    if message.content.startswith('!'):
        message_start = message.content[0:3].lower()
        message_content = message.content[3:]
        if "h" in message_start:
            await message.author.send(f"The manual is located here: {link}")
        result, dice_rolls = roller.roll_dice(message_content)
        if "gr" in message_start:
            for member in server_members:
                for role in member.roles:
                    if role.name == "DM":
                        await member.send(f"{result}\n"
                                          f"Details: {message_content} {dice_rolls}")
                        return
            else:
                await message.channel.send("There is nobody who has a rank of 'DM' on your server")
        elif "pr" in message_start:
            await message.author.send(f"{result}\n"
                                      f"Details: {message_content} {dice_rolls}")
        elif "r" in message_start:
            await message.channel.send(f"{result}\n"
                                       f"Details: {message_content} {dice_rolls}")
        elif "h" in message_start:
            await message.channel.send("Help is in progress!")


client.run(token)
