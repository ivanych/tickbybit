import logging
import re

from aiogram import Router, html
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tickbybit.bot import to_yaml
from tickbybit.states.settings import SettingsStatesGroup
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
    # Разбор аргументов команды
    args = re.split(r'\s*:\s*', command.args.strip(), 1)
    path = args[0]
    value = (args[1:] + [None])[0]

    data = await state.get_data()
    settings = Settings(**data['settings'])

    try:
        settings_data = settings.setup_key(path=path, value=value)
        await state.update_data(settings=settings_data)

        text = 'Ключ установлен.\n\n/settings — посмотреть настройки.'
    except Exception as e:
        text = str(e)

    await message.answer(text)


@router.message(Command("del"), SettingsStatesGroup.registered)
async def command_del(message: Message, command: CommandObject, state: FSMContext) -> None:
    # Разбор аргументов команды
    args = re.split(r'\s*:\s*', command.args.strip(), 1)
    path = args[0]

    data = await state.get_data()
    settings = Settings(**data['settings'])

    try:
        settings_data = settings.delete_key(path=path)
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
        settings_data = settings.setup_key(path='is_auto', value='true')
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
        settings_data = settings.setup_key(path='is_auto', value='false')
        await state.update_data(settings=settings_data)

        scheduler.pause_job(f"send_alert_u{data['user']['id']}")

        text = 'Автоматическая отправка уведомлений выключена.\n\n/settings — посмотреть настройки.'
    except Exception as e:
        text = str(e)

    await message.answer(text)
