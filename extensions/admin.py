import hikari
import lightbulb

admin_plugin = lightbulb.Plugin("admin")

@admin_plugin.command()
@lightbulb.app_command_permissions(hikari.Permissions.ADMINISTRATOR)
@lightbulb.option("title", "Title of the message you want to post.", hikari.OptionType.STRING, required=True)
@lightbulb.option("message", "The message you want to post in an embed", hikari.OptionType.STRING, required=True)
@lightbulb.command("create_post", "Create an embeded post.", pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def create_post(ctx: lightbulb.Context, title: hikari.OptionType.STRING, message: hikari.OptionType.STRING):
  embed = (
    hikari.Embed()
  )

  embed.add_field(title, message)

  await ctx.respond(embed)

def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(admin_plugin)
