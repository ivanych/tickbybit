import pytest
from pydantic import ValidationError

from tickbybit.models.settings.settings import Settings


@pytest.fixture()
def s():
    settings = Settings()
    return settings


# format
# успешно, значение — дефолтный "json"
def test_set_format_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='format', value=None)
    assert settings_data['format'] == 'json'


# format: yaml
# успешно, значение — "yaml"
def test_set_format_valid(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='format', value='yaml')
    assert settings_data['format'] == 'yaml'


# format: yaml
# затем
# format
# успешно, значение — дефолтный "json"
def test_set_format_valid_and_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='format', value='yaml')
    settings_data = settings.set_key(path='format', value=None)
    assert settings_data['format'] == 'json'


# format: qwe
# исключение, указано кривое значение
def test_set_format_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='format', value='qwe')


# is_auto ----------------------------------------------------------------

def test_is_auto(s):
    settings = s.model_copy(deep=True)

    assert settings.is_auto is False


def test_set_is_auto_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='is_auto', value=None)
    assert settings_data['is_auto'] is False


def test_set_is_auto_valid(s):
    settings = s.model_copy(deep=True)
    settings_data = settings.set_key(path='is_auto', value=True)
    assert settings_data['is_auto'] is True


def test_set_is_auto_valid_and_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='is_auto', value=True)
    settings_data = settings.set_key(path='is_auto', value=None)
    assert settings_data['is_auto'] is False


def test_set_is_auto_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='is_auto', value='qwe')


# triggers ------------------------------------------------------------------

def test_triggers(s):
    settings = s.model_copy(deep=True)

    assert settings.triggers.list() == []


def test_set_triggers_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers', value=None)
    assert settings_data['triggers'] == []


def test_set_triggers_valid_emptylist(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers', value=[])
    assert settings_data['triggers'] == []


def test_set_triggers_validlist(s):
    settings = s.model_copy(deep=True)

    pytest.skip("triggers: list")


def test_set_triggers_invalid_str(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers', value='qwe')


def test_set_triggers_invalid_emptydict(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers', value={})
