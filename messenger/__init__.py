import json
from pathlib import Path

from pyrogram import Client, Filters

config_path = Path("..") / '.sp_config'
config_file = config_path / 'config.json'
config = json.load(config_file.open())

API_KEY = config['telegram-api-token']

app = Client(config['bot-name'],
             api_id=config['api_id'],
             api_hash=config['api_hash'],
             bot_token=API_KEY
             )


@app.on_message(Filters.command("start"))
def start(client, message):
    pass


@app.on_message(Filters.command("help"))
def help(client, message):
    print(message.from_user)
    message.reply_text('''
    Hi! I'm progression bot, here to communicate with your raspberry pi.
    
Available commands:
/refresh - Redraw eInk display
/addevent - Add event to calendar
/switch - Switch display type
    ''')


@app.on_message(Filters.command("hello"))
def hello(client, message):
    message.reply_text("Hello {}".format(message.from_user.first_name))


if __name__ == '__main__':
    print(config)
    app.run()
