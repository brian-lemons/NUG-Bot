import hikari
import lightbulb
import math
import random
import datetime
import sqlite3
from operator import itemgetter



nuggets_plugin = lightbulb.Plugin("nuggets")


#Nuggets Collect Command
@lightbulb.add_cooldown(86400, 1, lightbulb.UserBucket)
@nuggets_plugin.command()
@lightbulb.command("nuggets_collect",
                   "Collect your daily nuggets!",
                   pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def nuggets_collect(ctx: lightbulb.Context):
  nugget_amount = random.randrange(25, 500)
  default_seed_amount = 1

  refresh_user_info(ctx.user.id, ctx.user.username)

  add_item(ctx.user.id, nugget_amount, "nuggets")
  current_nuggets = get_item(ctx.user.id, "nuggets")

  if nugget_amount <= 300:
    add_item(ctx.user.id, default_seed_amount, "seeds")
    await ctx.respond(
      "You've found: " + str(nugget_amount) + " nuggets! You now have: " +
      str(current_nuggets) +
      " nuggets! Oh, and take this seed I found as well. Might grow into something new!"
    )
    return

  await ctx.respond("You've found: " + str(nugget_amount) +
                      " nuggets! You now have: " + str(current_nuggets) +
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
  

  embed.add_field("Nuggets", str(get_item(ctx.user.id, "nuggets")))
  embed.add_field("Seeds", str(get_item(ctx.user.id, "seeds")))
  embed.add_field("Plots", str(get_item(ctx.user.id, "plots")))
  embed.add_field("Trees", str(get_item(ctx.user.id, "trees")))

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

  connection = sqlite3.connect("users.db")
  cursor = connection.cursor()


  cursor.execute("SELECT user_name, nuggets FROM users ORDER BY nuggets DESC")
  users = cursor.fetchall()

  leaderboard = dict(users)
  print(leaderboard)

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


@nuggets_plugin.set_error_handler
async def on_nuggets_error(event: lightbulb.CommandErrorEvent) -> bool:
  exception = event.exception.__cause__ or event.exception
  if isinstance(exception, lightbulb.CommandIsOnCooldown):
    seconds = int(exception.retry_after)
    time = datetime.timedelta(seconds=seconds)
    await event.context.respond(
      f"This command is on cooldown! You can use it again in " + str(time))
    return True
  return False


def refresh_user_info(user_id, user_name):
  connection = sqlite3.connect("users.db")
  cursor = connection.cursor()

  default_nuggets = 0
  default_seeds = 0
  default_trees = 0
  default_plots = 0
  default_plot_price = 0

  user_info = [
    (user_id, default_nuggets, user_name, default_seeds, default_trees, default_plots, default_plot_price)
    ]

  

  #Check to see if user table exists
  tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'").fetchall()
  if tables == []:
    cursor.execute("CREATE TABLE users (user_id INTEGER, nuggets INTEGER, user_name TEXT, seeds INTEGER, trees INTEGER, plots INTEGER, plot_price INTEGER)")
    cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?,?,?)", user_info)
    connection.commit()
  
  else:
    #Check if user exists in table
    cursor.execute("SELECT rowid FROM users WHERE user_id = ?", (user_id, ))
    data= cursor.fetchone()
    print(data)
    if data is None:
      cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?,?,?)", user_info)
      print(data)
      connection.commit()
    else:
      cursor.execute("UPDATE users SET user_id= ? WHERE user_id= ?", (user_id, user_id))
      cursor.execute("UPDATE users SET user_name= ? WHERE user_id= ?", (user_name, user_id))
      connection.commit()
  
  for row in cursor.execute("SELECT * FROM users"):
    print(row)
  connection.close()


#Set new items to user database
def set_item(user_id, amount, item):
  connection = sqlite3.connect("users.db")
  cursor = connection.cursor()

  cursor.execute("UPDATE users SET " + item + "= ? WHERE user_id= ?", (amount, user_id))
  connection.commit()

  connection.close()

#Add new items to user database
def add_item(user_id, amount, item):
  connection = sqlite3.connect("users.db")
  cursor = connection.cursor()

  cursor.execute("SELECT " + item + " FROM users WHERE user_id= ?", (user_id, ))
  item_row = cursor.fetchone()
  current_amount = item_row[0]
  amount += current_amount

  cursor.execute("UPDATE users SET " + item + "= ? WHERE user_id= ?", (amount, user_id))
  connection.commit()

  connection.close()

#Remove new items to user database
def remove_item(user_id, amount, item):
  connection = sqlite3.connect("users.db")
  cursor = connection.cursor()

  cursor.execute("SELECT " + item + " FROM users WHERE user_id= ?", (user_id, ))
  item_row = cursor.fetchone()
  current_amount = item_row[0]
  amount -= current_amount

  cursor.execute("UPDATE users SET " + item + "= ? WHERE user_id= ?", (amount, user_id))
  connection.commit()

  connection.close()

def get_item(user_id, item):
  connection = sqlite3.connect("users.db")
  cursor = connection.cursor()

  cursor.execute("SELECT " + item + " FROM users WHERE user_id= ?", (user_id, ))
  item_row = cursor.fetchone()
  value = item_row[0]
  connection.commit()

  connection.close()

  return value

def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(nuggets_plugin)
