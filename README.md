# Brawl stats discord bot

Self-hosted discord bot for getting in-game statistics; built in python, using the ``nextcord`` package (among other packages)

Just install all prerequisites, and then run

```bash
touch config_log/config.json
```

Open the json file in your editor of choice and add in the following entries:

```json
{
    "discord_token": "token_here",
    "brawl_token": "token_here",
    "client_id":"token_here",
    "server_id":"token_here"
}
```

And... you're done! To turn on the bot, just type out 

```bash
python main.py
```

Given everything is set up correctly, the bot should function.
