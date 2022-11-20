import hikari
import lightbulb
import math
import random
import datetime
import sqlite3
from operator import itemgetter



nuggets_plugin = lightbulb.Plugin("nuggets")


#Nuggets Collect Command
#@lightbulb.add_cooldown(86400, 1, lightbulb.UserBucket)
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


  '''


#Leaderboard Command
@nuggets_plugin.command()
@lightbulb.command("nuggets_leaderboard",
                   "View the nuggets leaderboard",
                   pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def nuggets_leaderboard(ctx: lightbulb.Context):
  embed = (hikari.Embed(title="Most Collected Nuggets", ).add_field(
    "Leaderboard", "Placeholder"))

  leaderboard = {}

  #Print out the current leaderboard
  for key in db.keys():
    user = db[key]["user_name"]
    total_nuggets = db[key]["nuggets"]
    leaderboard[user] = total_nuggets

  #sort
  sorted_leaderboard = sorted(leaderboard.items(), key=itemgetter(1))
  sorted_leaderboard_dict = dict(sorted_leaderboard)

  position = len(sorted_leaderboard_dict) + 1
  current_text = ""
  for key, value in sorted_leaderboard_dict.items():
    position -= 1
    new_text = str(position) + ". " + key + " (" + str(value) + ") \n"
    current_text = new_text + current_text

  embed.edit_field(0, "Leaderboard", current_text)
  await ctx.respond(embed)


#Give command
@nuggets_plugin.command()
@lightbulb.option("user",
                  "The user you would like to give your nuggets to!",
                  hikari.User,
                  required=True)
@lightbulb.option("amount",
                  "The amount of nuggets you want to give!",
                  hikari.OptionType.INTEGER,
                  required=True)
@lightbulb.command("nuggets_give",
                   "Give your nuggets to another user!",
                   pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def nuggets_give(
  ctx: lightbulb.Context,
  user: hikari.User,
  amount: hikari.OptionType.INTEGER,
):

  #Check if user has nuggets to give
  for key in db.keys():
    if key == str(ctx.user.id):
      if db[key]["nuggets"] >= amount and ctx.user.id != user.id:
        #remove nugget from giver
        current_nuggets = int(db[key]["nuggets"])
        current_nuggets -= amount

        #give nuggets to receiver
        receivers_nuggets = int(db[str(user.id)]["nuggets"])
        receivers_nuggets += amount

        #update givers nuggets
        refresh_user_info(ctx.user.id, current_nuggets, ctx.user.username)

        #update receivers nuggets
        refresh_user_info(user.id, receivers_nuggets, user.username)

        await ctx.respond("You give " + str(amount) + " nuggets to " +
                          user.username)
        return
      elif ctx.user.id == user.id:
        await ctx.respond("Nice try, you can't give yourself nuggets silly >.>"
                          )
      else:
        await ctx.respond("You don't have enough nuggets silly!")
        return


#Feed Dino command
@nuggets_plugin.command()
@lightbulb.option("amount",
                  "The amount of nuggets you wish to feed to Dino.",
                  hikari.OptionType.INTEGER,
                  required=True)
@lightbulb.command("feed_dino",
                   "Feed Dino for a chance for a boon, or a curse!",
                   pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def feed_dino(ctx: lightbulb.Context, amount: hikari.OptionType.INTEGER):
  #Feed the dino nuggets, based on how much is given, have a better chance of something good happening

  embed = (hikari.Embed(title="Dino Considers The Nuggets").add_field(
    "Dino Says",
    "Placeholder",
    inline=True,
  ).add_field(
    "Nuggets",
    "Placeholder",
    inline=False,
  ).add_field("Amount Given", "Placeholder",
              inline=True).add_field("Current Nugget Amount",
                                     "Placeholder",
                                     inline=False))
  #Check if user has enough nuggets to give
  nuggets_given = 0
  for key in db.keys():
    if key == str(ctx.user.id):
      if db[key]["nuggets"] >= amount:
        nuggets_given = amount
      else:
        await ctx.respond("You don't have that many nuggets to give!")
        return

  min_nuggs = 100
  mid_nuggs = 1000
  high_nuggs = 5000

  #Set the drop table
  dino_drop_table = {
    1: {
      "event_name": "nuggets_found",
      "weight": 10,
      "min_range": 1
    },
    2: {
      "event_name": "nuggets_eaten",
      "weight": 40,
      "min_range": 11
    },
    3: {
      "event_name": "return_nuggets",
      "weight": 50,
      "min_range": 41
    }
  }

  def set_weights():
    if nuggets_given <= min_nuggs:
      dino_drop_table[3]["weight"] = 100
    elif nuggets_given > high_nuggs:
      dino_drop_table[1]["weight"] = 40
      dino_drop_table[2]["weight"] = 10
      dino_drop_table[3]["weight"] = 25

  set_weights()

  total_weight = 0
  for key in dino_drop_table.keys():
    total_weight += dino_drop_table[key]["weight"]

  chance = random.randrange(1, total_weight)
  nuggets_gift = random.randrange(nuggets_given, nuggets_given * 2)
  nuggets_found = nuggets_gift - amount

  event_name = ""

  for key in dino_drop_table.keys():
    if chance <= dino_drop_table[key]["weight"] and chance >= dino_drop_table[
        key]["min_range"]:
      event_name = dino_drop_table[key]["event_name"]

  current_nuggets = int(db[str(ctx.user.id)]["nuggets"])
  if event_name == "nuggets_found":

    current_nuggets += nuggets_found
    refresh_user_info(ctx.user.id, current_nuggets, ctx.user.username)
    embed.edit_field(0, "Dino Says",
                     "Oh looky here, I found some extra nuggets for you!")
    embed.edit_field(1, "Nuggets Found", str(nuggets_found))
    embed.edit_field(2, "Nuggets Given", str(amount))
    embed.edit_field(3, "New Nuggets Amount", str(current_nuggets))
    await ctx.respond(embed)
    return

  elif event_name == "nuggets_eaten":
    current_nuggets -= amount
    refresh_user_info(ctx.user.id, current_nuggets, ctx.user.username)
    embed.edit_field(0, "Dino Says", "Yummy, I ate your nuggets 'burp'.")
    embed.edit_field(1, "Nuggets Ate", str(amount))
    embed.edit_field(2, "Nuggets Given", str(amount))
    embed.edit_field(3, "New Nuggets Amount", str(current_nuggets))
    await ctx.respond(embed)
    return

  elif event_name == "" or event_name == "return_nuggets":
    embed.edit_field(0, "Dino Says", "These smell funny, have them back!")
    embed.edit_field(1, "Nuggets Returned", str(amount))
    embed.edit_field(2, "Nuggets Given", str(amount))
    embed.edit_field(3, "New Nuggets Amount", str(current_nuggets))
    await ctx.respond(embed)
    return


#Plant Seed command
@nuggets_plugin.command()
@lightbulb.option("amount",
                  "How many seeds do you want to plant?",
                  hikari.OptionType.INTEGER,
                  required=True)
@lightbulb.command("plant_seed",
                   "Plant seeds you have found!",
                   pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def plant_seed(ctx: lightbulb.Context, amount: hikari.OptionType.INTEGER):
  if get_item(ctx.user.id, "seeds") == 0:
    await ctx.respond("I am afraid you have no seeds to plant!")
    return

  if get_item(ctx.user.id, "plots") == 0:
    await ctx.respond("You don't have any plots to plant your seeds! Type /view_market to see how much a new plot will cost you!")
    return
  
  add_tree(ctx.user.id, amount)

  await ctx.respond("You planted " + str(amount) + " nugget trees!")


#View market command
@nuggets_plugin.command()
@lightbulb.command("view_market", "See what all you can buy with your tasty nuggets!")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def view_market(ctx: lightbulb.Context):

  embed=(
    hikari.Embed(
      title="Market"
    )
    .set_footer(
      text="To buy a product, type /buy and the item and amount you want."
    )
  )
  plot_price = get_item(ctx.user.id, "plot_price")
  embed.add_field("Plots", str(plot_price) + " nuggets")
  await ctx.respond(embed)

#Buy command
@nuggets_plugin.command()
@lightbulb.option("item", "Item you want to buy", hikari.OptionType.STRING, required=True)
@lightbulb.option("amount", "The amount you want to buy", hikari.OptionType.INTEGER, required=True)
@lightbulb.command("buy", "Spend your hard earned nuggets on stuff!", pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def buy(ctx: lightbulb.Context, item: hikari.OptionType.STRING, amount: hikari.OptionType.INTEGER):

  total_nuggets = get_item(ctx.user.id, "nuggets")
  previous_plot_price = get_item(ctx.user.id, "plot_price")
  previous_plot_amount = get_item(ctx.user.id, "plots")

  plot_price = get_item(ctx.user.id, "plot_price")
  if item == "plots" or "plot":
    

    for x in range(amount):
      add_item(ctx.user.id, 1, "plots")
      set_plot_price(ctx.user.id)

    if total_nuggets >= plot_price:
      remove_item(ctx.user.id, plot_price, "nuggets")

      await ctx.respond("Purchased: " + str(amount) + " plots for " +
                       str(plot_price))
      return
    else:
        set_item(ctx.user.id, previous_plot_amount, "plots")
        set_item(ctx.user.id, previous_plot_price, "plot_price")

        await ctx.respond("You don't have enough nuggets to purchase")
        return

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
'''

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


'''
def add_tree(user_id, tree_amount):
  for key in db.keys():
    if key == str(user_id):
      if "trees" not in db[key]:
        db[key].update({"trees": tree_amount})
      else:
        db[key]["trees"] += tree_amount

      remove_item(user_id, tree_amount, "seeds")
      remove_item(user_id, tree_amount, "plots")

def set_item(user_id, amount, item):
  for key in db.keys():
    if key == str(user_id):
      if item not in db[key]:
        db[key].update({item: amount})
      else:
        db[key][item] = amount
'''
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

  for row in cursor.execute("SELECT * FROM users"):
    print(row)
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

'''

def remove_item(user_id, amount, item):
  for key in db.keys():
    if key == str(user_id):
      if item not in db[key]:
        db[key].update({item: amount})
      else:
        db[key][item] -= amount

def get_item(user_id, item):
  for key in db.keys():
    if key == str(user_id):
      if item not in db[key]:
        db[key].update({item: 0})

      return db[key][item]
'''
'''
def set_plot_price(user_id):
  modifier = 2
  last_price = get_item(user_id, "plot_price")
  new_price = last_price * modifier
  set_item(user_id, new_price, "plot_price")
'''


def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(nuggets_plugin)
