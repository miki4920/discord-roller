import discord
import os
from ErrorHandler import CommandNotExisting, NoDungeonMaster, TooManyDice
from Roller import DiceRoll
from DowntimeHandler import DowntimeScheduler
from WildMagicHandler import WildMagic
from ReferenceHandler import ReferenceHandler

# Instruction/Manual
link = "https://github.com/miki4920/discord-roller/blob/master/ReadMe.md"
api = "https://www.dnd5eapi.co/api/"
client = discord.Client()
roller = DiceRoll()
downtime = DowntimeScheduler()
wildmagic = WildMagic()
reference = ReferenceHandler(api)
token=os.getenv("TOKEN")


code_dictionary = {"h": 0,
                   "r": 1,
                   "pr": 2,
                   "gr": 3,
                   "w": 4,
                   "spell": 5,
                   "monster": 6}

dm_roles = ["dm", "gm", "game master", "dungeon master"]

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
            message_code = code_dictionary.get(message.content.split(" ")[0][1:])
            if message_code is None:
                raise CommandNotExisting(message.content)
            # Sends Manual
            if message_code == 0:
                await message.author.send(f"The instruction manual is located here: {link}")
            # Part for dice handling
            if message_code in [1, 2, 3]:
                if message_code in [2, 3]:
                    await message.delete()
                # Gets the dice roll from the roller then checks whether the message doesn't exceed the maximum capacity
                result, dice_rolls = roller.roll_dice(message.content[3:])
                if len(str(result) + dice_rolls) >= 1900:
                    raise TooManyDice(message.content)
                # Determines the message to be sent, cuts out the command
                result_message = f"{message.author.mention}\n**Roll**: {message.content[3:]}\n**Total: **{result}\n**Results**: {dice_rolls}"
                # Normal Roll
                if message_code == 1:
                    await message.channel.send(result_message)
                # Private Roll, sends the message to author
                elif message_code == 2:
                    await message.author.send(result_message)
                # DM roll, sends the message to someone with "DM" role
                elif message_code == 3:
                    server_members = message.guild.members
                    for member in server_members:
                        for role in member.roles:
                            if role.name in dm_roles:
                                await message.author.send(result_message)
                                if role not in message.author.roles:
                                    await member.send(
                                        f"The message was sent by {str(message.author.nick).split('#')[0]}:\n"
                                        + result_message)
                                return
                    else:
                        # If no DM in the server, sends an error message
                        raise NoDungeonMaster()
            if message_code == 4:
                result_roll = roller.roll_dice("1d100")[0]
                result_message = f"Your wild magic surge is:\n" + wildmagic.determine_wild_magic(result_roll)
                await message.channel.send(result_message)
            if message_code == 5:
                result_message = reference.reference_spell(message.content)
                if type(result_message) == tuple:
                    embeded_spell = discord.Embed(title=result_message[0], description=result_message[1])
                    await message.channel.send(embed=embeded_spell)
                else:
                    await message.channel.send(result_message)
            if message_code == 6:
                result_message = reference.reference_monster(message.content)
                if type(result_message) == tuple:
                    embeded_monster = discord.Embed(title=result_message[0], description=result_message[1])
                    await message.channel.send(embed=embeded_monster)
                else:
                    await message.channel.send(result_message)
        except Exception as e:
            # Handles all errors
            await message.channel.send(str(e))


client.run(token)
