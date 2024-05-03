import logging

from aiogram import Router, F
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types import Message

logger = logging.getLogger(__name__)

router = Router()


@router.error(ExceptionTypeFilter(Exception), F.update.message.as_("message"))
async def error_handler(event, message: Message):
    logger.critical("Critical error caused by %s", event.exception, exc_info=True)
    await message.answer("ERROR. Произошёл какой-то непредусмотренный сбой. "
                         "Возможно, в настройки было записано что-то, что бот не может нормально обработать. "
                         "Можно попробовать удалить это из настроек.\n\n"
                         "/settings - посмотреть настройки\n"
                         "/help — посмотреть инструкцию")
