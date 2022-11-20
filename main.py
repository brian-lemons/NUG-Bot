import os
import hikari
import lightbulb
import aiohttp
import dotenv 
import asyncio

dotenv.load_dotenv()



secret_guild = os.environ['SECRET_GUILD']
bot = lightbulb.BotApp(
  os.environ["DISCORD_BOT_SECRET"],
  intents=hikari.Intents.ALL,
)
  
bot.load_extensions_from("./extensions/")
  
  
@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
  bot.d.aio_session = aiohttp.ClientSession()
  
  
@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
  await bot.d.aio_session.close()

bot.run()

