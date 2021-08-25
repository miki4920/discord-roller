import os

import discord

from discord import Guild
from discord.ext import commands
from discord.ext.commands import Context
from functools import wraps
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from typing import Tuple, Callable, Coroutine, Union

from DiceOperations.Roller import DiceRoll
from ReferenceOperations.ReferenceHandler import ReferenceHandler
from Utility.ErrorHandler import UnexpectedError, TooFewArguments, RollerException
from Utility.GetHelp import get_help_messages
from WildMagicHandler import WildMagic

bot = commands.Bot(command_prefix="!")
bot.help_command = None
slash = SlashCommand(bot, sync_commands=True)
roller = DiceRoll()
wildmagic = WildMagic()
reference_handler = ReferenceHandler()
token = os.getenv("TOKEN")
test_mode = False
test_server_id = 740700782323826799
test_user_id = 254954838855516164

print(f"Bot running in the {'Test Mode' if test_mode else 'Production Mode'}")


def is_production(context: Context) -> bool:
    """Checks if bot is currently in testing environment or production environment.
    Prevents double posting when bot is being developed."""
    if test_mode:
        if context.guild and context.guild.id != test_server_id:
            return False
        elif not context.guild and context.author.id != test_user_id:
            return False
    elif not test_mode and context.guild and context.guild.id == test_server_id:
        return False
    return True


def error_handler(coro: Callable):
    """A decorator used handling errors.
    :param coro: A Discord Command or Discord Slash Command function.
    :return: Function wrapped with argument and error handling.
    """
    @wraps(coro)
    async def wrapper(*args, **kwargs) -> Union[Coroutine, None]:
        context = args[0]
        if not is_production(context):
            return None
        try:
            return await coro(*args, **kwargs)
        except RollerException as error:
            await context.send(str(error))
        except Exception as error:
            if test_mode:
                raise error
            else:
                error = UnexpectedError(str(error))
                await context.send(error)
    return wrapper


def has_valid_arguments(args: Tuple[str]) -> bool:
    """Checks if tuple of strings contains at least one item.
    Raises TooFewArguments if tuple is empty.
    """
    if len(args) == 0:
        raise TooFewArguments()
    return True


def argument_handler(coro: Callable):
    """A decorator used for checking if a function has received at least one argument.
    Raises TooFewArguments if no arguments were received."""
    @wraps(coro)
    async def wrapper(*args, **kwargs) -> Coroutine:
        has_valid_arguments(args[1:])
        return await coro(*args, **kwargs)
    return wrapper


@bot.event
async def on_guild_join(guild: Guild) -> None:
    """Sends a welcome message on guild join."""
    await guild.system_channel.send(
        "Hi, I am Marduk. Your personal dragon assistant. To tame me, simply type **!help-me** or **/help-me**")


@bot.event
async def on_ready() -> None:
    """Shows activity in discord server when bot is ready to be used."""
    await bot.change_presence(activity=discord.Game(name='D&D | !help-me'))


def help_me(context):
    """Returns a message containing all current bot commands."""
    author = context.author.nick if hasattr(context.author, 'nick') else context.author.name
    result_message = get_help_messages()
    embed_list = []
    for return_message in result_message:
        embedded_message = discord.Embed(title=return_message[0], description=return_message[1], color=10038562)
        embedded_message.set_author(name=author, icon_url=context.author.avatar_url)
        embed_list.append(embedded_message)
    return embed_list


@bot.command(name="help-me")
@error_handler
async def help_me_command(context):
    """Sends message through discord.py command system when user types !help-me. Gets message from help-me."""
    messages = help_me(context)
    if context.guild:
        await context.send("I have delivered secrets of taming me to your PMs.")
    for message in messages:
        await context.author.send(embed=message)


@slash.slash(name="help-me", description="Sends you a PM with all commands.")
@error_handler
async def help_me_slash(context):
    """Sends message through discord-slash system when user types /help-me. Gets message from help-me."""
    messages = help_me(context)
    if context.guild:
        await context.send("I have delivered secrets of taming me to your PMs.")
        for message in messages:
            await context.author.send(embed=message)
    else:
        for message in messages:
            await context.send(embed=message)


def roll(context, args):
    """Takes a rollable string such as 1d20+5 and returns its result after evaluating all the dice."""
    result, dice_rolls = roller.roll_dice(args)
    result_message = f"{context.author.mention}\n**Roll**: {args}\n**Total: **{result}\n**Results**: {dice_rolls}"
    return result_message


@bot.command(name="roll", aliases=("r",))
@error_handler
@argument_handler
async def roll_command(context, *args):
    """Sends message through discord.py command system when user types !roll. Requires valid dice roll as input."""
    args = " ".join(args)
    result_message = roll(context, args)
    await context.send(result_message)


@slash.slash(name="roll",
             description="Rolls Dice in xdy format. In case of FATE rolls, replace 'y' with 'F'.",
             options=[
                 create_option(
                     name="dice",
                     description="Dice in xdy format",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 )
             ]
             )
@error_handler
async def roll_slash(context, dice=""):
    """Sends message through discord-slash system when user types /roll. Requires valid dice roll as input."""
    result_message = roll(context, dice)
    await context.send(result_message)


def wild(context):
    """Returns a random value from the wild magic effects table. Internally, it uses 1d50 to determine the effect."""
    result_roll = roller.roll_dice("1d50")[0]
    result_message = f"{context.author.mention}\nYour wild magic surge is:\n" + wildmagic.determine_wild_magic(
        result_roll)
    return result_message


@bot.command(name="wild")
@error_handler
async def wild_command(context):
    """Sends message through discord.py command system when user types !wild."""
    result_message = wild(context)
    await context.send(result_message)


@slash.slash(name="wild", description="Rolls a random wild magic effect.")
@error_handler
async def wild_command(context):
    """Sends message through discord-slash system when user types /wild."""
    result_message = wild(context)
    await context.send(result_message)


def chaos(context):
    """Returns a random value from the chaos magic effects table.
    Internally, it uses 1d10000 to determine the effect."""
    result_roll = roller.roll_dice("1d10000")[0]
    result_message = f"{context.author.mention}\nYour random magical effect is:\n" + wildmagic.determine_surge_magic(
        result_roll)
    return result_message


@bot.command(name="chaos")
@error_handler
async def chaos_command(context):
    """Sends message through discord.py command system when user types !chaos."""
    result_message = chaos(context)
    await context.send(result_message)


@slash.slash(name="chaos", description="Rolls a random 1d10000 wild magic effect.")
@error_handler
async def chaos_slash(context):
    """Sends message through discord-slash system when user types /chaos."""
    result_message = chaos(context)
    await context.send(result_message)


async def reference(context, item_type, args):
    author = context.author.nick if hasattr(context.author, 'nick') else context.author.name
    result_message = reference_handler.reference_item(item_type, args)
    for return_message in result_message:
        embedded_message = discord.Embed(title=return_message[0], description=return_message[1], color=10038562)
        embedded_message.set_author(name=author, icon_url=context.author.avatar_url)
        await context.send(embed=embedded_message)


@bot.command(name="spell")
@error_handler
@argument_handler
async def spell_command(context, *args):
    args = " ".join(args)
    await reference(context, "spell", args)


@slash.slash(name="spell", description="Looks up spell card.",
             options=[
                 create_option(
                     name="name",
                     description="Name of the spell.",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 )
             ]
             )
@error_handler
async def spell_slash(context, name):
    await reference(context, "spell", name)


@bot.command(name="monster")
@error_handler
@argument_handler
async def monster_command(context, *args):
    args = " ".join(args)
    await reference(context, "monster", args)


@slash.slash(name="monster", description="Looks up monster card.",
             options=[
                 create_option(
                     name="name",
                     description="Name of the monster.",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 )
             ]
             )
@error_handler
async def monster_slash(context, name):
    await reference(context, "monster", name)


@bot.command(name="class")
@error_handler
@argument_handler
async def dnd_class_command(context, *args):
    args = " ".join(args)
    await reference(context, "class", args)


@slash.slash(name="class", description="Looks up class card.",
             options=[
                 create_option(
                     name="name",
                     description="Name of the class.",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 ),
                 create_option(
                     name="level",
                     description="Referenced level",
                     option_type=SlashCommandOptionType.STRING,
                     required=False
                 )
             ]
             )
@error_handler
async def dnd_class_slash(context, name, level=""):
    if level:
        name = name + " " + level
    await reference(context, "class", name)


@bot.command()
@error_handler
@argument_handler
async def condition_command(context, *args):
    args = " ".join(args)
    await reference(context, "condition", args)


@slash.slash(name="condition", description="Looks up condition card.",
             options=[
                 create_option(
                     name="name",
                     description="Name of the condition.",
                     option_type=SlashCommandOptionType.STRING,
                     required=True
                 )
             ]
             )
@error_handler
async def condition_slash(context, name):
    await reference(context, "condition", name)


def randstat(context, args, default):
    if len(args) == 0:
        args = default
    return_message = ""
    total = 0
    for _ in range(0, 6):
        result, dice_rolls = roller.roll_dice(args)
        return_message += f"{args} {dice_rolls}: {result}\n"
        total += result
    return_message += f"Total: {total}"
    return_message = context.author.mention + "```" + "\nRandomly Generated Statistics:\n" + return_message + "```"
    return return_message


@bot.command(name="randstat", aliases=("randstats",))
@error_handler
async def randstat_command(context, *args, default="4d6kh3"):
    if len(args) > 0:
        args = " ".join(args)
    return_message = randstat(context, args, default)
    await context.send(return_message)


@slash.slash(name="randstat",
             description="""Rolls random ability scores for D&D using 4d6 drop lowest. A different roll can be provided.""",
             options=[
                 create_option(
                     name="dice",
                     description="Dice in xdy format",
                     option_type=SlashCommandOptionType.STRING,
                     required=False
                 )
             ]
             )
@error_handler
async def randstat_slash(context, dice="", default="4d6kh3"):
    return_message = randstat(context, dice, default)
    await context.send(return_message)


bot.run(token)
