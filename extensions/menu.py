import hikari
import lightbulb
import miru
import random

from helper import user
from helper import database
from helper import manager
from helper import cooldown

class MenuView(miru.View):
    def __init__(self, collection_cooldown=True):
        super().__init__()
        self.embed = hikari.Embed()

        if collection_cooldown is False:
            self.collection.disabled = True
        else:
            self.collection.disabled  = False

    @miru.button(style=hikari.ButtonStyle.SUCCESS, label="Inventory")
    async def inventory(self, button: miru.Button, ctx: miru.Context) -> None:

        #Check if user is in database
        manager.refresh_user_info(ctx.user.id, ctx.user.username)

        #Build embed
        self.embed.title=f"{ctx.user.username}'s Nugget Inventory"
        
        player = user.User(ctx.user.id)
        self.embed.set_thumbnail(ctx.user.avatar_url)
        self.embed.description="Your Inventory:"
        self.embed.add_field("Nuggets", str(player.nuggets))
        self.embed.add_field("Seeds", str(player.seeds))
        self.embed.add_field("Plots", str(player.plots))
        self.embed.add_field("Trees", str(player.trees))
        self.embed.set_footer(f"{get_footer_text(ctx.user.id, ctx.user.username)} (Artwork by noion_art)")

        await ctx.edit_response(components=self.build())

        await ctx.edit_response(self.embed)
        
        self.embed._fields.clear()
        return
    
    @miru.button(style=hikari.ButtonStyle.PRIMARY, label="Collect Nuggets")
    async def collection(self, button: miru.Button, ctx: miru.Context) -> None:

        #create timer
        collection_timer = cooldown.Cooldown(minutes=1)
        collection_timer_name = f"{ctx.user.username}_collection_timer"
        collection_timer.update_user_timer(ctx.user.id, collection_timer_name)

        #Disable button
        button.disabled = True

        #Rebuild view
        await ctx.edit_response(components=self.build())

        manager.refresh_user_info(ctx.user.id, ctx.user.username)

        #Build embed
        self.embed.title=f"{ctx.user.username} Nugget Collection"

        self.embed.description=manager.collect_daily_nuggets(ctx.user.id)
        self.embed.set_thumbnail("https://i.redd.it/1yp58oe4pby61.png")
        self.embed.set_footer(f"{get_footer_text(ctx.user.id, ctx.user.username)} (Artwork by noion_art)")

        await ctx.edit_response(self.embed)
        return

    @miru.button(style=hikari.ButtonStyle.DANGER, label="Leaderboard")
    async def leaderboard(self, button: miru.Button, ctx: miru.Context) -> None:

        #Build embed

        self.embed.title="Most Collected Nuggets"
        
        self.embed.add_field("Leaderboard", "Placeholder")
        self.embed.description="Current Server Ranking"

        self.embed.edit_field(0, "Leaderboard", manager.get_leaderboard())
        self.embed.set_footer(f"{get_footer_text(ctx.user.id, ctx.user.username)}")

        await ctx.edit_response(components=self.build())
        await ctx.edit_response(self.embed)
        self.embed._fields.clear()
        return

    @miru.button(style=hikari.ButtonStyle.SECONDARY, label="Buy")
    async def buy(self, button: miru.Button, ctx: miru.Context) -> None:
        #Clear current view
        self.clear_items()
        await ctx.edit_response(components=self.build())

        #Build new view
        view = BuyView()
        message = await ctx.edit_response(components=view.build())
        await view.start(message)
        await view.wait()

    @miru.button(style=hikari.ButtonStyle.SECONDARY, label="Plant")
    async def plant(self, button: miru.Button, ctx: miru.Context) -> None:
        pass

class BuyView(miru.View):
    def __init__(self):
        super().__init__()
        self.embed = hikari.Embed()

    @miru.button(style=hikari.ButtonStyle.SECONDARY, label="Plots")
    async def plots(self, button: miru.Button, ctx: miru.Context) -> None:
        manager.refresh_user_info(ctx.user.id, ctx.user.username)
        player = user.User(ctx.user.id)
        player.set_plot_price(ctx.user.id)

        self.embed.title = f"Purchase a New Plot"
        self.embed.add_field(f"Current Plots", str(player.plots))
        self.embed.add_field("Plot Price Cost", str(player.plot_price))

        await ctx.edit_response(self.embed)

        #Clear current view
        self.clear_items()
        await ctx.edit_response(components=self.build())

        #Build new view
        view = BuyPlotView()
        message = await ctx.edit_response(components=view.build())
        await view.start(message)
        await view.wait()

    @miru.button(style=hikari.ButtonStyle.DANGER, label="Go Back")
    async def go_back(self, button: miru.Button, ctx: miru.Context) -> None:
        manager.refresh_user_info(ctx.user.id, ctx.user.username)

        self.embed.title="NUG Bot Menu"

        is_collection_on_cooldown = check_timer(ctx.user.id, ctx.user.username)

        self.embed.description=f"Hello {ctx.user.username}!"
        self.embed.set_footer(f"{get_footer_text(ctx.user.id, ctx.user.username)} until you can collect your daily nuggets")
        await ctx.edit_response(self.embed)

        #Clear current view
        self.clear_items()
        await ctx.edit_response(components=self.build())

        #Build new view
        view = MenuView(is_collection_on_cooldown)
        message = await ctx.edit_response(components=view.build())
        await view.start(message)
        await view.wait()

class BuyPlotView(miru.View):
    def __init__(self):
        super().__init__()
        self.embed = hikari.Embed()

    @miru.button(style=hikari.ButtonStyle.SECONDARY, label="Buy Plot")
    async def buy_plot(self, button: miru.Button, ctx: miru.Context) -> None:
        if manager.buy_plot(ctx.user.id) is True:
            self.embed.title="Purchase a New Plot!"
            self.embed.description="Plot purchased!"
            await ctx.edit_response(self.embed)

        else:
            self.embed.description="Not enough Nuggets!"
            await ctx.edit_response(self.embed)

    
        self.embed.title="NUG Bot Menu"

        #Clear current view
        self.clear_items()
        await ctx.edit_response(components=self.build())

        #Build new view
        view = BuyView()
        message = await ctx.edit_response(components=view.build())
        await view.start(message)
        await view.wait()


    @miru.button(style=hikari.ButtonStyle.DANGER, label="Go Back")
    async def go_back(self, button: miru.Button, ctx: miru.Context) -> None:
        manager.refresh_user_info(ctx.user.id, ctx.user.username)

        self.embed.title="NUG Bot Menu"

        #Clear current view
        self.clear_items()
        await ctx.edit_response(components=self.build())

        #Build new view
        view = BuyView()
        message = await ctx.edit_response(components=view.build())
        await view.start(message)
        await view.wait()

menu_plugin = lightbulb.Plugin("menu")

@menu_plugin.command()
@lightbulb.command("menu", "View the NUG Bot's menu")
@lightbulb.implements(lightbulb.SlashCommand)
async def menu(ctx: lightbulb.Context)->None:
    manager.refresh_user_info(ctx.user.id, ctx.user.username)

    embed=(hikari.Embed(title="NUG Bot Menu"))

    is_collection_on_cooldown = check_timer(ctx.user.id, ctx.user.username)

    view = MenuView(is_collection_on_cooldown)

    embed.description=f"Hello {ctx.user.username}!"
    embed.set_footer(f"{get_footer_text(ctx.user.id, ctx.user.username)} until you can collect your daily nuggets")


    message = await ctx.respond(embed, components=view.build())
    await view.start(message)
    await view.wait()

def get_footer_text(user_id, user_name)->str:
    collection_timer = cooldown.Cooldown(minutes=1)
    timer_name = f"{user_name}_collection_timer"
    footer = collection_timer.get_cooldown_text(user_id, timer_name)

    return footer

def check_timer(user_id, user_name)->bool:
    #Get timer
    collection_timer = cooldown.Cooldown(minutes=1)
    collection_timer_name = f"{user_name}_collection_timer"
    is_collection_on_cooldown = collection_timer.check_if_on_cooldown(user_id, collection_timer_name)

    return is_collection_on_cooldown


def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(menu_plugin)