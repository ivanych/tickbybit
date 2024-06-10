import pytest
from pydantic import ValidationError

from tickbybit.models.settings.settings import Settings


@pytest.fixture()
def s():
    settings = Settings()
    settings.set_key(path='triggers[+]', value=None)
    return settings


# markPrice -------------------------------------------------------------------------

# triggers[0].ticker.markPrice
# успешно, значение — дефолтный словарь с ключами флоат-атрибута
def test_set_markPrice_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.markPrice', value=None)

    assert isinstance(settings_data['triggers'][0]['ticker']['markPrice'], dict)
    assert 'absolute' in settings_data['triggers'][0]['ticker']['markPrice']


# triggers[0].ticker.markPrice: {} (эквивалентно None)
# успешно, значение — дефолтный словарь с ключами флоат-атрибута
def test_set_markPrice_emptydict(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.markPrice', value={})

    assert isinstance(settings_data['triggers'][0]['ticker']['markPrice'], dict)
    assert 'absolute' in settings_data['triggers'][0]['ticker']['markPrice']


# triggers[0].ticker.markPrice: {valid}
# успешно, значение — словарь valid
def test_set_markPrice_validdict(s):
    settings = s.model_copy(deep=True)

    pytest.skip("triggers[0].ticker.markPrice: {valid}")


# triggers[0].ticker.markPrice: qwe
# исключение, указано кривое значение
def test_set_markPrice_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers[0].ticker.markPrice', value='qwe')


# openInterestValue -------------------------------------------------------------------------

# triggers[0].ticker.openInterestValue
# успешно, значение — дефолтный словарь с ключами флоат-атрибута
def test_set_openInterestValue_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.openInterestValue', value=None)

    assert isinstance(settings_data['triggers'][0]['ticker']['openInterestValue'], dict)
    assert 'absolute' in settings_data['triggers'][0]['ticker']['openInterestValue']


# triggers[0].ticker.openInterestValue: {} (эквивалентно None)
# успешно, значение — дефолтный словарь с ключами флоат-атрибута
def test_set_openInterestValue_emptydict(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.openInterestValue', value={})

    assert isinstance(settings_data['triggers'][0]['ticker']['openInterestValue'], dict)
    assert 'absolute' in settings_data['triggers'][0]['ticker']['openInterestValue']


# triggers[0].ticker.openInterestValue: {valid}
# успешно, значение — словарь valid
def test_set_openInterestValue_validdict(s):
    settings = s.model_copy(deep=True)

    pytest.skip("triggers[0].ticker.openInterestValue: {valid}")


# triggers[0].ticker.openInterestValue: qwe
# исключение, указано кривое значение
def test_set_openInterestValue_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers[0].ticker.openInterestValue', value='qwe')


# symbol -------------------------------------------------------------------------

# triggers[0].ticker.symbol
# успешно, значение — дефолтный словарь с ключами стринг-атрибута
def test_set_symbol_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.symbol', value=None)

    assert isinstance(settings_data['triggers'][0]['ticker']['symbol'], dict)
    assert 'suffix' in settings_data['triggers'][0]['ticker']['symbol']


# triggers[0].ticker.symbol: {} (эквивалентно None)
# успешно, значение — дефолтный словарь с ключами стринг-атрибута
def test_set_symbol_emptydict(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker.symbol', value={})

    assert isinstance(settings_data['triggers'][0]['ticker']['symbol'], dict)
    assert 'suffix' in settings_data['triggers'][0]['ticker']['symbol']


# triggers[0].ticker.symbol: {valid}
# успешно, значение — словарь valid
def test_set_symbol_validdict(s):
    settings = s.model_copy(deep=True)

    pytest.skip("triggers[0].ticker.symbol: {valid}")


# triggers[0].ticker.symbol: qwe
# исключение, указано кривое значение
def test_set_symbol_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers[0].ticker.symbol', value='qwe')
