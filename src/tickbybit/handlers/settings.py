import logging
import re
from typing import Any

from aiogram import Router, html
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tickbybit.bot import to_yaml
from tickbybit.states.settings import SettingsStatesGroup, SStatesGroup
from tickbybit.models.settings.settings import Settings

logger = logging.getLogger(__name__)
router = Router()


@router.message(CommandStart(), StateFilter(None))
async def command_start(message: Message, state: FSMContext) -> None:
    # Состояние пользователя
    await state.set_state(SettingsStatesGroup.registered)

    # Данные пользователя
    user = {
        'id': message.from_user.id,
        'full_name': message.from_user.full_name,
    }
    settings = Settings.new()

    await state.update_data(
        user=user,
        settings=settings.model_dump(),
    )

    await message.answer(f"Здрасьте-мордасьте, {html.bold(message.from_user.full_name)}!")


@router.message(CommandStart())
async def command_start_reject(message: Message, state: FSMContext) -> None:
    fsm_state = await state.get_state()
    await message.answer(f"Вы уже зарегистрированы (state={fsm_state}).\n\n/help — посмотреть инструкцию.")


@router.message(StateFilter(None))
async def command_reject(message: Message) -> None:
    await message.answer(f"Сначала нужно зарегистрироваться!\n\n/start — зарегистрироваться.")


@router.message(Command("settings"), SettingsStatesGroup.registered)
async def command_settings(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    settings = Settings(**data['settings'])
    logger.info('Прочитаны настройки Settings')

    settings_yaml = to_yaml(settings.model_dump())
    msg = html.pre_language(settings_yaml, 'YAML')

    await message.answer(msg)


@router.message(Command("set"), SettingsStatesGroup.registered)
async def command_set(message: Message, command: CommandObject, state: FSMContext) -> None:
    # Если прилетела команда с аргументами — устанавливаем ключ
    if command.args:
        # Разбор аргументов команды
        args = re.split(r'\s*:\s*', command.args.strip(), 1)
        path = args[0]
        value = (args[1:] + [None])[0]

        text = await _set(path, state, value)

        await message.answer(text)

    # Если прилетела команда без аргументов — запускаем диалог установки ключа
    else:
        data = await state.get_data()
        settings = Settings(**data['settings'])

        # Клавиатура
        builder = InlineKeyboardBuilder()
        builder.button(
            text=f'format: {settings.format}', callback_data=FormatCallbackData(action='value', path="format")
        )
        builder.button(
            text="triggers...", callback_data=FormatCallbackData(action='value', path="triggers")
        )
        builder.adjust(1)

        text = 'Выберите ключ:'

        await message.answer(
            text=text,
            reply_markup=builder.as_markup()
        )


async def _annotation(path, state) -> Any:
    # Настройки
    data = await state.get_data()
    settings = Settings(**data['settings'])

    return settings.get_annotation(path)


async def _get(path, state) -> Any:
    # Настройки
    data = await state.get_data()
    settings = Settings(**data['settings'])

    return settings.get_value(path)


async def _set(path, state, value):
    # Настройки
    data = await state.get_data()
    settings = Settings(**data['settings'])

    try:
        settings_data = settings.set_key(path=path, value=value)
        await state.update_data(settings=settings_data)

        # TODO при установке значения по умолчанию value будет None, value_pre тоже None.
        #  Но выводить None в этом случае не изящно, надо бы выводить значение по умолчанию.
        value_pre = html.pre_language(value, 'YAML')
        text = f'Установлен ключ <b>{path}</b>.\n\nНовое значение:\n{value_pre}'
    except Exception as e:
        text = str(e)

    return text


@router.message(Command("del"), SettingsStatesGroup.registered)
async def command_del(message: Message, command: CommandObject, state: FSMContext) -> None:
    # Разбор аргументов команды
    args = re.split(r'\s*:\s*', command.args.strip(), 1)
    path = args[0]

    data = await state.get_data()
    settings = Settings(**data['settings'])

    try:
        settings_data = settings.del_key(path=path)
        await state.update_data(settings=settings_data)

        text = 'Ключ удалён.\n\n/settings — посмотреть настройки.'
    except Exception as e:
        text = str(e)

    await message.answer(text)


@router.message(Command("on"), SettingsStatesGroup.registered)
async def command_on(message: Message, state: FSMContext, scheduler: AsyncIOScheduler) -> None:
    data = await state.get_data()
    settings = Settings(**data['settings'])

    try:
        settings_data = settings.set_key(path='is_auto', value='true')
        await state.update_data(settings=settings_data)

        scheduler.resume_job(f"send_alert_u{data['user']['id']}")

        text = 'Автоматическая отправка уведомлений включена.\n\n/settings — посмотреть настройки.'
    except Exception as e:
        text = str(e)

    await message.answer(text)


@router.message(Command("off"), SettingsStatesGroup.registered)
async def command_off(message: Message, state: FSMContext, scheduler: AsyncIOScheduler) -> None:
    data = await state.get_data()
    settings = Settings(**data['settings'])

    try:
        settings_data = settings.set_key(path='is_auto', value='false')
        await state.update_data(settings=settings_data)

        scheduler.pause_job(f"send_alert_u{data['user']['id']}")

        text = 'Автоматическая отправка уведомлений выключена.\n\n/settings — посмотреть настройки.'
    except Exception as e:
        text = str(e)

    await message.answer(text)


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from aiogram.filters.callback_data import CallbackData
from typing import Optional, get_args, Literal, get_origin
from pprint import pformat
from pydantic import RootModel


class FormatCallbackData(CallbackData, prefix="st"):
    action: str
    path: str
    value: Optional[str] = None


@router.callback_query(FormatCallbackData.filter(F.action == "value"))
async def cb_value(callback: CallbackQuery, callback_data: FormatCallbackData, state: FSMContext):
    path = callback_data.path

    # Значение узла настроек
    value = await _get(path, state)

    builder = InlineKeyboardBuilder()
    text: str

    # Узел - строка
    #if get_origin(annotation) is Literal:
    if isinstance(value, str):
        annotation = await _annotation(path, state)

        # Узел — литерал
        if get_origin(annotation) is Literal:
            # Допустимы значания литерала
            annotation_args = get_args(annotation)
            print(f'annotation_args = {annotation_args}')

            # Клавиатура по списку значений
            for arg in annotation_args:
                builder.button(
                    text=arg, callback_data=FormatCallbackData(action='set', path=path, value=arg)
                )
            builder.adjust(3)

            value_pre = html.pre_language(value, 'YAML')
            text = f'Выберите значение для ключа <b>{path}</b>.\n\nТекущее значение:\n{value_pre}'

        # Узел - обычная строка
        else:
            value_pre = html.pre_language(value, 'YAML')
            text = f'Введите значение для ключа <b>{path}</b>.\n\nТекущее значение:\n{value_pre}'

    # Узел — список
    elif isinstance(value, RootModel):
        # Длина списка
        length = len(value.list())

        # Клавиатура по диапазону чисел (и кнопка `+`)
        for i in range(length):
            builder.button(
                text=f'{i}', callback_data=FormatCallbackData(action='value', path=f'{path}[{i}]')
            )
        builder.button(
            text='+', callback_data=FormatCallbackData(action='value', path=f'{path}[+]')
        )
        builder.adjust(3)

        length_code = html.code(length)
        text = (f'Выберите индекс элемента в ключе <b>{path}</b>.\n\n'
                f'Всего элементов в ключе: {length_code}')

    else:
        value_pre = html.pre_language(value, 'YAML')
        text = f'неизвестный тип узла <b>{path}</b>.\n\nТекущее значение:\n{value_pre}'

    await callback.message.edit_text(
        text=text,
        reply_markup=builder.as_markup()
    )


@router.callback_query(FormatCallbackData.filter(F.action == "set"))
async def cb_set(callback: CallbackQuery, callback_data: FormatCallbackData, state: FSMContext):
    path = callback_data.path
    value = callback_data.value

    text = await _set(path, state, value)

    await callback.message.edit_text(text)
