from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

router = Router()


@router.message(Command("help"))
async def command_help(message: Message) -> None:
    msg = """
<b>Настройки</b>
    <code>/settings</code> — посмотреть настройки.
    <code>/set путь.к.ключу: значение</code> — установить ключ в настройках.
    <code>/del путь.к.ключу</code> — удалить ключ в настройках.
    
    <i>(не все ключи можно установить и удалить)</i>
    
<b>Фильтры</b>
    <code>absolute</code> — абсолютное значение изменения атрибута, число в процентах.
    <code>suffix</code> — последние буквы в значении атрибута. Можно указать список вариантов через запятую.
    Варианты одного фильтра объединяются через "ИЛИ".
    
    Все фильтры объединяются через "И".
    
    Примеры:
    
    Отфильтровать тикеры по изменению цены:
    <code>/set ticker.markPrice.absolute: 1.5</code>
    Этот фильтр будет выдавать уведомления только для тикеров, у которых цена изменилась на 1.5 процента и больше.
    
    Отфильтровать тикеры по названию:
    <code>/set ticker.symbol.suffix: USDT, EKLMN</code>
    Этот фильтр будет выдавать уведомления только для тикеров, которые заканчиваются на USDT или на EKLMN.
    
<b>Форматы</b> 
    <code>json</code> — все данные.
    <code>yaml</code> — все данные.
    <code>str1</code> — процент Price.
    <code>str1p</code> — процент Price, всегда со знаком.
    <code>str2</code> — проценты Price и OpenInterestValue.
    <code>str2p</code> — проценты Price и OpenInterestValue, всегда со знаком.
    <code>tpl1pa</code> — проценты Price и OpenInterestValue в ряд, всегда со знаком, стрелки.
    <code>tpl1pc</code> — проценты Price и OpenInterestValue в ряд, всегда со знаком, круги.
    <code>tpl1ps</code> — проценты Price и OpenInterestValue в ряд, всегда со знаком, квадраты.
    <code>tpl2pa</code> — проценты Price и OpenInterestValue в колонку, всегда со знаком, стрелки.
    <code>tpl2pc</code> — проценты Price и OpenInterestValue в колонку, всегда со знаком, круги.
    <code>tpl2ps</code> — проценты Price и OpenInterestValue в колонку, всегда со знаком, квадраты.
    
    Примеры:
    
    Установить минималистичный формат с красивыми кружками один под другим:
    <code>/set format: tpl2pc</code>
    
<b>Уведомления</b>
    <code>/alert</code> — получить уведомления.
    <code>/on</code> — включить автоматические уведомления.
    <code>/off</code> — выключить автоматические уведомления.
    """

    await message.answer(msg)
