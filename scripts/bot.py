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
from tickbybit.middlewares.access import AccessMiddleware

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

logger = logging.getLogger("tickbybit")

TOKEN = getenv("BOT_TOKEN")
DIRPATH = getenv("BOT_DIRPATH")
CHAT_ID = int(getenv("BOT_CHAT_ID"))
ALLOWED_USERS = list(map(int, getenv("ALLOWED_USERS").split(':')))

logger.info("Env TOKEN=%s", TOKEN)
logger.info("Env DIRPATH=%s", DIRPATH)
logger.info("Env ALLOWED_USERS=%s", ALLOWED_USERS)

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


@dp.message(Command("help"))
async def command_diff(message: Message) -> None:
    help_md = ("*Настройки*\n"
               "Посмотреть настройки — /settings\n"
               "Установить ключ в настройках — `/set путь.к.ключу: значение`\n"
               "Удалить ключ в настройках — `/del путь.к.ключу`\n"
               "\n"
               "_\(не все ключи можно установить и удалить\)_\n"
               "\n"
               "Например, установить порог уведомления для атрибута markPrice: `/set ticker.markPrice.alert_pcnt: 3`\n"
               "\n"
               "*Форматы*\n"
               "Формат устанавливается в настройках — `/set format: формат`\n"
               "\n"
               "`json` — все данные\n"
               "`yaml` — все данные\n"
               "`str1` — процент Price\n"
               "`str2` — процент Price, всегда со знаком\n"
               "`str3` — проценты Price и OpenInterestValue\n"
               "`str4` — проценты Price и OpenInterestValue, всегда со знаком\n"
               "`tpl1pa` — проценты Price и OpenInterestValue в ряд, всегда со знаком, стрелки\n"
               "`tpl1pc` — проценты Price и OpenInterestValue в ряд, всегда со знаком, круги\n"
               "`tpl1ps` — проценты Price и OpenInterestValue в ряд, всегда со знаком, квадраты\n"
               "`tpl2pc` — проценты Price и OpenInterestValue в колонку, всегда со знаком, круги\n"
               "`tpl2ps` — проценты Price и OpenInterestValue в колонку, всегда со знаком, круги\n"
               "\n"
               "*Уведомления*\n"
               "Получить уведомления — /alert\n"
               "Включить автоматические уведомления — /on\n"
               "Выключить автоматические уведомления — /off\n")

    await message.answer(help_md, parse_mode=ParseMode.MARKDOWN_V2)


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


@dp.message(Command("on"))
async def command_on(message: Message) -> None:
    global settings

    path = 'is_auto'
    value = 'true'

    try:
        scheduler.resume_job(f"schedule_alert_{CHAT_ID}")

        settings = set_key(dirpath='.settings', path=path, value=value)
        text = f"Автоматическая отправка уведомлений включена ({path}: {value})."
    except Exception as e:
        text = str(e)

    await message.answer(text)


@dp.message(Command("off"))
async def command_off(message: Message) -> None:
    global settings

    path = 'is_auto'
    value = 'false'

    try:
        scheduler.pause_job(f"schedule_alert_{CHAT_ID}")

        settings = set_key(dirpath='.settings', path=path, value=value)
        text = f"Автоматическая отправка уведомлений выключена ({path}: {value})."
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
        id=f"schedule_alert_{CHAT_ID}",
        next_run_time=None,  # None здесь чтобы задача создавалась на паузе
        seconds=60,
    )

    if settings['is_auto']:
        scheduler.resume_job(f"schedule_alert_{CHAT_ID}")

    scheduler.start()

    # Разрешить доступ к боту только указанным пользователям
    dp.update.outer_middleware(AccessMiddleware(users=ALLOWED_USERS))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
