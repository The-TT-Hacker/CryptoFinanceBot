from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from time import sleep
import json

import os
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

'''
Gets cryptocurrency data from CoinMarketCap API
as JSON, converts to object and returns this
'''
def get_crypto_data(query):
    # https://coinmarketcap.com/api/documentation/v1/#

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'10',
    'convert':'AUD'
    }
    headers = {
    'Accepts': 'application/json',
    'Accept-Encoding': 'deflate, gzip',
    'X-CMC_PRO_API_KEY': '971768f9-fc4a-4166-9a71-249e89d36138',
    }

    session = Session()
    session.headers.update(headers)

    # while True:
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        with open('output.log', 'w') as out:    # logs the entirety of each request in a file
            out.write(json.dumps(data, indent=4))
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        # sleep(10)

    for obj in data['data']:
        if obj['symbol'] == query:
            output = obj
            break
    else:
        print("Requested cryptocurrency not found")
    
    print(output)
    return output


# Connecting to discord
# bot token is stored in environment variable for security reasons
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# every command must be prefixed with a !
bot = commands.Bot(command_prefix='!')

client = discord.Client()

'''
Defines a 'watch' task which provides hourly updates 
on chosen cryptocurrencies in a chosen channel, set by a user
'''
@tasks.loop(hours=1)
async def crypto_update():
    channel = bot.get_channel(793053168304783440)
    query = "BTC"
    crypto_data = get_crypto_data(query)
    await channel.send(crypto_data)

'''
Displays when the bot is connected and 
ready on console output
'''
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    # crypto_update.start()

@bot.command(name="crypto")
async def crypto_view(ctx, *args):
    if len(args) == 0:
        await ctx.send("Please input a cryptocurrency code")
    else:
        crypto_data = get_crypto_data(args[0])
        if crypto_data['platform'] == None:
            platform = "None"
        else:
            platform = crypto_data['platform']['name']
        
        await ctx.send("**Name:** " + crypto_data['name'])
        await ctx.send("―――――――――――――")
        await ctx.send("**Current Price**: " + str( '{:,.2f}'.format(crypto_data['quote']['AUD']['price']) + "\n" 
        + "**CoinMarketCap Rank**: " + str(crypto_data['cmc_rank'])) + "\n"
        + "**Platform**: " + platform)

        if len(args) > 1:
            if args[1] == "-extra":
                await ctx.send("―――")
                volume_24h = str( '{:,.2f}'.format(crypto_data['quote']['AUD']['volume_24h']) )
                change_1h = str( '{:,.2f}'.format(crypto_data['quote']['AUD']['percent_change_1h']) )
                change_24h = str( '{:,.2f}'.format(crypto_data['quote']['AUD']['percent_change_24h']) )
                change_7d = str( '{:,.2f}'.format(crypto_data['quote']['AUD']['percent_change_7d']) )
                
                extra_info = f"""
**Volume Traded Last 24 Hours**: {volume_24h}
**Percent Change Last 1 Hour**: {change_1h}
**Percent Change Last 24 Hours**: {change_24h}
**Percent Change Last 7 Days**: {change_7d}
                """ 
                await ctx.send(extra_info)
        
            elif args[1] == "-supply":
                await ctx.send("―――")
                max_supply = str( '{:,.0f}'.format(crypto_data['max_supply']) )
                circulating_supply = str( '{:,.0f}'.format(crypto_data['circulating_supply']) )
                total_supply = str( '{:,.0f}'.format(crypto_data['total_supply']) )

                supply_info = f"""
**Max Supply**: {max_supply}
**Circulating Supply**: {circulating_supply}
**Total Supply**: {total_supply}
                """
                await ctx.send(supply_info)
            
            elif args[1] == "-link":
                await ctx.send("―――")
                await ctx.send(f"https://coinmarketcap.com/currencies/{crypto_data['name']}")


        
# '''
# Checks if particular commands are present in each message,
# and sends responses accordingly 
# '''
# @bot.event
# async def on_message(message):
#     if message.content.startswith("!crypto"):
#         query_list = message.content.split(" ")
#         if len(query_list) == 1:
#             await message.channel.send("Please input a cryptocurrency code")
#         else:
#             crypto_data = get_crypto_data(query_list[1])
#             await message.channel.send("**Name:** " + crypto_data['name'])
#             await message.channel.send("------------------")
#             await message.channel.send("**Current Price**: " + str( '{:,.2f}'.format(crypto_data['quote']['AUD']['price']) ))
#             await message.channel.send("**CoinMarketCap Rank**: " + str(crypto_data['cmc_rank']))
#             # await message.channel.send(crypto_data['quote'])


# Error Handling
@bot.event
async def on_error(event, *args, **kwargs):
    # output error to err.log file
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise Exception

bot.run(TOKEN)

    