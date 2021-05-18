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
   token            = 'ENTER YOUR DISCORD TOKEN',
   api_key          = 'ENTER YOUR RIOT API KEY',
   
   bot_prefix       = 'SET YOUR BOT PREFIX',
   
   welcome_channel  = 'SET YOUR WELCOME CHANNEL ID'
   ```

 ## TODO LIST

- [x] Debug the restart command ( end the loop if restarted )
- [ ] Add the free champion rotation to the bot
- [x] Rewrite the welcome.py ( Read the welcome channel directly from the config )
- [ ] Let users register their lol Account to see information about theirselfes
- [ ] Add "Live Game" to the bot ( To check the enemys while ingame )
