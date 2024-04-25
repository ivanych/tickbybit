import logging
import json
import yaml

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


def _plus(value: int | float) -> str:
    return f"{'+' if value > 0 else ''}{value}"


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
    else:
        logger.warning(f"Unknown format \"{settings['format']}\"; used default \"json\"")
        return to_json(data)
