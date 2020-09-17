from bs4 import BeautifulSoup
import urllib.request as urllib
from discord.ext import commands
import os
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()
global token
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix="%")

    
ipltablepage = "https://www.iplt20.com/points-table/2020"


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


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord! ')

@bot.command(name='table', help='Returns the current IPL Table from IPLT20.com')
async def on_table_command(ctx):
    table = str(getIplTable())
    await ctx.send(table) 

bot.run(token)


