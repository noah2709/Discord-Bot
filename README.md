<!-- GETTING STARTED -->
## Getting Started

To use this bot for your own you need to follow these steps.
First of all you need to create a config.json file in the my_bot folder.

### Installation

1. Get a free API Key at [https://discord.com/developers]
2. Get a free RIOT API Key at [https://developer.riotgames.com/]
3. Clone the repo
   ```sh
   git clone https://github.com/Taikador/Taikador-Bot
   ```
4. Enter your variables in `config.js`
   ```JS
   "token"            = 'ENTER YOUR DISCORD TOKEN',
   "api_key"          = 'ENTER YOUR RIOT API KEY',
   "guild_id"         = 'ENTER YOUR GUILD ID',
   
   "bot_prefix"       = 'SET YOUR BOT PREFIX',
   
   "welcome_channel"  = 'SET YOUR WELCOME CHANNEL ID',
   "rota_channel_id"  = 'SET YOUR ROTA CHANNEL ID',
   "moderation_roles" = ['ROLE ONE', 'ROLE TWO']
   ```
5. Create a db.json file

 ## TODO LIST

- [x] Debug the restart command ( end the loop if restarted )
- [x] Add the free champion rotation to the bot
- [x] Rewrite the welcome.py ( Read the welcome channel directly from the config )
- [x] Let users register their lol Account to see information about theirselfes
- [x] Add the new commands to the custom help command
- [ ] Add "Live Game" to the bot ( To check the enemys while ingame )
- [ ] Rewrite the lolinfo command ( Get the code cleaner with more custom functions (In Progress...))
