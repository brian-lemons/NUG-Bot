import hikari
import math

import lightbulb

weapons_plugin = lightbulb.Plugin("weapons")


@weapons_plugin.command
@lightbulb.option("attackers_weapons",
                  "attackers weapons level",
                  hikari.OptionType.INTEGER,
                  required=True)
@lightbulb.option("defenders_weapons",
                  "defenders weapons level",
                  hikari.OptionType.INTEGER,
                  required=True)
@lightbulb.option("attackers_ships",
                  "attackers ship amount",
                  hikari.OptionType.INTEGER,
                  required=True)
@lightbulb.option("defenders_ships",
                  "defender ship amount",
                  hikari.OptionType.INTEGER,
                  required=True)
@lightbulb.option("defenders_bonus",
                  "Does the defender have a defenders bonus?",
                  hikari.OptionType.BOOLEAN,
                  required=True)
@lightbulb.command("weapons", "Calculate combat", pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def weapons(ctx: lightbulb.context,
                  attackers_weapons: hikari.OptionType.INTEGER,
                  defenders_weapons: hikari.OptionType.INTEGER,
                  attackers_ships: hikari.OptionType.INTEGER,
                  defenders_ships: hikari.OptionType.INTEGER,
                  defenders_bonus: hikari.OptionType.BOOLEAN):

  #Calculate Defenders Bonus
  if defenders_bonus == True:
    defenders_weapons += 1
    defenders_bonus_text = "Yes"
  else:
    defenders_bonus_text = "No"

  #Set minimum hits needed to destory all of the opposing ships
  attacker_min_hits = math.ceil(defenders_ships / attackers_weapons)
  defenders_min_hits = math.ceil(attackers_ships / defenders_weapons)

  #Calculate attacking and defending ships lost
  if attacker_min_hits > defenders_min_hits or attacker_min_hits == defenders_min_hits and defenders_bonus == True:
    defenders_ships_lost = (defenders_min_hits - 1) * attackers_weapons
    attacker_ships_lost = defenders_min_hits * defenders_weapons
  else:
    defenders_ships_lost = attacker_min_hits * attackers_weapons
    attacker_ships_lost = attacker_min_hits * defenders_weapons

  #Calculate who wins combat
  if attacker_ships_lost > attackers_ships:
    attacking_ships_remaining = 0
  else:
    attacking_ships_remaining = attackers_ships - attacker_ships_lost

  if defenders_ships_lost > defenders_ships:
    defending_ships_remaining = 0
  else:
    defending_ships_remaining = defenders_ships - defenders_ships_lost

  if attacking_ships_remaining > defending_ships_remaining:
    who_won = "Attacker"
  else:
    who_won = "Defender"

  if attacking_ships_remaining == defending_ships_remaining:
    who_won = "No One"
    attacking_ships_remaining = 0
    defending_ships_remaining = 0

  #Calculate ships needed to win

  embed = (hikari.Embed(title="Battle Results").set_footer(
    text=f"Requested by {ctx.author.username}",
    icon=ctx.author.display_avatar_url,
  ).add_field("Defenders Bonus", defenders_bonus_text).add_field(
    "Attackers Ships",
    str(attackers_ships),
  ).add_field(
    "Defenders Ships",
    str(defenders_ships),
  ).add_field(
    "Attackers Weapons",
    str(attackers_weapons),
  ).add_field("Defenders Weapons", str(defenders_weapons)).add_field(
    "Winner",
    who_won,
    inline=True,
  ).add_field(
    "Attacking Ships Remaining",
    str(attacking_ships_remaining),
    inline=True,
  ).add_field(
    "Defending Ships Remaining",
    str(defending_ships_remaining),
    inline=True,
  ))

  await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(weapons_plugin)
