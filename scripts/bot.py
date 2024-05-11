#!/usr/bin/env python

import sys
from os import getenv
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.util import undefined

from tickbybit.middlewares.access import AccessMiddleware
from tickbybit.handlers import alert_router, error_router, help_router, settings_router
from tickbybit.storages.yamlfile import FileStorage
from tickbybit.schedule.tickers import download_new_tickers, prune_old_tickers
from tickbybit.schedule.alert import send_alert
from tickbybit.menu import set_command_menu
from tickbybit.settings import settings

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

logger = logging.getLogger("tickbybit")

TOKEN = getenv("BOT_TOKEN")
SETTINGS_FILE = getenv("SETTINGS_FILE")
TICKERS_DIR = getenv("TICKERS_DIR")
PRICE_TTL = int(getenv("PRICE_TTL"))
ALLOWED_USERS = list(map(int, getenv("ALLOWED_USERS").split(':')))
DOWNLOAD_PERIOD = int(getenv("DOWNLOAD_PERIOD"))
PRUNE_PERIOD = int(getenv("PRUNE_PERIOD"))
ALERT_PERIOD = int(getenv("ALERT_PERIOD"))

logger.info("Env TOKEN=%s", TOKEN)
logger.info("Env SETTINGS_FILE=%s", SETTINGS_FILE)
logger.info("Env TICKERS_DIR=%s", TICKERS_DIR)
logger.info("Env PRICE_TTL=%s", PRICE_TTL)
logger.info("Env ALLOWED_USERS=%s", ALLOWED_USERS)
logger.info("Env DOWNLOAD_PERIOD=%s", DOWNLOAD_PERIOD)
logger.info("Env PRUNE_PERIOD=%s", PRUNE_PERIOD)
logger.info("Env ALERT_PERIOD=%s", ALERT_PERIOD)

storage = FileStorage(file=SETTINGS_FILE)
dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.GLOBAL_USER)


async def main() -> None:
    #
    # Бот
    #
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Роуты
    dp.include_routers(settings_router, alert_router, help_router, error_router)

    # Разрешить доступ к боту только указанным пользователям
    dp.update.outer_middleware(AccessMiddleware(users=ALLOWED_USERS))

    # Установить в боте меню с командами
    dp.startup.register(set_command_menu)

    #
    # Планировщик
    #
    scheduler = AsyncIOScheduler()

    # Загрузка новых прайсов
    scheduler.add_job(
        func=download_new_tickers,
        trigger='interval',
        kwargs={'tickers_dir': TICKERS_DIR},
        id=f"download_new_tickers",
        seconds=DOWNLOAD_PERIOD,
    )

    # Очистка старых прайсов
    scheduler.add_job(
        func=prune_old_tickers,
        trigger='interval',
        kwargs={'tickers_dir': TICKERS_DIR, 'ttl': PRICE_TTL},
        id=f"prune_old_tickers",
        seconds=PRUNE_PERIOD,
    )

    # Автоматическая отправка уведомлений
    # (тут нам понадобятся все данные из хранилища)
    all_data = settings(file=SETTINGS_FILE)

    for key in all_data:
        # Смотрим только ключи с данными
        if '_data' in key:
            user_id = all_data[key]['user']['id']
            is_auto = all_data[key]['settings']['is_auto']

            # Если у пользователя включена автоматическая отправка уведомлений,
            # то передаём undefined — это что-то типа дефолта в apscheduler-е,
            # иначе передаём None — это сразу ставит задачу на паузу
            next_run_time = undefined if is_auto else None

            # Отправка уведомлений пользователю
            scheduler.add_job(
                func=send_alert,
                trigger='interval',
                kwargs={'dp': dp, 'bot': bot, 'user_id': user_id, 'tickers_dir': TICKERS_DIR},
                id=f"send_alert_u{user_id}",
                next_run_time=next_run_time,
                seconds=ALERT_PERIOD,
            )

    scheduler.start()

    # Понеслась!
    await dp.start_polling(bot, scheduler=scheduler, tickers_dir=TICKERS_DIR)


if __name__ == "__main__":
    asyncio.run(main())
