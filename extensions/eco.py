import lightbulb
import math
import hikari
from typing import Optional

infrastructure_plugin = lightbulb.Plugin("infrastructure")

@infrastructure_plugin.command
@lightbulb.option("terraforming_level", "Your current terra level", hikari.OptionType.INTEGER, required=True)
@lightbulb.option("natural_resources", "The current stars Natural Resources", hikari.OptionType.INTEGER, required=True)
@lightbulb.option("current_eco", "Current Infrastructure already built", hikari.OptionType.INTEGER, required=True)
@lightbulb.option("current_ind", "Current Infrastructure already built", hikari.OptionType.INTEGER, required=True)
@lightbulb.option("current_sci", "Current Infrastructure already built", hikari.OptionType.INTEGER, required=True)
@lightbulb.option("economy", "Level of economy infrastructure to improve to", hikari.OptionType.INTEGER, required=True)
@lightbulb.option("industry", "Level of industry infrastructure to improve to", hikari.OptionType.INTEGER, required=True)
@lightbulb.option("science", "Level of science infrastructure to improve to", hikari.OptionType.INTEGER, required=True)
@lightbulb.option("expense_config", "Expense config", hikari.OptionType.INTEGER, required=False)
@lightbulb.command("infrastructure", "Calculate the amount of savings you get with a terra boost!", pass_options=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def infrastructure(ctx: lightbulb.Context,
terraforming_level: hikari.OptionType.INTEGER,
natural_resources: hikari.OptionType.INTEGER,
current_eco: hikari.OptionType.INTEGER,
current_ind: hikari.OptionType.INTEGER, 
current_sci: hikari.OptionType.INTEGER,                         
economy: hikari.OptionType.INTEGER,
industry: hikari.OptionType.INTEGER,
science: hikari.OptionType.INTEGER,
expense_config: Optional[int] = None,
):
    #Set base costs
    baseCost = {
        "Warp Gates": 50,
        "Economy": 2.5,
        "Industry": 5,
        "Science": 20,
        "Carriers": 10,
        "Expense Config": 2,
    }
 
    #Calculate current terra resources
    def calculate_current_terra_resources(natural_resources, terraforming_level):
        terraformedResources = math.floor(natural_resources + (5 * terraforming_level))
        return terraformedResources


    #calculate current infra cost
    def calculate_eco_upgrade_cost(ecoBaseCost, expenseConfig, current_eco, terraformedResources, upgrade_to):
      current_upgrade_cost = 0
      ecoUpgradeCost = 0
      total_infra  = current_eco
      upgrade_dif = upgrade_to - current_eco

      for x in range(upgrade_dif):
        current_upgrade_cost = max(1, math.floor((ecoBaseCost * expenseConfig * (current_eco + 1)) / (terraformedResources / 100)))
        total_infra +=1
        ecoUpgradeCost += current_upgrade_cost
      return ecoUpgradeCost

    def calculate_ind_upgrade_cost(indBaseCost, expenseConfig, current_ind, terraformedResources, upgrade_to):
      current_upgrade_cost = 0
      indUpgradeCost = 0
      total_infra  = current_ind
      upgrade_dif = upgrade_to - current_ind
      
      for x in range(upgrade_dif):
        current_upgrade_cost = max(1, math.floor((indBaseCost * expenseConfig * (current_ind + 1)) / (terraformedResources / 100)))
        total_infra +=1
        indUpgradeCost += current_upgrade_cost
      return indUpgradeCost

    def calculate_science_upgrade_cost(scienceBaseCost, expenseConfig, current_sci, terraformedResources, upgrade_to):
      current_upgrade_cost = 0
      scienceUpgradeCost = 0
      total_infra  = current_sci
      upgrade_dif = upgrade_to - current_sci
      
      for x in range(upgrade_dif):
        current_upgrade_cost = max(1, math.floor((scienceBaseCost * expenseConfig * (total_infra  + 1)) / (terraformedResources / 100)))
        total_infra +=1
        scienceUpgradeCost += current_upgrade_cost
      return scienceUpgradeCost

    terraformedResources = calculate_current_terra_resources(natural_resources, terraforming_level)
    ecoUgradeCost = calculate_eco_upgrade_cost(baseCost.get("Economy"), baseCost.get("Expense Config"), current_eco, terraformedResources, economy)
    indUpgradeCost = calculate_ind_upgrade_cost(baseCost.get("Industry"), baseCost.get("Expense Config"), current_ind, terraformedResources, industry)
    scienceUpgradeCost = calculate_science_upgrade_cost(baseCost.get("Science"), baseCost.get("Expense Config"), current_sci, terraformedResources, science)

    embed = (
      hikari.Embed(
        title="Infrastructure Upgrade Cost",
      )
      .add_field(
        "Eco Upgrade Cost", str(ecoUgradeCost),
        inline=True,
      )
      .add_field(
        "Industry Upgrade Cost", str(indUpgradeCost),
        inline=True,
      )
      .add_field(
        "Science Upgrade Cost", str(scienceUpgradeCost),
        inline=True,
      )
    .add_field(
        "Terraforming Level", str(terraforming_level),
      )        
    .add_field(
          "Old Economy", str(current_eco),
          inline=True,
      )
    .add_field(
          "Old Industry", str(current_ind),
          inline=True,
      )   
    .add_field(
          "Old Science", str(current_sci),
          inline=True,
      )   
    .add_field(
        "Natural Resources", str(natural_resources),
      )
    .add_field(
          "New Economy Infrastructure", str(economy),
          inline=True,
      )
    .add_field(
          "New Industry Infrastructure", str(industry),
          inline=True,
      )   
    .add_field(
          "New Science Infrastructure", str(science),
          inline=True,
      )   
    )

    await ctx.respond(embed)

def load(bot: lightbulb.BotApp) -> None:

  bot.add_plugin(infrastructure_plugin)
