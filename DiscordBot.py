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
    server_members = message.guild.members
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        message_start = message.content[0:3]
        message_content = message.content[3:]
        result, dice_rolls = roller.roll_dice(message_content)
        if "gr" in message_start:
            for member in server_members:
                for role in member.roles:
                    if role.name == "GM":
                        await member.send(f"{result}\n"
                                          f"Details: {message_content} {dice_rolls}")
                        break
            else:
                await message.channel.send("There is nobody who has a rank of 'GM' on your server")
        elif "pr" in message_content:
            await message.author.send(f"{result}\n"
                                      f"Details: {message_content} {dice_rolls}")
        elif "r" in message_content:

            await message.channel.send(f"{result}\n"
                                       f"Details: {message_content} {dice_rolls}")


client.run(token)
