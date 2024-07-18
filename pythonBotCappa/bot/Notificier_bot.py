from telethon import TelegramClient, events, Button
from utils.setting import *
config = get_config()

# Создать клиент телеграм-бота
client = TelegramClient('', int(config["Telethon"]["api_id"]), config["Telethon"]["api_hash"]).start(
    bot_token=config["Telethon"]["bot_token2"])



