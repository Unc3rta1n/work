from bot import Notificier_bot, Regauth_bot

if __name__ == "__main__":

    Regauth_bot.client.start()
    Regauth_bot.client.run_until_disconnected()

