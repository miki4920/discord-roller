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
test_user_id = 254954838855516164

print(f"Bot running in the {'Test Mode' if test_mode else 'Production Mode'}")

code_dictionary = {("help-me", "h"): 0,
                   ("roll", "r"): 1,
                   ("wild", "w"): 2,
                   ("chaos",): 3,
                   ("spell", "s"): 4,
                   ("monster", "m"): 5,
                   ("race", "r"): 6,
                   ("class", "c"): 7,
                   ("condition",): 8,
                   ("randstats", "randstat"): 9,
                   }

dm_roles = ["dm", "gm", "game master", "dungeon master"]


@client.event
async def on_guild_join(guild):
    await guild.system_channel.send("Hi, I am Marduk. Your personal dragon assistant. To tame me, simply type **!help-me**")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='D&D | !help-me'))


@client.event
async def on_message(message):
    original_message = message.content
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        message.content = message.content.lower()
        if test_mode:
            if message.guild and message.guild.id != test_server_id:
                return
            elif not message.guild and message.author.id != test_user_id:
                return
        elif not test_mode and message.guild and message.guild.id == test_server_id:
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
            # Sends Manual
            author = message.author.nick if hasattr(message.author, 'nick') else message.author.name
            if message_code == 0:
                result_message = get_help_messages()
                if message.guild:
                    await message.channel.send("I have delivered secrets of taming me to your PMs.")
                for return_message in result_message:
                    embedded_message = discord.Embed(title=return_message[0], description=return_message[1], color=10038562)
                    embedded_message.set_author(name=author, icon_url=message.author.avatar_url)
                    await message.author.send(embed=embedded_message)
            elif message_code == 1:
                roll_message = " ".join(message.content.split(" ")[1:])
                result, dice_rolls = roller.roll_dice(roll_message)
                result_message = f"{message.author.mention}\n**Roll**: {roll_message}\n**Total: **{result}\n**Results**: {dice_rolls}"
                if message_code == 1:
                    await message.channel.send(result_message)
            elif message_code in [2, 3]:
                if message_code == 2:
                    result_roll = roller.roll_dice("1d100")[0]
                    result_message = f"{message.author.mention}\nYour wild magic surge is:\n" + wildmagic.determine_wild_magic(result_roll)
                else:
                    result_roll = roller.roll_dice("1d10000")[0]
                    result_message = f"{message.author.mention}\nYour random magical effect is:\n" + wildmagic.determine_surge_magic(
                        result_roll)
                await message.channel.send(result_message)
            elif message_code in [4, 5, 6, 7, 8]:
                result_message = reference.reference_item(message.content)
                for return_message in result_message:
                    embedded_message = discord.Embed(title=return_message[0], description=return_message[1], color=10038562)
                    embedded_message.set_author(name=author, icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embedded_message)
            elif message_code == 9:
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

