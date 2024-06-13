import pytest

from tickbybit.models.settings.settings import Settings


@pytest.fixture()
def s():
    settings = Settings()
    return settings


# triggers[+].interval
# успешно, значение — дефолт 60
def test_set_interval_none(s):
    settings = s.model_copy(deep=True)

    settings_data = settings.set_key(path='triggers[+].interval', value=None)
    assert settings_data['triggers'][0]['interval'] is 60


# /del triggers[0].icon
# исключение, нельзя удалять промежуточный элемент
def test_del_icon(s):
    settings = s.model_copy(deep=True)

    with pytest.raises(ValueError):
        settings_data = settings.del_key(path='triggers[-].icon')
