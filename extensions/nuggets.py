import hikari
import lightbulb
import random

from operator import itemgetter
from helper import database
from helper import user



nuggets_plugin = lightbulb.Plugin("nuggets")


#Nuggets Collect Command
@nuggets_plugin.command()
@lightbulb.command("nuggets_collect",
                   "Collect your daily nuggets!",
                   pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def nuggets_collect(ctx: lightbulb.Context):
  nugget_amount = random.randrange(25, 500)
  default_seed_amount = 1

  refresh_user_info(ctx.user.id, ctx.user.username)

  player = user.User(ctx.user.id)

  #Set new nugget amount
  current_nuggets = int(player.nuggets)
  new_nuggets = current_nuggets + nugget_amount
  print(new_nuggets)

  player.set_nuggets(new_nuggets, ctx.user.id)

  #Refresh the user
  player = user.User(ctx.user.id)


  
  if nugget_amount <= 300:
    current_seeds = int(player.seeds)
    new_seeds = current_seeds + default_seed_amount
    player.set_seeds(new_seeds, ctx.user.id)
    #Refresh the user
    player = user.User(ctx.user.id)
    await ctx.respond(
      "You've found: " + str(nugget_amount) + " nuggets! You now have: " +
      str(current_nuggets) +
      " nuggets! Oh, and take this seed I found as well. Might grow into something new!"
    )
    return

  await ctx.respond("You've found: " + str(nugget_amount) +
                      " nuggets! You now have: " + str(player.nuggets) +
                      " nuggets!")

#Check amount command
@nuggets_plugin.command()
@lightbulb.command("inventory_nugs",
                   "Check the items you have collected!")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def inventory_nugs(ctx: lightbulb.Context):
  embed = (
    hikari.Embed(
      title="Nugget Collection", 
    )
  )
  #Check if user is in database
  refresh_user_info(ctx.user.id, ctx.user.username)
  
  player = user.User(ctx.user.id)
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
    hikari.Embed
    (
      title="Most Collected Nuggets", 
    )
    .add_field(
    "Leaderboard", "Placeholder"
    )
  )

  #Grab the data
  sql = "SELECT user_name, nuggets FROM users ORDER BY nuggets ASC"
  info = database.complex_query_fetchall(sql)
  users_names = database.convert_tuple_data_into_list(info)
  nuggets = database.convert_tuple_data_into_list(info, 1)
  users_and_nuggets = zip(users_names, nuggets)

  
  #Convert data to list
  leaderboard_list = []
  for name, value in users_and_nuggets:
    user_tuple = (name,value)
    leaderboard_list.append(user_tuple)
  
  leaderboard = dict(leaderboard_list)

  #sort
  sorted_leaderboard = sorted(leaderboard.items(), key=itemgetter(1))
  sorted_leaderboard_dict = dict(sorted_leaderboard)

  current_text = ""
  position = 0
  position = len(sorted_leaderboard_dict) + 1


  for key, value in sorted_leaderboard_dict.items():
    position -= 1
    new_text = str(position) + ". " + key + " (" + str(value) + ") \n"
    current_text = new_text + current_text

  embed.edit_field(0, "Leaderboard", current_text)
  await ctx.respond(embed)

@nuggets_plugin.command()
@lightbulb.option("recipient", "The user you want to give your nuggets away to", hikari.User, required=True)
@lightbulb.option("amount", "The amount of Nuggets to give away.", hikari.OptionType.INTEGER, required=True)
@lightbulb.command("give_nuggets", "Give your hard earned nuggets away!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def give_nuggets(ctx: lightbulb.Context, recipient: hikari.User, amount: hikari.OptionType.INTEGER):

  refresh_user_info(ctx.user.id, ctx.user.username)
  refresh_user_info(recipient.id, recipient.username)

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


def refresh_user_info(user_id, user_name):
  if database.check_if_data_exists(user_id, "users", "user_id") is False:
    print(user_id, user_name)
    print("failed")
    user.User.create_new_user(user_id, user_name)


def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(nuggets_plugin)
