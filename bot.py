# IMPORTS 
from bs4 import BeautifulSoup
import urllib.request as urllib
from discord.ext import commands
import os
from dotenv import load_dotenv
from tabulate import tabulate
import requests
import json
import csv
import datetime
import time

"""
DISCORD BOT for the Indian Premier League
Copyright Dhruv Venkataraman
"Indian Premier League" is a trademark of the BCCI. I am in no way associated with the BCCI or the IPL. 
"Discord" is a trademark of Discord, Inc
Please read the "LICENSE" associated with this Repository for more information. 
"""

# CONSTANTS (DISCORD TOKEN, Bot Object, important URLs)
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="%")
moDict = {"sep":9, "oct":10, "nov":11}
matches = []   
ipltablepage = "https://www.iplt20.com/points-table/2020"


# UTILITY FUNCTIONS TO INTERACT WITH APIs - CricBuzz and IPLT20.com


def shorthand(tName):
    shortName = ""
    if tName == "sunrisers hyderabad":
        return "srh"
    elif tName == "kings xi punjab":
        return "kxip"
    else:
        for word in tName.split(" "):
            shortName+= word[0]
        return shortName

def map_month_to_date(mo: str):                                                    
    mo = mo.lower()
    return moDict[mo]

def csv_file_read():
    with open("sched.csv",mode="r") as file:
        global matches
        scores = csv.reader(file, delimiter=",")
        for row in scores:
            day = int(row[0].split("-")[0])
            mo = int(list(map(map_month_to_date, [row[0].split("-")[1]]))[0])
            hr = int(row[1].split(":")[0]) + 12
            hr = int(hr)
            mi = int(row[1].split(":")[1][0:2])
            finalTime = datetime.datetime(2020,mo,day,hr,mi,0).timestamp()
            t1 = shorthand(row[3].lower())
            t2 = shorthand(row[4].lower())
            matches.append([finalTime,t1,t2,row[5].lower()])

def get_from_url(url):
    return requests.get(url).json()

def find_next_match(*args):
    pass
    
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
    return(tabulate(attrList, headers=tableHeadersNew, tablefmt='simple'))

def get_live_score():
    matches = get_from_url("https://mapps.cricbuzz.com/cbzios/match/livematches")['matches']
    curMatches = []
    for match in matches:
        if match['series_name'] == "Indian Premier League 2020": 
            if match['header']['status'] == "preview" or match['header']['state'] == "preview":
                curMatches.append(match)
            else:
                curMatches.append(match)
    if len(curMatches) < 1 :
        return "No IPL Match found"
    else:
        return curMatches

def get_next_match(args):
    global matches
    curTime = int(time.time())
    if len(args) < 1:
        for match in matches:
            if match[0] >= curTime:
                return match
    else:
        for match in matches:
            if match[0] >= curTime and (match[1] == args[0].lower() or match[2] == args[0].lower()):
                return match
    return None      

# DISCORD BOT COMMANDS FOLLOW 
@bot.event
async def on_ready():
    csv_file_read()
    print(f'{bot.user} has connected to Discord! ')
    #print(matches)

@bot.command(name='table', help='Returns the current IPL Table from IPLT20.com')
async def on_table_command(ctx):
    table = str(getIplTable())
    await ctx.send("```"+table+"```")
    print(table)

@bot.command(name='score', help='Returns the score of the current match. Data scraped from IPLT20.com')
async def on_score_command(ctx):
    prop = get_live_score()
    await ctx.send(prop)

@bot.command(name='nextmatch', help='Returns the next match of PARAM. Usage: %nextmatch TEAMNAME. If no NAME is supplied, the next match will be returned')
async def on_nextmatch_command(ctx, *args):
    matchObj = get_next_match(args=args)
    if matchObj is not None:
        await ctx.send("Next match is "+ matchObj[1].upper() + " versus "+ matchObj[2].upper() + " at " + matchObj[-1].capitalize() + " "+  str(time.asctime(time.localtime(int(matchObj[0])))))
    else:
        await ctx.send("No team with that name found. Perhaps you typed a wrong team name?")

@bot.command(name='github', help='The GitHub repo for this bot!')
async def github_command(ctx):
    await ctx.send('VIsit https://github.com/dhruvv/IPLDiscordBot to see the bot!')

@bot.command(name='joinvc')
async def voicejoin(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

bot.run(token)


