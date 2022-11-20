import os
import hikari
import lightbulb
import aiohttp
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

import os 


secret_guild = int(os.environ['SECRET_GUILD'])
bot = lightbulb.BotApp(token=os.environ['DISCORD_BOT_SECRET'],
                         default_enabled_guilds=(secret_guild))
  
bot.load_extensions_from("./extensions/")
  
  
@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
  bot.d.aio_session = aiohttp.ClientSession()
  
  
@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
  await bot.d.aio_session.close()

bot.run()

