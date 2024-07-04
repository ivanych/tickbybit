from aiogram import Bot
from aiogram.types import BotCommand


async def set_command_menu(bot: Bot) -> bool:
    commands = [
        BotCommand(command='/on', description='Включить уведомления'),
        BotCommand(command='/off', description='Выключить уведомления'),
        BotCommand(command='/alert', description='Получить уведомления'),
        BotCommand(command='/settings', description='Посмотреть настройки'),
        BotCommand(command='/set', description='Установить ключ в настройках'),
        BotCommand(command='/del', description='Удалить триггер из настроек'),
        BotCommand(command='/help', description='Посмотреть инструкцию'),
    ]

    return await bot.set_my_commands(commands)
