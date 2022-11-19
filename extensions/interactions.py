import hikari
import lightbulb
import random
from typing import Optional

interactions_plugin = lightbulb.Plugin("interactions")

@interactions_plugin.command
@lightbulb.option(
    "user", "The user to attack!", hikari.User, required=False
)
@lightbulb.command("swordattack", "Do a sword attack against another user!", pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def swordattack(ctx: lightbulb.Context, user: Optional[hikari.User] = None) -> None:

    #Get random damage
    damage = random.randrange(1, 1000)

    embed = (
        hikari.Embed(
            title=f"{ctx.author.username} Attacks!",
        )
        .set_footer(

            text=f"Requested by {ctx.author.username}",

            icon=ctx.author.display_avatar_url,
        )
        .set_thumbnail(user.avatar_url)
        .add_field(
            "AHHHHHHHHHHHHHH",
            f"╰(⇀︿⇀)つ-]═─── {user.mention}",
        )
        .add_field(
            "Damage Dealt:",
            str(damage),
        )
    )
    await ctx.respond(embed)

@interactions_plugin.command
@lightbulb.option(
    "user", "The user to attack!", hikari.User, required=False
)
@lightbulb.command("snipe", "Snipe another user!", pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def snipe(ctx: lightbulb.Context, user: Optional[hikari.User] = None) -> None:

    #Get random damage
    damage = random.randrange(1, 1000)

    embed = (
        hikari.Embed(
            title=f"{ctx.author.username} Attacks!",
        )
        .set_footer(

            text=f"Requested by {ctx.author.username}",

            icon=ctx.author.display_avatar_url,
        )
        .set_thumbnail(user.avatar_url)
        .add_field(
            "PEWWWWWWWWWWW",
            f"(๑>◡╹)︻┳═一 {user.mention}",
        )
        .add_field(
            "Damage Dealt:",
            str(damage),
        )
    )
    await ctx.respond(embed)

@interactions_plugin.command
@lightbulb.option(
    "user", "The user to attack!", hikari.User, required=False
)
@lightbulb.command("magic_attack", "Cast a spell at another user!", pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def magic_attack(ctx: lightbulb.Context, user: Optional[hikari.User] = None) -> None:

    #Get random damage
    damage = random.randrange(1, 1000)

    embed = (
        hikari.Embed(
            title=f"{ctx.author.username} Attacks!",
        )
        .set_footer(

            text=f"Requested by {ctx.author.username}",

            icon=ctx.author.display_avatar_url,
        )
        .set_thumbnail(user.avatar_url)
        .add_field(
            "WATER, WATER, FROTH AND FOAM!",
            f"ଘ(๑˃ᴗ˂)━☆ﾟ.*･☆*｡ﾟ {user.mention}",
        )
        .add_field(
            "Damage Dealt:",
            str(damage),
        )
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(interactions_plugin)
