# Discord-Roller

Discord-Roller is a bot which allows you to roll dice through simple commands. As the name suggests, the bot is dedicated for Discord.
It also has additional features such as an ability to roll wild magic for d&d 5th edition or booking solo-sessions.

## Installing / Getting started

To install the bot, just click: https://discord.com/oauth2/authorize?client_id=713734351648587776&permissions=206848&scope=bot
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
* !race|r [RACE_NAME] - sends a race card to the server chat.
* !class|c [CLASS_NAME] - sends a class card to the server chat.

## Mathematical Operations
You can do math-only rolls by adding a math expression after the roll command.

For example, if you want Discord Roller to do a simple addition like 5 + 3, you'd enter the following:
!r 5+3
Discord Roller supports following operations:
* Addition: "+"
* Substrations: "-"
* Multiplication: "*"
* Division: "/"
* Rounded Division: "//" - Automatically rounds down
* Modulus: "%"


## Modifiers
### Exploding Dice:
DiscordRoller supports exploding dice -- you may also know it as "rule of 6", "rule of 10s", or "acing" depending on your game system. With exploding dice, if you roll the maximum number on the dice (a 6 with a d6, a 10 with a d10, etc.) you get to re-roll again and add the additional roll to your total for that roll. If the additional roll is also a maximum number, you get to keep rolling!
To perform a roll with exploding dice, just add an exclamation point after the number of sides in the formula. For example, !r 3d6! would roll 3 d6 dice with exploding re-rolls.

### Compounding Exploding Dice (Shadowrun-Style Exploding Dice):
Shadowrun (and some other systems) use a special style of exploding dice where the the additional rolls for each dice are added together as a single "roll". To do this, just use two exclamation marks instead of one. So for example to roll 5 d6's, you would do !r 5d6!!.

### Penetrating Exploding Dice (Hackmaster-Style Exploding Dice):
HackMaster (and some other systems) use a special style of exploding dice where the the additional rolls for each dice have 1 subtracted from the roll. To do this, add a p after the exclamation mark. So for example to roll 5 d6's, you would do !r 5d6!p.

### Drop/Keep:
Some game systems ask you to roll a large number of dice, and then either drop a certain number of the lowest rolls, or keep only a certain number of the highest rolls. Discord Roller supports this type of roll through the d and k commands, respectively.

For example, you might roll 8 d100 dice and only be allowed to keep the top 4 rolls. In Discord Roller this would be expressed with !r 8d100k4. Doing a roll to drop the 3 lowest rolls would be very similar: !r 8d100d3. In each case, the unwanted dice are dropped.

The d and k commands are shortcuts for the full dl and kh commands. If you need to drop the highest dice use dh and if you need to keep the lowest dice use kl. For example !r 8d100dh3 would drop the highest three rolls and keep the lowest 5 and !r 8d100kl3 would keep the lowest three rolls and drop the highest 5.

### Target Number (Successes)
Normally when you perform a roll, DiscordRoller reports back the total value of all the dice rolled, plus any modifiers. Some game systems, though, work by rolling a set of dice versus a target number, and then adding up the total number of successes instead. DiscordRoller uses the greater-than symbol > to indicate when the roll is greater-than or equal-to >= the target number. The less-than symbol < is used to indicate when the roll is less-than or equal-to <= the target number.

For example, you might be performing an action that requires a target number of 3, and you get to roll 3 d6's to see how many successes you have. In DiscordRoller, you would do !r 3d6>3. Note the inclusion of the greater-than symbol to indicate that this is a target roll versus 3. DiscordRoller will show you each dice that was rolled, and then tell you the number of dice with a value of 3 or greater (note that ties with the target number count as a success!). You can also roll less-than target numbers, for example !r 10d6<4, which would give you a success for each dice rolled that is equal to 4 or less.

### Fate Dice
DiscordRoller also supports FATE dice (used for FATE, FUDGE, and other systems). DiscordRoller accurately simulates FATE dice as 6-sided dice in which two sides are 0, two sides are +1, and two sides are -1.

To roll 4 FATE dice, just do !r 4dF. DiscordRoller will show you the result of each individual FATE dice roll, then give you the total of all the dice rolls added up together. You can also add a modifier onto the total, with !r 4dF+1.







