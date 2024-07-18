from bot import Notificier_bot, Regauth_bot
from bot.Notificier_bot import periodic_check
import asyncio
if __name__ == "__main__":

    Regauth_bot.client.start()
    Regauth_bot.client.run_until_disconnected()

    Notificier_bot.client.start()
    Notificier_bot.client.run_until_disconnected()


