import os

import discord
from discord.ext import commands

from DiceOperations.Roller import DiceRoll
from ReferenceOperations.ReferenceHandler import ReferenceHandler
from Utility.ErrorHandler import unexpected_error, too_few_arguments, RollerException
from Utility.GetHelp import get_help_messages
from WildMagicHandler import WildMagic

client = discord.Client()
bot = commands.Bot(command_prefix="!")
roller = DiceRoll()
wildmagic = WildMagic()
reference_handler = ReferenceHandler()
token = os.getenv("TOKEN")
test_mode = False
test_server_id = 740700782323826799
test_user_id = 254954838855516164

print(f"Bot running in the {'Test Mode' if test_mode else 'Production Mode'}")

code_dictionary = {("spell",): 4,
                   ("monster",): 5,
                   ("race",): 6,
                   ("class",): 7,
                   ("condition",): 8,
                   ("randstats", "randstat"): 9,
                   }

dm_roles = ["dm", "gm", "game master", "dungeon master"]


@bot.event
async def on_guild_join(guild):
    await guild.system_channel.send("Hi, I am Marduk. Your personal dragon assistant. To tame me, simply type **!help-me**")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='D&D | !help-me'))


def has_valid_arguments(args):
    if len(args) == 0:
        raise too_few_arguments()
    return True


@bot.check
def is_production(context):
    if test_mode:
        if context.guild and context.guild.id != test_server_id:
            return False
        elif not context.guild and context.author.id != test_user_id:
            return False
    elif not test_mode and context.guild and context.guild.id == test_server_id:
        return False
    return True


@bot.command(name="help-me")
async def help_me(context):
    author = context.author.nick if hasattr(context.author, 'nick') else context.author.name
    result_message = get_help_messages()
    if context.guild:
        await context.channel.send("I have delivered secrets of taming me to your PMs.")
    for return_message in result_message:
        embedded_message = discord.Embed(title=return_message[0], description=return_message[1], color=10038562)
        embedded_message.set_author(name=author, icon_url=context.author.avatar_url)
        await context.author.send(embed=embedded_message)


@bot.command(aliases=("r",))
async def roll(context, *args):
    if has_valid_arguments(args):
        args = " ".join(args)
    result, dice_rolls = roller.roll_dice(args)
    result_message = f"{context.author.mention}\n**Roll**: {args}\n**Total: **{result}\n**Results**: {dice_rolls}"
    await context.send(result_message)


@bot.command()
async def wild(context):
    result_roll = roller.roll_dice("1d100")[0]
    result_message = f"{context.author.mention}\nYour wild magic surge is:\n" + wildmagic.determine_wild_magic(
        result_roll)
    await context.channel.send(result_message)


@bot.command()
async def chaos(context):
    result_roll = roller.roll_dice("1d10000")[0]
    result_message = f"{context.author.mention}\nYour random magical effect is:\n" + wildmagic.determine_surge_magic(
        result_roll)
    await context.channel.send(result_message)


async def reference(context, item_type, args):
    author = context.author.nick if hasattr(context.author, 'nick') else context.author.name
    if has_valid_arguments(args):
        args = " ".join(args)
    result_message = reference_handler.reference_item(item_type, args)
    for return_message in result_message:
        embedded_message = discord.Embed(title=return_message[0], description=return_message[1], color=10038562)
        embedded_message.set_author(name=author, icon_url=context.author.avatar_url)
        await context.channel.send(embed=embedded_message)


@bot.command()
async def spell(context, *args):
    await reference(context, "spell", args)


@bot.command()
async def monster(context, *args):
    await reference(context, "monster", args)


@bot.command(name="class")
async def dnd_class(context, *args):
    await reference(context, "class", args)


@bot.command()
async def condition(context, *args):
    await reference(context, "condition", args)


@bot.command(aliases=("randstats",))
async def randstat(context, *args):
    if len(args) > 0:
        args = " ".join(args)
    else:
        args = "4d6kh3"
    return_message = ""
    total = 0
    for _ in range(0, 6):
        result, dice_rolls = roller.roll_dice(args)
        return_message += f"{args} {dice_rolls}: {result}\n"
        total += result
    return_message += f"Total: {total}"
    return_message = context.author.mention + "```" + "\nRandomly Generated Statistics:\n" + return_message + "```"
    await context.channel.send(return_message)


@roll.error
@help_me.error
@wild.error
@chaos.error
@spell.error
@monster.error
@dnd_class.error
@condition.error
@randstat.error
async def marduk_error(context, error):
    if test_mode:
        raise error
    if isinstance(error.original, RollerException):
        await context.channel.send(str(error.original))
    else:
        error = unexpected_error(str(error.original))
        await context.channel.send(error)


bot.run(token)

