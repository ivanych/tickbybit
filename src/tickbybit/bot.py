import logging
import json
import yaml

from aiogram import html

from .ticker_diff import TickerDiff

logger = logging.getLogger("tickbybit.bot")


def notify(diff) -> None:
    print(json.dumps(diff, indent=2))


def to_json(data: dict) -> str:
    return json.dumps(data, indent=2)


def to_yaml(data: dict) -> str:
    return yaml.safe_dump(data)


def to_str1(data: dict) -> str:
    markPrice = data['attrs']['markPrice']['pcnt']
    return f"{data['symbol']} {markPrice}%"


def to_str2(data: dict) -> str:
    markPrice = _plus(data['attrs']['markPrice']['pcnt'])
    return f"{data['symbol']} {markPrice}%"


def to_str3(data: dict) -> str:
    markPrice = data['attrs']['markPrice']['pcnt']
    openInterestValue = data['attrs']['openInterestValue']['pcnt']
    return f"{data['symbol']} markPrice: {markPrice}%, openInterestValue: {openInterestValue}%"


def to_str4(data: dict) -> str:
    markPrice = _plus(data['attrs']['markPrice']['pcnt'])
    openInterestValue = _plus(data['attrs']['openInterestValue']['pcnt'])
    return f"{data['symbol']} markPrice: {markPrice}%, openInterestValue: {openInterestValue}%"


def to_tpl1p(data: dict) -> str:
    symbol = html.bold(data['symbol'])

    price_indicator = _indicator_circle(data['attrs']['markPrice']['pcnt'],
                                        data['attrs']['markPrice']['alert_pcnt'])
    price_pcnt = _plus(data['attrs']['markPrice']['pcnt'])

    oi_indicator = _indicator_circle(data['attrs']['openInterestValue']['pcnt'],
                                     data['attrs']['openInterestValue']['alert_pcnt'])
    oi_pcnt = _plus(data['attrs']['openInterestValue']['pcnt'])

    return (f"{symbol}\n\n"
            f"{price_indicator} Price: {price_pcnt}%    {oi_indicator} OI: {oi_pcnt}%")


def to_tpl2p(data: dict) -> str:
    symbol = html.bold(data['symbol'])

    price_indicator = _indicator_arrow(data['attrs']['markPrice']['pcnt'],
                                       data['attrs']['markPrice']['alert_pcnt'])
    price_pcnt = _plus(data['attrs']['markPrice']['pcnt'])

    oi_indicator = _indicator_arrow(data['attrs']['openInterestValue']['pcnt'],
                                    data['attrs']['openInterestValue']['alert_pcnt'])
    oi_pcnt = _plus(data['attrs']['openInterestValue']['pcnt'])

    return (f"{symbol}\n\n"
            f"{price_indicator} Price  {price_pcnt}%    {oi_indicator} OI  {oi_pcnt}%")


def _plus(value: int | float) -> str:
    return f"{'+' if value > 0 else ''}{value}"


def _indicator_circle(value: int | float, alert: int | float = 0) -> str:
    if abs(value) >= alert:
        return '🟢' if value > 0 else '🔴' if value < 0 else '⚫'
    else:
        return '⚪'


def _indicator_arrow(value: int | float, alert: int | float = 0) -> str:
    if abs(value) >= alert:
        return '🡅' if value > 0 else '🡇' if value < 0 else '●'
    else:
        return '⭘'


def format(td: TickerDiff, settings: dict) -> str:
    data = td.model_dump()

    if settings['format'] == 'json':
        return to_json(data)
    elif settings['format'] == 'yaml':
        return to_yaml(data)
    elif settings['format'] == 'str1':
        return to_str1(data)
    elif settings['format'] == 'str2':
        return to_str2(data)
    elif settings['format'] == 'str3':
        return to_str3(data)
    elif settings['format'] == 'str4':
        return to_str4(data)
    elif settings['format'] == 'tpl1p':
        return to_tpl1p(data)
    elif settings['format'] == 'tpl2p':
        return to_tpl2p(data)
    else:
        logger.warning(f"Unknown format \"{settings['format']}\"; used default \"json\"")
        return to_json(data)
