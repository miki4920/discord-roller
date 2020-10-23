# Marduk

Marduk is a bot which allows you to roll dice and reference SRD in D&D 5E.

## Installing / Getting started

To install the bot, just click: https://discord.com/oauth2/authorize?client_id=713734351648587776&scope=bot&permissions=3072
Then select the server you want to use.
Congratulations, you are ready to go!

## Terms Used
* DM - A person with one of the following ranks: "DM", "GM", "Game Master", "Dungeon Master".

## How to Use
Each command starts with the "!" prefix.
Dice Commands (All dice in format xdy):
* !roll|r [ROLL] - Rolls Dice in xdy format and sends to the server
* !gmroll|r [ROLL] - Same as the previous one, but sends to the roll to the DM and person who sent it.
Wild Magic:
* !w - Rolls a random wild magic effect.
Reference:
* !spell|s [SPELL_NAME] - Sends a spell card to the server chat.
* !monster|m [MONSTER_NAME] - Sends a monster card to the server chat.
* !race|r [RACE_NAME] - Sends a race card to the server chat.
* !class|c [CLASS_NAME] [CLASS_LEVEL] - Sends a class card to the server chat, if level is included, it sends specific features a class gets on that level.
* !condition [CONDITION_NAME] - Sends a condition card to the server chat.
* !randstats [OPTIONAL_ROLL] - Rolls random ability scores for D&D using 4d6 drop lowest. If optional roll provided, it would use that instead.

## Mathematical Operations
Marduk supports both dice operations and math-only operations.
For example, if you want Marduk to do a simple addition like 5 + 3, you'd enter the following:
!r 5+3
Following operations are supported:
* Addition: "+"
* Substrations: "-"
* Multiplication: "*"
* Division: "/"
* Rounded Division: "//" - Automatically rounds down
* Modulus: "%"

## Dice Modifiers
Marduk Supports a number of dice modifiers. To use them, simply add them at the end of the roll. For example 8d6k4 rolls eight six-sided dice and keeps four highest ones.
* Exploding Dice: "!"
* Compounding Exploding Dice: "!!"
* Penetrating Exploding Dice (Hackmaster-Style): "!p"
* Drops [NUMBER] of Lowest Dice: "dl[NUMBER]"
* Drops [NUMBER] of Highest Dice: "dh[NUMBER]"
* Abbrevation for "dl": "d[NUMBER]"
* Keeps [NUMBER] of Lowest Dice (Drops everything else): "kl[NUMBER]"
* Keeps [NUMBER] of Highest Dice (Drops everything else): "kh[NUMBER]"
* Abbrevation for "kh": "k[NUMBER]"

## Fate Dice
Marduk supports FATE dice. To roll one, simply use F instead of a number after d, such as 1dF.




