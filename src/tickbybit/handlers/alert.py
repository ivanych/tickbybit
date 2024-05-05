from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from tickbybit.bot import format
from tickbybit.files import pair
from tickbybit.states.settings import SettingsStatesGroup

router = Router()


@router.message(Command("alert"), SettingsStatesGroup.registered)
async def command_alert(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    settings = data['settings']

    # Пара сравниваемых прайсов
    tickers_pair = await pair(settings, dirpath='.tickers')

    # Изменения в отслеживаемых тикерах
    tickers_diff = tickers_pair.diff(settings)

    # Изменения с уведомлениями
    diffs = tickers_diff.alert()

    if settings['filters'].get('suffix'):
        diffs = diffs.suffix(settings['filters'].get('suffix'))

    diff_list = diffs.list()

    # Отправка уведомлений в телегу
    if diff_list:
        for ticker_diff in diff_list:
            msg = format(ticker_diff, settings=settings)
            await message.answer(msg)
    else:
        await message.answer('Уведомлений нет.')
