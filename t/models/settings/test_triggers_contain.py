import pytest

from tickbybit.models.settings.settings import Settings


@pytest.fixture()
def s():
    settings = Settings()
    settings.set_key(path='triggers[+]', value=None)
    return settings


# triggers[0]
# успешно, результат — дефолтный словарь с ключами триггера
def test_set_item_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0]', value=None)

    assert isinstance(settings_data['triggers'][0], dict)
    assert 'icon' in settings_data['triggers'][0]
    assert 'interval' in settings_data['triggers'][0]
    assert 'ticker' in settings_data['triggers'][0]


# triggers[0]: {} (пустой словарь здесь эквивалентен None)
# успешно, результат — дефолтный словарь с ключами триггера
def test_set_item_emptydict(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0]', value={})

    assert isinstance(settings_data['triggers'][0], dict)
    assert 'icon' in settings_data['triggers'][0]
    assert 'interval' in settings_data['triggers'][0]
    assert 'ticker' in settings_data['triggers'][0]


# triggers[0]: {valid}
# успешно, результат — словарь valid
def test_set_item_validdict(s):
    pytest.skip("triggers[0]: {valid}")


# triggers[0]: qwe
# исключение, указано кривое значение
def test_set_item_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValueError):
        settings_data = settings.set_key(path='triggers[0]', value='qwe')
