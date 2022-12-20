import hikari
import lightbulb
import random

pokemon_plugin = lightbulb.Plugin("pokemon")

@pokemon_plugin.command()
@lightbulb.command("random_type", "Get a random pokemon type")
@lightbulb.implements(lightbulb.SlashCommand)
async def random_type(ctx: lightbulb.Context):
    types = ['Normal',
            'Fighting',    
            'Flying',    
            'Poison',    
            'Ground',    
            'Rock',    
            'Bug',    
            'Ghost',    
            'Steel',    
            'Fire',    
            'Water',    
            'Grass',    
            'Electric',    
            'Psychic',    
            'Ice',    
            'Dragon',    
            'Dark',    
            'Fairy']

    random_pokemon_type = random.choice(types)

    await ctx.respond(random_pokemon_type)

def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(pokemon_plugin)