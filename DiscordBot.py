import discord
import os
from Utility.GetHelp import get_help_messages
from Utility.ErrorHandler import command_not_existing, unexpected_error, too_many_dice, RollerException
from DiceOperations.Roller import DiceRoll
from WildMagicHandler import WildMagic
from ReferenceOperations.ReferenceHandler import ReferenceHandler


client = discord.Client()
roller = DiceRoll()
wildmagic = WildMagic()
reference = ReferenceHandler()
token = os.getenv("TOKEN")
test_mode = False
test_server_id = 740700782323826799

print(f"Bot running in the {'Test Mode' if test_mode else 'Production Mode'}")

code_dictionary = {("help", "h"): 0,
                   ("roll", "r"): 1,
                   ("wild", "w"): 2,
                   ("spell", "s"): 3,
                   ("monster", "m"): 4,
                   ("race", "r"): 5,
                   ("class", "c"): 6,
                   ("condition",): 7,
                   ("randstats",): 8}

dm_roles = ["dm", "gm", "game master", "dungeon master"]


@client.event
async def on_guild_join(guild):
    await guild.system_channel.send("Hi, I am Marduk. Your personal dragon assistant. To tame me, simply type **!help**")


@client.event
async def on_ready():
    print("Number of Servers the bot is in: ", len(list(client.guilds)))
    await client.change_presence(activity=discord.Game(name='D&D | !help'))


@client.event
async def on_message(message):
    original_message = message.content
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
            message_code = message.content.split(" ")[0][1:]
            for list_of_keys in code_dictionary:
                if message_code in list_of_keys:
                    message_code = code_dictionary[list_of_keys]
                    break
            else:
                message_code = None
            if message_code is None:
                raise command_not_existing()
            # Sends Manual
            if message_code == 0:
                result_message = get_help_messages()
                await message.channel.send("I have delivered secrets of taming me to your PMs.")
                for return_message in result_message:
                    embedded_message = discord.Embed(title=return_message[0], description=return_message[1], color=10038562)
                    embedded_message.set_author(name=message.author.nick, icon_url=message.author.avatar_url)
                    await message.author.send(embed=embedded_message)
            # Part for dice handling
            if message_code == 1:
                # Gets the dice roll from the roller then checks whether the message doesn't exceed the maximum capacity
                roll_message = " ".join(message.content.split(" ")[1:])
                result, dice_rolls = roller.roll_dice(roll_message)
                if len(str(result) + dice_rolls) >= 1900:
                    raise too_many_dice()
                # Determines the message to be sent, cuts out the command
                result_message = f"{message.author.mention}\n**Roll**: {roll_message}\n**Total: **{result}\n**Results**: {dice_rolls}"
                # Normal Roll
                if message_code == 1:
                    await message.channel.send(result_message)
            if message_code == 2:
                result_roll = roller.roll_dice("1d100")[0]
                result_message = f"{message.author.mention}\nYour wild magic surge is:\n" + wildmagic.determine_wild_magic(result_roll)
                await message.channel.send(result_message)
            if message_code in [3, 4, 5, 6, 7]:
                result_message = reference.reference_item(message.content)
                for return_message in result_message:
                    embedded_message = discord.Embed(title=return_message[0], description=return_message[1], color=10038562)
                    embedded_message.set_author(name=message.author.nick, icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embedded_message)
            if message_code == 8:
                roll_message = " ".join(message.content.split(" ")[1:])
                if roll_message == "":
                    roll_message = "4d6kh3"
                return_message = ""
                total = 0
                for _ in range(0, 6):
                    result, dice_rolls = roller.roll_dice(roll_message)
                    return_message += f"{roll_message} {dice_rolls}: {result}\n"
                    total += result
                return_message += f"Total: {total}"
                return_message = message.author.mention + "\nRandomly Generated Statistics:\n" + "```" + return_message + "```"
                if len(return_message) >= 1900:
                    raise too_many_dice()
                await message.channel.send(return_message)
        except Exception as e:
            # Handles all errors
            if not isinstance(e, RollerException):
                e = unexpected_error(str(e))
            e.command = original_message
            await message.channel.send(str(e))
            if test_mode:
                raise e


client.run(token)

