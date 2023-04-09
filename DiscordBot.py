import os
from functools import wraps
from typing import Callable, Coroutine, Union

import discord
from discord import Guild, SlashCommandOptionType, Option
from discord.ext.commands import Context
from dotenv import load_dotenv

from DiceOperations.Roller import DiceRoll
from ReferenceOperations.ReferenceHandler import ReferenceHandler
from Utility.ErrorHandler import UnexpectedError, RollerException
from Utility.GetHelp import get_help_messages
from Utility.UtilityHandler import escape
from WildMagicHandler import WildMagic

load_dotenv()
bot = discord.Bot()
roller = DiceRoll()
wildmagic = WildMagic()
reference_handler = ReferenceHandler()
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
            await context.respond(str(error))
        except Exception as error:
            if test_mode:
                raise error
            else:
                error = UnexpectedError(str(error))
                await context.respond(error)

    return wrapper

@bot.event
async def on_guild_join(guild: Guild) -> None:
    """Sends a welcome message on guild join."""
    await guild.system_channel.send(
        "Hi, I am Marduk. Your personal dragon assistant. To tame me, simply type **/help**")


@bot.event
async def on_ready() -> None:
    """Shows activity in discord server when bot is ready to be used."""
    await bot.change_presence(activity=discord.Game(name='D&D | /help'))


def help_message(context):
    """Returns a message containing all current bot commands."""
    result_message = get_help_messages()
    embedded_message = discord.Embed(title=result_message[0], description=result_message[1], color=10038562)
    embedded_message.set_author(name=context.author.display_name, icon_url=context.author.display_avatar)
    return embedded_message


@bot.slash_command(name="help", description="Sends you a PM with all commands.")
@error_handler
async def help_slash(context):
    """Sends message through discord-slash system when user types /help. Gets message from help."""
    message = help_message(context)
    await context.respond(embed=message, ephemeral=True)


def make_roll(context, args):
    """Takes a rollable string such as 1d20+5 and returns its result after evaluating all the dice."""
    result, dice_rolls = roller.roll_dice(args)
    result_message = f"{context.author.mention}\n**Roll**: {escape(args)}\n**Total: **{result}\n**Results**: {escape(dice_rolls)}"
    return result_message


@bot.slash_command(name="roll", description="Rolls Dice in xdy format. In case of FATE rolls, replace 'y' with 'F'.",
                   options=[
                       Option(name="dice",
                              description="Dice in xdy format",
                              option_type=SlashCommandOptionType.string,
                              required=True)

                   ])
@error_handler
async def roll_slash(context, dice):
    """Sends message through discord-slash system when user types /roll. Requires valid dice roll as input."""
    dice = dice.lower()
    result_message = make_roll(context, dice)
    await context.respond(result_message)


def wild(context):
    """Returns a random value from the wild magic effects table. Internally, it uses 1d50 to determine the effect."""
    result_roll = roller.roll_dice("1d50")[0]
    result_message = f"{context.author.mention}\nYour wild magic surge is:\n" + wildmagic.determine_wild_magic(
        result_roll)
    return result_message


@bot.slash_command(name="wild", description="Rolls a random wild magic effect.")
@error_handler
async def wild_command(context):
    """Sends message through discord-slash system when user types /wild."""
    result_message = wild(context)
    await context.respond(result_message)


def chaos(context):
    """Returns a random value from the chaos magic effects table.
    Internally, it uses 1d10000 to determine the effect."""
    result_roll = roller.roll_dice("1d10000")[0]
    result_message = f"{context.author.mention}\nYour random magical effect is:\n" + wildmagic.determine_surge_magic(
        result_roll)
    return result_message


@bot.slash_command(name="chaos", description="Rolls a random 1d10000 wild magic effect.")
@error_handler
async def chaos_slash(context):
    """Sends message through discord-slash system when user types /chaos."""
    result_message = chaos(context)
    await context.respond(result_message)


async def reference(context, item_type, args):
    item_type = item_type.lower()
    result_message = reference_handler.reference_item(item_type, args)
    for return_message in result_message:
        embedded_message = discord.Embed(title=return_message[0], description=return_message[1], color=10038562)
        embedded_message.set_author(name=context.author.display_name, icon_url=context.author.display_avatar)
        await context.respond(embed=embedded_message)


@bot.slash_command(name="spell", description="Looks up spell card.",
                   options=[
                       Option(name="name",
                              description="The name of the spell from SRD you want to look up.",
                              option_type=SlashCommandOptionType.string,
                              required=True)

                   ])
@error_handler
async def spell_slash(context, name):
    await reference(context, "spell", name)


@bot.slash_command(name="monster", description="Looks up monster card.",
                   options=[
                       Option(name="name",
                              description="The name of the monster from SRD you want to look up.",
                              option_type=SlashCommandOptionType.string,
                              required=True)

                   ])
@error_handler
async def monster_slash(context, name):
    await reference(context, "monster", name)


@bot.slash_command(name="class", description="Looks up class card. Providing level returns a list of features at that level.",
                   options=[
                       Option(name="name",
                              description="The name of the class you want to look up.",
                              option_type=SlashCommandOptionType.string,
                              required=True),
                       Option(name="level",
                              description="Level you want to see features at. 1-20.",
                              default="",
                              option_type=SlashCommandOptionType.string,
                              required=False)

                   ])
@error_handler
async def class_slash(context, name, level):
    if level:
        name = name + " " + level
    await reference(context, "class", name)


@bot.slash_command(name="condition", description="Looks up condition card.",
                   options=[
                       Option(name="name",
                              description="The name of the condition you want to look up.",
                              option_type=SlashCommandOptionType.string,
                              required=True)

                   ])
@error_handler
async def condition_slash(context, name):
    await reference(context, "condition", name)


def randstat(context, args):
    return_message = ""
    total = 0
    for _ in range(0, 6):
        result, dice_rolls = roller.roll_dice(args, inside_codeblock=True)
        return_message += f"{args} {dice_rolls}: {result}\n"
        total += result
    return_message += f"Total: {total}"
    return_message = context.author.mention + "```" + "\nRandomly Generated Statistics:\n" + return_message + "```"
    return return_message


@bot.slash_command(name="randstat", description="Rolls random ability scores for D&D using 4d6 drop lowest. A different roll can be provided.",
                   options=[
                       Option(name="dice",
                              description="Dice in xdy format",
                              default="4d6kh3",
                              option_type=SlashCommandOptionType.string,
                              required=False)

                   ])
@error_handler
async def randstat_slash(context, dice):
    return_message = randstat(context, dice)
    await context.respond(return_message)


bot.run(os.getenv("TOKEN"))
