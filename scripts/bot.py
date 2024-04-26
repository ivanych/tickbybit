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
CHAT_ID = getenv("BOT_CHAT_ID")

logger.info("Env TOKEN=%s", TOKEN)
logger.info("Env DIRPATH=%s", DIRPATH)
logger.info("Env CHAT_ID=%s", CHAT_ID)

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
    msg_yaml = to_yaml(settings)
    msg_yaml_md = f"```YAML\n{msg_yaml}```"
    await message.answer(msg_yaml_md, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message(Command("alert"))
async def command_alert(message: Message) -> None:
    # Пара сравниваемых прайсов
    tickers_pair = await pair(settings, dirpath='.tickers')

    # Изменения в отслеживаемых тикерах
    tickers_diff = tickers_pair.diff(settings)

    # Изменения с уведомлениями
    diffs = tickers_diff.alert()

    # Отправка уведомлений в телегу
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


async def schedule_alert(bot: Bot, dir_path: str, chat_id: int) -> None:
    # Пара сравниваемых прайсов
    tickers_pair = await pair(settings, dirpath=dir_path)

    # Изменения в отслеживаемых тикерах
    tickers_diff = tickers_pair.diff(settings)

    # Изменения с уведомлениями
    diffs = tickers_diff.alert()

    # Отправка уведомлений в телегу
    for ticker_diff in diffs:
        msg = format(td=ticker_diff, settings=settings)

        await bot.send_message(
            chat_id=chat_id,
            text=msg,
        )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    scheduler.add_job(
        func=schedule_alert,
        trigger='interval',
        kwargs={'bot': bot, 'dir_path': DIRPATH, 'chat_id': CHAT_ID},
        seconds=60,
    )

    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
