import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tickbybit.bot import format
from tickbybit.files import pair
from tickbybit.states.settings import SettingsStatesGroup

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("alert"), SettingsStatesGroup.registered)
async def command_alert(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    settings = data['settings']

    # TODO надо бы перенести кеш в метод files.pair, но там инвалидацию надо продумывать,
    # а тут инвалидируется само при выходе из метода.
    tickers_pair_cache = {}

    alerts_list = []

    # Отсортировать триггеры по интервалу
    triggers = sorted(settings['triggers'], key=lambda x: x['interval'], reverse=True)

    # Цикл по триггерам
    for trigger in triggers:
        interval = trigger['interval']
        logger.info('Обработка триггера (interval=%s)...', interval)

        # Пара прайсов (пытаемся взять из кеша)
        tickers_pair = tickers_pair_cache.get(interval)
        if tickers_pair is None:
            tickers_pair_cache[interval] = await pair(interval, dirpath='.tickers')
            tickers_pair = tickers_pair_cache[interval]
        else:
            logger.info('Пара прайсов для интервала interval=%s получена из кеша', interval)

        # Изменения тикеров
        ticker_diffs = tickers_pair.diff()

        # Уведомления по тикерам
        # TODO надо тут сделать, чтобы возвращался объект Alerts.
        alerts = ticker_diffs.filter(trigger=trigger)

        alerts_list.extend(alerts.list())

    # Отправка уведомлений в телегу
    if alerts_list:
        for alert in alerts_list:
            msg = format(alert, settings=settings)
            await message.answer(msg)
    else:
        await message.answer('Уведомлений нет.')
