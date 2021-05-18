#-*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2021 Taikador

Special thanks to coma64 for his extraordinary help.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files, to deal in the
Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so, subject
of the following conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.


THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import logs
import asyncio
import discord
from typing import Optional
from pathlib import Path
from os import listdir
from logging import getLogger
from config import Config


from discord import Guild
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.errors import CheckFailure, CommandNotFound

log = getLogger('mybot')

class Bot(commands.Bot):

    def __init__(self, config: Config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logs.setup()
        self.config = config

        self.extension_path: Path = Path(__file__).parent / 'extensions'

        self.guild: Optional[Guild] = None
        self._guild_available = asyncio.Event()

        self.signature = 'Bot created by: Taikador'

        self.load_extensions()

    def load_extensions(self) -> None:
    
        for file in listdir(self.extension_path):
            if file.endswith(".py"):
                name = file[:-3]
                self.load_extension(
                    f'extensions.{name}'
                )

    def add_gog(self, cog: Cog) -> None:
        super().add_cog(cog)
        log.info(f'Cog loaded: {cog.qualified_name}')

    async def on_ready(self) -> None:
        log.info(f'Logged in as {self.user}')

        await self.wait_until_guild_available()
        log.info('Now serving in guild: ' + next(guild.name for guild in self.guilds if guild.id == bot.config.guild_id))
    
    async def on_error(self, event: str, *args, **kwargs) -> None:
        log.exception(f'Unhandled exception in {event}')

    async def on_command_error(self, context, exception) -> None:
        if isinstance(exception, CheckFailure):
            log.info(f'Check failed for user {context.author}: {exception}')
        elif isinstance(exception, CommandNotFound):
            pass
        else:
            log.exception(f'Unhandled "{type(exception)}" exception: {exception}')
    
    async def wait_until_guild_available(self) -> None:
        """
        Wait until the `config.guild_id` guild is available (and the cache is ready).
        The on_ready event is inadequate because it only waits 2 seconds for a GUILD_CREATE
        gateway event before giving up and thus not populating the cache for unavailable guilds.
        """
        await self._guild_available.wait()

if __name__ == "__main__":
    config = Config()
    bot = Bot(
        config,
        command_prefix= config.prefix, 
        case_insensitive=True, 
        intents=discord.Intents.all(),
        help_command=None
    )
    bot.run(bot.config.token)