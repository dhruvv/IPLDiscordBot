# IMPORTS 
from bs4 import BeautifulSoup
import urllib.request as urllib
from discord.ext import commands
import os
from dotenv import load_dotenv
from tabulate import tabulate
import requests
import json

# CONSTANTS (DISCORD TOKEN, Bot Object, important URLs)
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="%")

    
ipltablepage = "https://www.iplt20.com/points-table/2020"

# UTILITY FUNCTIONS TO INTERACT WITH APIs - CricBuzz and IPLT20.com


def get_from_url(url):
    return requests.get(url).json()

def getIplTable():
    ipltableData = urllib.urlopen(ipltablepage)
    soup = BeautifulSoup(ipltableData, 'html.parser')
    iplTable = soup.find('table', attrs={'class':'standings-table'})
    #print(iplTable.prettify())
    iplTableByPos = iplTable.find_all('tr')
    tableHeadersOld = iplTableByPos[0]
    tableHeadersNew = []
    for th in tableHeadersOld.find_all('th'):
        d = th.contents
        if len(d) < 1:
            tableHeadersNew.append(" ")
        else:
            tableHeadersNew.append(d[0])
    iplTableByPos.pop(0)
    attrList = []
    for pos in iplTableByPos:
        tdList = pos.find_all('td')
        posList = []
        for td in tdList:
            c = td.contents
            if len(c) > 4:
                tName = c[3].find('span',attrs={'class':'standings-table__team-name--short'}).contents
                posList.append(tName[0])
            else:
                if len(c) < 1:
                    posList.append("N/A")
                else:
                    posList.append(c[0])
        posList.pop(-1)
        attrList.append(posList)
    return(tabulate(attrList, headers=tableHeadersNew, tablefmt='github'))


def get_live_score():
    matches = get_from_url("https://mapps.cricbuzz.com/cbzios/match/livematches")['matches']
    for match in matches:
        if match['series_name'] == "Indian Premier League 2020": 
            try :
                if match['state'] != "preview" or match['header']['state'] != "preview":
                    matchprop = match
                    return matchprop
                else:
                    return "No IPL Match in progress, though one is scheduled soon"
            except KeyError:
                return "Match state not found"
        else:
            return "No IPL Match found      "
    


# DISCORD BOT COMMANDS FOLLOW 
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord! ')

@bot.command(name='table', help='Returns the current IPL Table from IPLT20.com')
async def on_table_command(ctx):
    table = str(getIplTable())
    await ctx.send("```"+table+"```") 

@bot.command(name='score', help='Returns the score of the current match. Data scraped from IPLT20.com')
async def on_score_command(ctx):
    prop = get_live_score()
    await ctx.send(prop)

@bot.command(name='nextmatch', help='Returns the next match of PARAM. Usage: %nextmatch TEAMNAME')
async def on_nextmatch_command(ctx, teamname):
    await ctx.send('Next match command invoked with ' + teamname + ' as param')


@bot.command(name='github', help='The GitHub repo for this bot!')
async def github_command(   ctx):
    await ctx.send('VIsit https://github.com/dhruvv/IPLDiscordBot to see the bot!')

bot.run(token)


