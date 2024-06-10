import pytest
from pydantic import ValidationError

from tickbybit.models.settings.settings import Settings


@pytest.fixture()
def s():
    settings = Settings()
    settings.set_key(path='triggers[+]', value=None)
    return settings


# absolute -----------------------------------------------------------------------

# triggers[0].ticker.markPrice.absolute
# успешно, значение — дефолт 1
def test_set_absolute_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.markPrice.absolute', value=None)
    assert settings_data['triggers'][0]['ticker']['markPrice']['absolute'] == 1


# triggers[0].ticker.markPrice.absolute: 5
# успешно, значение — 5
def test_set_absolute_valid(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.markPrice.absolute', value=5)
    assert settings_data['triggers'][0]['ticker']['markPrice']['absolute'] == 5


# triggers[0].ticker.markPrice.absolute: 5
# затем
# triggers[0].ticker.markPrice.absolute
# успешно, значение — дефолт 1
def test_set_absolute_valid_and_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.markPrice.absolute', value=5)
    settings_data = settings.set_key(path='triggers[0].ticker.markPrice.absolute', value=None)
    assert settings_data['triggers'][0]['ticker']['markPrice']['absolute'] == 1


# triggers[0].ticker.markPrice.absolute: qwe
# исключение, указано кривое значение
def test_set_absolute_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers[0].ticker.markPrice.absolute', value='qwe')


# suffix -----------------------------------------------------------------------

# triggers[0].ticker.symbol.suffix
# успешно, значение — дефолт "USDT"
def test_set_suffix_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.symbol.suffix', value=None)
    assert settings_data['triggers'][0]['ticker']['symbol']['suffix'] == 'USDT'


# triggers[0].ticker.symbol.suffix: TST
# успешно, значение — "TST"
def test_set_suffix_valid(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.symbol.suffix', value='TST')
    assert settings_data['triggers'][0]['ticker']['symbol']['suffix'] == 'TST'


# triggers[0].ticker.symbol.suffix: TST
# затем
# triggers[0].ticker.symbol.suffix
# успешно, значение — дефолт "USDT"
def test_set_suffix_valid_and_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.symbol.suffix', value='TST')
    settings_data = settings.set_key(path='triggers[0].ticker.symbol.suffix', value=None)
    assert settings_data['triggers'][0]['ticker']['symbol']['suffix'] == 'USDT'


# triggers[0].ticker.symbol.suffix: {}
# исключение, указано кривое значение
def test_set_suffix_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers[0].ticker.symbol.suffix', value={})
