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

    Установить значение любого ключа:
    <code>/set путь.к.ключу: значение</code>
    <code>/set путь[1].к.ключу: значение</code>

<b>ТРИГГЕРЫ</b>
    Добавить триггер:
    <code>/set triggers[+]</code>

    Удалить триггер:
    <code>/del triggers[1]</code>

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

    Установить формат уведомления:
    <code>/set format: формат</code>

    Включить автоматические уведомления (каждую минуту):
    <code>/on</code>

    Выключить автоматические уведомления:
    <code>/off</code>


<b>ПОЛНАЯ ДОКУМЕНТАЦИЯ</b>

    https://github.com/ivanych/tickbybit
    """

    await message.answer(msg_help, disable_web_page_preview=True)
