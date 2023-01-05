import hikari
import lightbulb
import miru
import random

from helper import user
from helper import database
from helper import manager
from helper import cooldown

class MenuView(miru.View):
    def __init__(self):
        super().__init__()

class InventoryButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(style=hikari.ButtonStyle.SUCCESS, label="Inventory")

    async def callback(self, ctx: miru.ViewContext) -> None:
        embed = (hikari.Embed(title=f"{ctx.user.username}'s Nugget Collection"))
        #Check if user is in database
        manager.refresh_user_info(ctx.user.id, ctx.user.username)
        
        player = user.User(ctx.user.id)
        embed.set_thumbnail(ctx.user.avatar_url)
        embed.add_field("Nuggets", str(player.nuggets))
        embed.add_field("Seeds", str(player.seeds))
        embed.add_field("Plots", str(player.plots))
        embed.add_field("Trees", str(player.trees))

        await ctx.edit_response(embed)
        return

class LeaderboardButton(miru.Button):
    def __init__(self) -> None:
        super().__init__(style=hikari.ButtonStyle.DANGER, label="Leaderboard")

    async def callback(self, ctx: miru.ViewContext) -> None:
        embed = (
            hikari.Embed(
                title="Most Collected Nuggets",)
                .add_field("Leaderboard", "Placeholder")
        )

        embed.edit_field(0, "Leaderboard", manager.get_leaderboard())
        await ctx.edit_response(embed)
        return

class DailyNuggetCollectionButton(miru.Button):
    def __init__(self, collection_cooldown:bool) -> None:
        super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Collect Nuggets")

        if collection_cooldown is False:
            self.disabled = True
        else:
            self.disabled = False

    async def callback(self, ctx: miru.ViewContext) -> None:
        embed=(hikari.Embed(title=f"{ctx.user.username} Nugget Collection"))

        #create timer
        collection_timer = cooldown.Cooldown(hours=23)
        collection_timer_name = f"{ctx.user.username}_collection_timer"
        collection_timer.update_user_timer(ctx.user.id, collection_timer_name)

        #Disable button
        self.disabled = True

        #Rebuild view
        await ctx.edit_response(components=ctx.view)

        manager.refresh_user_info(ctx.user.id, ctx.user.username)

        embed.description=manager.collect_daily_nuggets(ctx.user.id)
        embed.set_thumbnail("https://i.redd.it/1yp58oe4pby61.png")
        embed.set_footer(f"{get_footer_text(ctx.user.id, collection_timer_name)} until you can collect your daily nuggets!(Artwork by noion_art)")

        await ctx.edit_response(embed)
        return

menu_plugin = lightbulb.Plugin("menu")

@menu_plugin.command()
@lightbulb.command("menu", "View the NUG Bot's menu")
@lightbulb.implements(lightbulb.SlashCommand)
async def menu(ctx: lightbulb.Context)->None:
    manager.refresh_user_info(ctx.user.id, ctx.user.username)

    embed=(hikari.Embed(title="NUG Bot Menu"))

    #Get timer
    collection_timer = cooldown.Cooldown(hours=23)
    collection_timer_name = f"{ctx.user.username}_collection_timer"
    is_collection_on_cooldown = collection_timer.check_if_on_cooldown(ctx.user.id, collection_timer_name)

    view = MenuView()
    view.add_item(InventoryButton())
    view.add_item(DailyNuggetCollectionButton(is_collection_on_cooldown))
    view.add_item(LeaderboardButton())

    embed.description=f"Hello {ctx.user.username}!"
    embed.set_footer(f"{get_footer_text(ctx.user.id, collection_timer_name)} until you can collect your daily nuggets")


    message = await ctx.respond(embed, components=view.build())
    await view.start(message)
    await view.wait()

def get_footer_text(user_id, timer_name):
    collection_timer = cooldown.Cooldown(hours=23)
    footer = collection_timer.get_cooldown_text(user_id, timer_name)

    return footer


def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(menu_plugin)