import json


class Config:
    """
    Give out config data (tokens & other constants) for this bot.

    If config.json not already set up, please set it up by following the steps in the README
    """

    def __init__(self):
        with open("config_log/config.json", "r") as f:
            self.data = json.loads(f.read())

    def discord(self) -> str:
        """
        Discord token that is given in config.json.
        """
        return self.data["discord_token"]

    def discord_test(self) -> str:
        """
        Testing bot discord token that is given in config.json.
        """
        return self.data["test_discord_token"]

    def client_test(self) -> str:
        """Testing bot client ID"""
        return self.data.test_client_id

    def client(self) -> str:
        """Main bot client ID"""

        return self.data.client_id

    def server_test(self) -> str:
        """Testing server ID"""

        return self.data.test_server_id

    def server(self) -> str:
        """Main client ID"""

        return self.data.server_id
