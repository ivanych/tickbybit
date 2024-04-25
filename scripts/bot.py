#!/usr/bin/env python

import asyncio
import logging
import sys
import re
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject, Filter
from aiogram.types import Message
from aiogram.filters.exception import ExceptionTypeFilter

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tickbybit import format, to_yaml
from tickbybit.settings import settings, set_key, del_key
from tickbybit.bybit import tickers
from tickbybit.files import save, pair, prune

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

logger = logging.getLogger("tickbybit")

TOKEN = getenv("BOT_TOKEN")
DIRPATH = getenv("BOT_DIRPATH")

logger.info("Env TOKEN=%s", TOKEN)
logger.info("Env DIRPATH=%s", DIRPATH)

settings = settings('.settings')
scheduler = AsyncIOScheduler()
dp = Dispatcher()


@dp.error(ExceptionTypeFilter(Exception), F.update.message.as_("message"))
async def error_handler(event, message: Message):
    logger.critical("Critical error caused by %s", event.exception, exc_info=True)
    await message.answer("ERROR. Произошёл какой-то непредусмотренный сбой. "
                         "Возможно, в настройки было записано что-то, что бот не может нормально обработать. "
                         "Можно попробовать удалить это из настроек.\n\n"
                         "Посмотреть настройки — /settings")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здрасьте-мордасьте, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("settings"))
async def command_diff(message: Message) -> None:
    msg = to_yaml(settings)
    await message.answer(msg)


@dp.message(Command("alert"))
async def command_alert(message: Message) -> None:
    # Пара сравниваемых прайсов
    tickers_pair = await pair(settings, dirpath='.tickers')

    # Изменения в отслеживаемых тикерах
    tickers_diff = tickers_pair.diff(settings)

    # Вывод изменений в Телегу
    diffs = tickers_diff.alert()

    if diffs:
        for ticker_diff in diffs:
            msg = format(td=ticker_diff, settings=settings)
            await message.answer(msg)
    else:
        await message.answer('Уведомлений нет.')


@dp.message(Command("set"))
async def command_set(message: Message, command: CommandObject) -> None:
    global settings

    # Разбор аргумента
    args = re.split(r'\s*:\s*', command.args.strip(), 1)
    path = args[0]
    value = (args[1:] + [None])[0]

    try:
        settings = set_key(dirpath='.settings', path=path, value=value)
        text = 'Ключ установлен.\n\nПосмотреть настройки — /settings'
    except Exception as e:
        text = str(e)

    await message.answer(text)


@dp.message(Command("del"))
async def command_del(message: Message, command: CommandObject) -> None:
    global settings

    # Разбор аргумента
    args = re.split(r'\s*:\s*', command.args.strip(), 1)
    path = args[0]

    try:
        settings = del_key(dirpath='.settings', path=path)
        text = 'Ключ удалён.\n\nПосмотреть настройки — /settings'
    except Exception as e:
        text = str(e)

    await message.answer(text)


@scheduler.scheduled_job(trigger='interval', kwargs={'dirpath': DIRPATH}, seconds=60)
async def download_new_tickers(dirpath: str) -> None:
    new_tickers = await tickers()
    await save(new_tickers['tickers'], time=new_tickers['time'], dirpath=dirpath)


@scheduler.scheduled_job(trigger='interval',
                         kwargs={'period': settings['period'], 'interval': settings['interval'], 'dirpath': DIRPATH},
                         seconds=60)
async def prune_old_tickers(period: int, interval: int, dirpath: str) -> None:
    prune(period=period, interval=interval, dirpath=dirpath)


async def main() -> None:
    scheduler.start()

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
