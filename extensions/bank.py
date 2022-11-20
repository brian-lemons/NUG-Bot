import hikari
import lightbulb
import math
import datetime

bank_plugin = lightbulb.Plugin("bank")

@lightbulb.add_cooldown(5, 1, lightbulb.UserBucket)
@bank_plugin.command()
@lightbulb.option("banking_level", "Banking level you want to calculate",hikari.OptionType.INTEGER ,required=True)
@lightbulb.option("total_econ", "Total amount of econ you will have at EOC", hikari.OptionType.INTEGER ,required=True)
@lightbulb.command("bank", "Calculate your End of Cycle banking reward amount!", pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def bank(ctx: lightbulb.Context, banking_level: hikari.OptionType.INTEGER, total_econ: hikari.OptionType.INTEGER):
    
    extra_credits = math.ceil((banking_level * 75) + (0.15 * banking_level * total_econ))
    econ_income = math.ceil(10 * total_econ) 
    total_income = econ_income + extra_credits

    embed = (
        hikari.Embed(
            title= "Results",
        )
        .add_field(
            "Banking Level", str(banking_level),
            inline=True,
        )
        .add_field(
            "Total Economy", str(total_econ),
            inline=True,
        )
        .add_field(
            "Extra Credit Allowance", str(extra_credits),
        )
        .add_field(
            "Total Income From Econonmy", str(econ_income),
            inline=True,
        )
        .add_field(
            "Total Combined Income", str(total_income),
            inline=True
        )
    )

    await ctx.respond(embed)

@bank_plugin.set_error_handler
async def on_bank_error(event: lightbulb.CommandErrorEvent) -> bool:
  exception = event.exception.__cause__ or event.exception
  if isinstance(exception, lightbulb.CommandIsOnCooldown):
    seconds = int(exception.retry_after)
    time = datetime.timedelta(seconds=seconds)
    await event.context.respond(f"This command is on cooldown! You can use it again in "  + str(time))
    return True
  return False

def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(bank_plugin)