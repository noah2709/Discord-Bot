import json
from types import SimpleNamespace
from typing import List



class ConfigError(Exception):
    def __init__(self, *missing_keys: object) -> None:
        self.missing_keys = missing_keys

    def __str__(self):
        return f"Config variable '{self.missing_keys}' doesn't exist"


class Config(SimpleNamespace):
    def __init__(self):
        config = self._get_config()
        try:
            self.token: str = config['token']
            self.api_key: str = config['api_key']

            self.moderation_roles: List[int] = [
                int(role_id)
                for role_id in config['moderation_roles']
            ]
            self.prefix: str = config['bot_prefix']

            self.welcome_channel: str = config['welcome_channel']
        except KeyError as error:
            raise ConfigError(*error.args)

    def _get_config(self):
        with open("./my_bot/config.json") as file:
            return json.load(file)
