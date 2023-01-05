import hikari
import lightbulb
import random

from operator import itemgetter
from helper import database
from helper import user
from helper import manager


nuggets_plugin = lightbulb.Plugin("nuggets")


#Nuggets Collect Command
@nuggets_plugin.command()
@lightbulb.command("nuggets_collect",
                   "Collect your daily nuggets!",
                   pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def nuggets_collect(ctx: lightbulb.Context):
  embed=(hikari.Embed(title=f"{ctx.user.username} Nugget Collection"))

  manager.refresh_user_info(ctx.user.id, ctx.user.username)

  embed.description=manager.collect_daily_nuggets(ctx.user.id)
  embed.set_thumbnail("https://i.redd.it/1yp58oe4pby61.png")
  embed.set_footer("Artwork by noion_art")

  await ctx.respond(embed)

#Check amount command
@nuggets_plugin.command()
@lightbulb.command("inventory_nugs",
                   "Check the items you have collected!")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def inventory_nugs(ctx: lightbulb.Context):
  embed = (hikari.Embed(title=f"{ctx.user.username}'s Nugget Collection"))
  #Check if user is in database
  manager.refresh_user_info(ctx.user.id, ctx.user.username)
  
  player = user.User(ctx.user.id)
  embed.set_thumbnail(ctx.user.avatar_url)
  embed.add_field("Nuggets", str(player.nuggets))
  embed.add_field("Seeds", str(player.seeds))
  embed.add_field("Plots", str(player.plots))
  embed.add_field("Trees", str(player.trees))

  await ctx.respond(embed)

#Leaderboard Command
@nuggets_plugin.command()
@lightbulb.command("nuggets_leaderboard",
                   "View the nuggets leaderboard",
                   pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def nuggets_leaderboard(ctx: lightbulb.Context):
  embed = (
            hikari.Embed(
                title="Most Collected Nuggets",)
                .add_field("Leaderboard", "Placeholder")
        )

  embed.edit_field(0, "Leaderboard", manager.get_leaderboard())
  await ctx.respond(embed)

@nuggets_plugin.command()
@lightbulb.option("recipient", "The user you want to give your nuggets away to", hikari.User, required=True)
@lightbulb.option("amount", "The amount of Nuggets to give away.", hikari.OptionType.INTEGER, required=True)
@lightbulb.command("give_nuggets", "Give your hard earned nuggets away!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def give_nuggets(ctx: lightbulb.Context, recipient: hikari.User, amount: hikari.OptionType.INTEGER):

  manager.refresh_user_info(ctx.user.id, ctx.user.username)
  manager.refresh_user_info(recipient.id, recipient.username)

  giving_user = user.User(ctx.user.id)
  recipient_user = user.User(recipient.id)

  givers_current_nuggets = int(giving_user.nuggets)
  recipient_current_nuggets = int(recipient_user.nuggets)
  

  if givers_current_nuggets < amount or amount < 1:
    await ctx.respond("I am afraid you don't have that amount of nuggets to give")
    return
  
  if ctx.user.id == recipient.id:
    await ctx.respond("Nice try >.>. You can't give yourself nuggets silly.")
    return
    
  else:
    givers_new_nuggets = givers_current_nuggets - amount
    recipient_new_nuggets = recipient_current_nuggets + amount

    giving_user.set_nuggets(givers_new_nuggets, ctx.user.id)
    recipient_user.set_nuggets(recipient_new_nuggets, recipient.id)

    giving_user = user.User(ctx.user.id)
    recipient_user = user.User(recipient.id)

    givers_current_nuggets = int(giving_user.nuggets)
    recipient_current_nuggets = int(recipient_user.nuggets)

    await ctx.respond(f"You gave {str(amount)} nuggets to {recipient.username}. You currently have {str(givers_current_nuggets)} nuggets and {recipient.username} now has {str(recipient_current_nuggets)} nuggets")

  print(givers_new_nuggets, recipient_current_nuggets)

'''
@nuggets_plugin.set_error_handler
async def on_nuggets_error(event: lightbulb.CommandErrorEvent) -> bool:
  exception = event.exception.__cause__ or event.exception
  if isinstance(exception, lightbulb.CommandIsOnCooldown):
    seconds = int(exception.retry_after)
    time = datetime.timedelta(seconds=seconds)
    await event.context.respond(
      f"This command is on cooldown! You can use it again in " + str(time))
    return True
  return False'''


def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(nuggets_plugin)
