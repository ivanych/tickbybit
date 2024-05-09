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

    # Пара сравниваемых прайсов
    tickers_pair = await pair(settings, dirpath=tickers_dir)

    # Изменения в отслеживаемых тикерах
    tickers_diff = tickers_pair.diff(settings)

    # Уведомления
    # TODO надо тут сделать, чтобы возвращался объект Alerts.
    diffs = tickers_diff.filter(filters=settings['ticker'])

    diff_list = diffs.list()

    # Отправка уведомлений в телегу
    for ticker_diff in diff_list:
        msg = format(td=ticker_diff, settings=settings)

        await bot.send_message(
            chat_id=chat_id,
            text=msg,
        )

    logger.info("Выполнена отправка уведомлений по расписанию; отправлено %s (user_id=%s)", len(diff_list), user_id)
