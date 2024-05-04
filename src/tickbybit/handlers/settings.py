import re

from aiogram import Router, html
from aiogram.filters import CommandStart, Command, CommandObject, StateFilter
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from tickbybit.bot import to_yaml
from tickbybit.states.settings import SettingsStatesGroup
from tickbybit.settings import DEFAULT_SETTINGS, setup_key, delete_key

router = Router()


@router.message(CommandStart(), StateFilter(None))
async def command_start(message: Message, state: FSMContext) -> None:
    # Зарегистрировать пользователя
    await state.set_state(SettingsStatesGroup.registered)

    # Данные пользователя
    user = {
        'id': message.from_user.id,
    }

    # Зарегистрировать пользователя с настройками по умолчанию
    await state.update_data(
        user=user,
        settings=DEFAULT_SETTINGS,
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

    msg_yaml = to_yaml(data['settings'])
    msg_yaml_md = f"```YAML\n{msg_yaml}```"

    await message.answer(msg_yaml_md, parse_mode=ParseMode.MARKDOWN_V2)


@router.message(Command("set"), SettingsStatesGroup.registered)
async def command_set(message: Message, command: CommandObject, state: FSMContext) -> None:
    # Разбор аргументов команды
    args = re.split(r'\s*:\s*', command.args.strip(), 1)
    path = args[0]
    value = (args[1:] + [None])[0]

    try:
        data = await state.get_data()
        settings = setup_key(data['settings'], path=path, value=value)
        await state.update_data(settings=settings)
        text = 'Ключ установлен.\n\n/settings — посмотреть настройки.'
    except Exception as e:
        text = str(e)

    await message.answer(text)


@router.message(Command("del"), SettingsStatesGroup.registered)
async def command_del(message: Message, command: CommandObject, state: FSMContext) -> None:
    # Разбор аргументов команды
    args = re.split(r'\s*:\s*', command.args.strip(), 1)
    path = args[0]

    try:
        data = await state.get_data()
        settings = delete_key(data['settings'], path=path)
        await state.update_data(settings=settings)
        text = 'Ключ удалён.\n\n/settings — посмотреть настройки.'
    except Exception as e:
        text = str(e)

    await message.answer(text)
