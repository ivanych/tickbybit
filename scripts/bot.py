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
from tickbybit.settings import settings

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

logger = logging.getLogger("tickbybit")

TOKEN = getenv("BOT_TOKEN")
SETTINGS_FILE = getenv("SETTINGS_FILE")
DIRPATH = getenv("BOT_DIRPATH")
PRICE_TTL = int(getenv("PRICE_TTL"))
ALLOWED_USERS = list(map(int, getenv("ALLOWED_USERS").split(':')))

logger.info("Env TOKEN=%s", TOKEN)
logger.info("Env SETTINGS_FILE=%s", SETTINGS_FILE)
logger.info("Env DIRPATH=%s", DIRPATH)
logger.info("Env PRICE_TTL=%s", PRICE_TTL)
logger.info("Env ALLOWED_USERS=%s", ALLOWED_USERS)

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

    #
    # Планировщик
    #
    scheduler = AsyncIOScheduler()

    # Загрузка новых прайсов
    scheduler.add_job(
        func=download_new_tickers,
        trigger='interval',
        kwargs={'dirpath': DIRPATH},
        id=f"download_new_tickers",
        seconds=60,
    )

    # Очистка старых прайсов
    scheduler.add_job(
        func=prune_old_tickers,
        trigger='interval',
        kwargs={'dirpath': DIRPATH, 'ttl': PRICE_TTL},
        id=f"prune_old_tickers",
        seconds=60,
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
                kwargs={'dp': dp, 'bot': bot, 'user_id': user_id, 'tickers_dir': DIRPATH},
                id=f"send_alert_u{user_id}",
                next_run_time=next_run_time,
                seconds=60,
            )

    scheduler.start()

    # Понеслась!
    await dp.start_polling(bot, scheduler=scheduler)


if __name__ == "__main__":
    asyncio.run(main())
