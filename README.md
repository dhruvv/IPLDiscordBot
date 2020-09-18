# IPL Discord Bot
 The server code for an IPL Discord Bot. Can respond to commands for the table, live commentary, scheduled matches of a team, etc

 Current working commands
 ```discord
 %help 
 %table - the current IPL table, scraped from IPLT20.com
 ```
 Commands referenced in code but func is not complete:
 ```
 %nextmatch TEAMNAME
 %score
 ```

 ## Inviting the Bot to your Discord Guild

 As of right now, you can't! But within a few days I hope to finish the bot and make it inviteable. 
 
## Using the Bot Script on your own
If you want to run the bot on your own server and create your own version of the IPL Bot, you need to do a few things.

### Acquire a Discord Bot Token from Discord Developers

Go to https://discord.com/developers and sign in with your Discord account. Once you get to the "Create an Application" Screen, create one, name it etc. Then go to "Create a Bot", name your bot whatever you want, and then copy the Authentication Token that is generated, just below the profile picture of your bot. 

### Fork the Repo and install dependencies
IPL Bot uses Python 3.8.5 and the following modules:
```
beautifulsoup4
python-dotenv
discord.py
tabulate
``` 
You can install these using 
```bash
$ pip3 install -u beautifulsoup4 python-dotenv discord.py tabulate
```
Then, use Git to clone this repository, using
```bash
$ git clone https://github.com/dhruvv/IPLDIscordBot.git
```
### Adding your Authentication Token to the Application
In the same directory as the `bot.py` file, create a new file called `.env` 

```bash
$ nano .env
```
Place your auth token in to the file in this format, (without curly braces)

```shell
DISCORD_TOKEN={INSERT DISCORD TOKEN HERE}
```
Now you are ready to run the bot. The bot runs in blocking loop, whicb will block your terminal, so it is recommended to run it in Tmux or Screen and detach it. 
```bash
$ python3 bot.py
```

Your bot should now, if in a server, respond to commnads, prefixed with `%`! Have fun!
