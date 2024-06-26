from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

router = Router()


@router.message(Command("help"))
async def command_help(message: Message) -> None:
    msg_help = """
<b>НАСТРОЙКИ</b>
    Посмотреть настройки:
    <code>/settings</code>

    Установить значение ключа:
    <code>/set путь.к.ключу: значение</code>
    <code>/set путь[1].к.ключу: значение</code>

    Добавить элемент в конец списка:
    <code>/set путь[+]</code>

    Удалить произвольный элемент из списка:
    <code>/del путь[1]</code>

    Удалить элемент из конца списка:
    <code>/del путь[-]</code>

<b>ТРИГГЕРЫ</b>
    Добавить триггер:
    <code>/set triggers[+]</code>

    Установить интервал триггера (в секундах):
    <code>/set triggers[0].interval: 60</code>

    Установить фильтр по численным показателям тикера (в процентах):
    <code>/set triggers[0].ticker.markPrice.absolute: 1.5</code>
    <code>/set triggers[0].ticker.openInterestValue.absolute: 2</code>

    Установить фильтр по названию тикера (последние буквы названия):
    <code>/set triggers[0].ticker.symbol.suffix: USDT</code>

<b>УВЕДОМЛЕНИЯ</b>
    Получить уведомления немедленно:
    <code>/alert</code>

    Включить автоматические уведомления (каждую минуту):
    <code>/set is_alert: true</code>
    <code>/on</code>

    Выключить автоматические уведомления:
    <code>/set is_alert: false</code>
    <code>/off</code>

    Установить формат уведомления:
    <code>/set format: формат</code>
    """

    await message.answer(msg_help)
