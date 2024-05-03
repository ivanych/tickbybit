from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

router = Router()


@router.message(Command("help"))
async def command_help(message: Message) -> None:
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
               "`tpl2ps` — проценты Price и OpenInterestValue в колонку, всегда со знаком, квадраты\n"
               "\n"
               "*Уведомления*\n"
               "Получить уведомления — /alert\n"
               "Включить автоматические уведомления — /on\n"
               "Выключить автоматические уведомления — /off\n")

    await message.answer(help_md, parse_mode=ParseMode.MARKDOWN_V2)
