#!/usr/bin/env python

import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tickbybit import diff, tickers, settings, to_json
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


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здрасьте-мордасьте, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("settings"))
async def command_diff(message: Message) -> None:
    msg = to_json(settings)
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN_V2)


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
