import discord
import os
from ErrorHandler import CommandNotExisting, NoDungeonMaster, TooManyDice
from Roller import DiceRoll
# Instruction/Manual
link = "https://github.com/miki4920/discord-roller/blob/master/ReadMe.md"
client = discord.Client()
roller = DiceRoll()
token=os.getenv("TOKEN")

code_dictionary = {"h": 0,
                   "r": 1,
                   "pr": 2,
                   "gr": 3,
                   "dt": 4}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # Prevents Bot's Recursion
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        message.content = message.content.lower()
        try:
            # Checks the code dictionary for the role type
            message_code = code_dictionary.get(message.content[1:3].replace(" ", ""))
            if message_code is None:
                raise CommandNotExisting(message.content)
            # Sends Manual
            if message_code == 0:
                await message.author.send(f"The instruction manual is located here: {link}")
            # Part for dice handling
            if message_code in [1, 2, 3]:
                # Gets the dice roll from the roller then checks whether the message doesn't exceed the maximum capacity
                result, dice_rolls = roller.roll_dice(message.content[3:])
                if len(str(result)+dice_rolls) >= 1900:
                    raise TooManyDice(message.content)
                # Determines the message to be sent, cuts out the command
                return_message = f"{result}\nDetails: {message.content[3:]}\n{dice_rolls}"
                # Normal Roll
                if message_code == 1:
                    await message.channel.send(return_message)
                # Private Roll, sends the message to author
                elif message_code == 2:
                    await message.author.send(return_message)
                    await message.delete()
                # DM roll, sends the message to someone with "DM" role
                elif message_code == 3:
                    server_members = message.guild.members
                    await message.delete()
                    for member in server_members:
                        for role in member.roles:
                            if role.name == "DM":
                                await member.send(f"The message was sent by {str(message.nick).split('#')[0]}:\n"
                                                  + return_message)
                                await message.author.send("Your roll has been sent:\n" + return_message)
                                return
                    else:
                        # If no DM in the server, sends an error message
                        raise NoDungeonMaster()
            if message_code == 4:
                day = message.content[3:]
                if day == "":
                    await message.delete()
                else:
                    await message.channel.send()
        except Exception as e:
            # Handles all errors
            await message.channel.send(str(e))


client.run(token)
