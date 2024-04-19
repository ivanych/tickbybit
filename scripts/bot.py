#!/usr/bin/env python

import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject, Filter
from aiogram.types import Message
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.exceptions import AiogramError

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tickbybit import diff, tickers, settings, to_json
from tickbybit.settings import set_key, del_key
import tickbybit.files

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
                         "Иванов что-то криво запрограммировал. "
                         "Скорее всего в настройки записано что-то, что бот не может нормально обработать. "
                         "Можно попробовать удалить это из настроек.\n\n"
                         "Посмотреть все настройки — /settings")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здрасьте-мордасьте, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("settings"))
async def command_diff(message: Message) -> None:
    msg = to_json(settings)
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message(Command("set"))
async def command_set(message: Message, command: CommandObject) -> None:
    global settings

    try:
        settings = set_key(dirpath='.settings', path=command.args)
        text = 'OK.\n\nПосмотреть все настройки — /settings'
    except Exception as e:
        text = str(e)

    await message.answer(text)


@dp.message(Command("del"))
async def command_del(message: Message, command: CommandObject) -> None:
    global settings

    try:
        settings = del_key(dirpath='.settings', path=command.args)
        text = 'OK.\n\nПосмотреть все настройки — /settings'
    except Exception as e:
        text = str(e)

    await message.answer(text)


@dp.message(Command("diff"))
async def command_diff(message: Message) -> None:
    # Загрузить новый прайс
    await download_new_tickers(dirpath=DIRPATH)

    # Найти пару сравниваемых прайсов
    pair = tickbybit.files.pair(settings, dirpath=DIRPATH)

    # Найти изменения в отслеживаемых тикерах
    diffs = diff(settings, pair)

    # Отправить в Телегу найденные изменения
    for dif in diffs:
        msg = to_json(dif)
        await message.answer(msg, parse_mode=ParseMode.MARKDOWN_V2)


@scheduler.scheduled_job(trigger='interval', kwargs={'dirpath': DIRPATH}, seconds=60)
async def download_new_tickers(dirpath: str) -> None:
    new_tickers = await tickers()
    await tickbybit.files.save(new_tickers, dirpath=dirpath)


@scheduler.scheduled_job(trigger='interval',
                         kwargs={'period': settings['period'], 'interval': settings['interval'], 'dirpath': DIRPATH},
                         seconds=60)
async def prune_old_tickers(period: int, interval: int, dirpath: str) -> None:
    tickbybit.files.prune(period=period, interval=interval, dirpath=dirpath)


async def main() -> None:
    scheduler.start()

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
