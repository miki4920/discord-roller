import discord
import os

from ErrorHandler import CommandNotExisting, NoDungeonMaster, TooManyDice
from DiceOperations.Roller import DiceRoll
from DowntimeHandler import DowntimeScheduler
from WildMagicHandler import WildMagic
from ReferenceOperations.ReferenceHandler import ReferenceHandler


# Instruction/Manual
link = "https://github.com/miki4920/discord-roller/blob/master/ReadMe.md"
client = discord.Client(activity=discord.CustomActivity("**Roleplaying D&D** | **!help**"))
roller = DiceRoll()
downtime = DowntimeScheduler()
wildmagic = WildMagic()
reference = ReferenceHandler()
token = os.getenv("TOKEN")
test_mode = False
test_server_id = 740700782323826799

code_dictionary = {"h": 0,
                   "r": 1,
                   "pr": 2,
                   "gr": 3,
                   "w": 4,
                   "spell": 5,
                   "monster": 6,
                   "race": 7}

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
        if test_mode and message.guild.id != 740700782323826799:
            return
        elif not test_mode and message.guild.id == 740700782323826799:
            return
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
            if message_code in [5, 6, 7]:
                result_message = reference.reference_item(message.content)
                for return_message in result_message:
                    embedded_message = discord.Embed(title=return_message[0], description=return_message[1], color=10038562)
                    await message.channel.send(embed=embedded_message)
        except Exception as e:
            # Handles all errors
            await message.channel.send(str(e))


client.run(token)
