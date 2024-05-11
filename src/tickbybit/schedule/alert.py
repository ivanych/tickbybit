import logging

from aiogram import Bot, Dispatcher

from tickbybit.files import pair
from tickbybit.bot import format

logger = logging.getLogger(__name__)


async def send_alert(dp: Dispatcher, bot: Bot, user_id: int, tickers_dir: str) -> None:
    # Бот использует FSM-стратегию GLOBAL_USER, поэтому для получения состояния из хранилища
    # не требуется задавать chat_id в явном виде. Можно указать chat_id=None и в resolve_context
    # chat_id будет автоматически приравнен к user_id.
    # Однако, chat_id всё-равно потребуется далее для отправки сообщений в телегу в send_message,
    # поэтому делаем chat_id=user_id явно.
    chat_id = user_id
    state = dp.fsm.resolve_context(bot=bot, chat_id=chat_id, user_id=user_id)
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
            tickers_pair_cache[interval] = await pair(interval, dirpath=tickers_dir)
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
    for alert in alerts_list:
        msg = format(td=alert, settings=settings)

        await bot.send_message(
            chat_id=chat_id,
            text=msg,
        )

    logger.info("Выполнена отправка уведомлений по расписанию; отправлено %s уведомлений (user_id=%s)",
                len(alerts_list), user_id)
