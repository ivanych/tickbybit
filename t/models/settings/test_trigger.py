import pytest
from pydantic import ValidationError

from tickbybit.models.settings.settings import Settings


@pytest.fixture()
def s():
    settings = Settings()
    settings.set_key(path='triggers[+]', value=None)
    return settings


# triggers[0].icon
# успешно, значение — дефолт None
def test_set_icon_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].icon', value=None)
    assert settings_data['triggers'][0]['icon'] is None


# triggers[0].icon: X
# успешно, значение — "X"
def test_set_icon_valid(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].icon', value="X")
    assert settings_data['triggers'][0]['icon'] == 'X'


# triggers[0].icon: X
# затем
# triggers[0].icon
# успешно, значение — дефолт None
def test_set_icon_valid_and_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].icon', value='X')
    settings_data = settings.set_key(path='triggers[0].icon', value=None)
    assert settings_data['triggers'][0]['icon'] is None


# interval -----------------------------------------------------------------------

# triggers[0].interval
# успешно, значение — дефолт 60
def test_set_interval_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].interval', value=None)
    assert settings_data['triggers'][0]['interval'] == 60


# triggers[0].interval: 90
# успешно, значение — 90
def test_set_interval_valid(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].interval', value=90)
    assert settings_data['triggers'][0]['interval'] == 90


# triggers[0].interval: 90
# затем
# triggers[0].interval
# успешно, значение — дефолт 60
def test_set_interval_valid_and_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].interval', value=90)
    settings_data = settings.set_key(path='triggers[0].interval', value=None)
    assert settings_data['triggers'][0]['interval'] == 60


# triggers[0].interval: qwe
# исключение, указано кривое значение
def test_set_interval_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers[0].interval', value='qwe')


# ticker -----------------------------------------------------------------------

# triggers[0].ticker
# успешно, значение — дефолт словарь с ключами тикера
def test_set_ticker_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker', value=None)

    assert isinstance(settings_data['triggers'][0]['ticker'], dict)
    assert 'markPrice' in settings_data['triggers'][0]['ticker']
    assert 'openInterestValue' in settings_data['triggers'][0]['ticker']
    assert 'symbol' in settings_data['triggers'][0]['ticker']


# triggers[0].ticker: {} (эквивалентно None)
# успешно, значение — дефолт словарь с ключами тикера
def test_set_ticker_emptydict(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[0].ticker', value={})

    assert isinstance(settings_data['triggers'][0]['ticker'], dict)
    assert 'markPrice' in settings_data['triggers'][0]['ticker']
    assert 'openInterestValue' in settings_data['triggers'][0]['ticker']
    assert 'symbol' in settings_data['triggers'][0]['ticker']


# triggers[0].ticker: {valid}
# успешно, значение — словарь valid
def test_set_ticker_validdict(s):
    settings = s.model_copy(deep=True)

    pytest.skip("triggers[0].ticker: {valid}")


# triggers[0].ticker: qwe
# исключение, указано кривое значение
def test_set_ticker_invalid(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValidationError):
        settings_data = settings.set_key(path='triggers[0].ticker', value='qwe')


# /del triggers[0].icon
# исключение, нельзя удалять атрибут
def test_del_icon(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValueError):
        settings_data = settings.del_key(path='triggers[0].icon')
