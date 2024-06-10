import pytest
from pydantic import ValidationError

from tickbybit.models.settings.settings import Settings


@pytest.fixture()
def s():
    settings = Settings()
    return settings


# triggers[]
# исключение, не указан элемент
def test_set_noitem_none(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers[]', value=None)


# triggers[]: {}
# исключение, не указан элемент
def test_set_noitem_emptydict(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers[]', value={})


# triggers[0]
# исключение, указан несуществующий элемент
def test_set_notexistitem_none(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(IndexError):
        settings_data = settings.set_key(path='triggers[0]', value=None)


# triggers[0]: {}
# исключение, указан несуществующий элемент
def test_set_notexistitem_emptydict(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(IndexError):
        settings_data = settings.set_key(path='triggers[0]', value={})


# triggers[+]
# успешно, результат — список с одним дефолтным словарём триггера
def test_set_append_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[+]', value=None)

    assert isinstance(settings_data['triggers'], list)
    assert len(settings_data['triggers']) == 1
    assert isinstance(settings_data['triggers'][0], dict)
    assert 'icon' in settings_data['triggers'][0]
    assert 'interval' in settings_data['triggers'][0]
    assert 'ticker' in settings_data['triggers'][0]


# triggers[+]: {} (пустой словарь здесь эквивалентен None)
# успешно, результат — список с одним дефолтным словарём триггера
def test_set_append_emptydict(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[+]', value={})

    assert isinstance(settings_data['triggers'], list)
    assert len(settings_data['triggers']) == 1
    assert isinstance(settings_data['triggers'][0], dict)
    assert 'icon' in settings_data['triggers'][0]
    assert 'interval' in settings_data['triggers'][0]
    assert 'ticker' in settings_data['triggers'][0]


# triggers[+]: {valid}
# успешно, результат — список с одним validdict
def test_set_append_validdict():
    pytest.skip("triggers[+]: {valid}")


# triggers[+]: qwe
# исключение, указано кривое значение
def test_set_append_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValueError):
        settings_data = settings.set_key(path='triggers[+]', value='qwe')
