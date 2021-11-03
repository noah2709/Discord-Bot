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
4. Enter your variables in `config.js` you have to create that file in [my_bot]
   ```JS
   "token"            = 'ENTER YOUR DISCORD TOKEN',
   "api_key"          = 'ENTER YOUR RIOT API KEY',
   "guild_id"         = 'ENTER YOUR GUILD ID',
   
   "bot_prefix"       = 'SET YOUR BOT PREFIX',
   
   "welcome_channel"  = 'SET YOUR WELCOME CHANNEL ID',
   "rota_channel_id"  = 'SET YOUR ROTA CHANNEL ID',
   "patch_notes_channel_id" = 'SET YOUR PATCHNOTE CHANNEL ID'
   "moderation_roles" = ['ROLE ONE', 'ROLE TWO']
   "guild_id": 'ENTER YOUR SERVER ID'
   ```
5. Create a `db.json` file (in [data])

 ## TODO LIST

- [x] Debug the restart command ( end the loop if restarted )
- [x] Add the free champion rotation to the bot
- [x] Rewrite the welcome.py ( Read the welcome channel directly from the config )
- [x] Let users register their lol Account to see information about theirselfes
- [x] Add the new commands to the custom help command
- [x] Rewrite the lolinfo command ( Get the code cleaner with more custom functions )
- [x] Fix new gitpull command ( Can't restart the bot anymore ( while loop isn't working ))
- [x] Add Patchnotes
- [ ] Add multiple Team Search
