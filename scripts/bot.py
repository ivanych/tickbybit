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

from tickbybit import diff, tickers, notify, settings, to_json
import tickbybit.files

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

logger = logging.getLogger("tickbybit")

TOKEN = getenv("BOT_TOKEN")
DIRPATH = getenv("BOT_DIRPATH")

logger.info("Env TOKEN=%s", TOKEN)
logger.info("Env DIRPATH=%s", DIRPATH)

# Настройки
settings = settings()

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здрасьте-мордасьте, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("diff"))
async def command_diff(message: Message) -> None:
    # Загрузить новый прайс
    new_tickers = await tickers()
    await tickbybit.files.save(new_tickers, dirpath=DIRPATH)

    # Удалить устаревшие прйсы
    tickbybit.files.prune(dirpath=DIRPATH, period=5 * 60 * 1000)

    # Найти пару сравниваемых прайсов
    pair = tickbybit.files.pair(settings, dirpath=DIRPATH)

    # Найти изменения в отслеживаемых тикерах
    diffs = diff(settings, pair)

    # Отправить в Телегу найденные изменения
    for dif in diffs:
        msg = to_json(dif)
        await message.answer(msg, parse_mode=ParseMode.MARKDOWN_V2)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    asyncio.run(main())
