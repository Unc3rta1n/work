import asyncio
from bot.Notificier_bot import periodic_check

# Запуск периодической проверки в event loop
loop = asyncio.get_event_loop()
loop.create_task(periodic_check())
