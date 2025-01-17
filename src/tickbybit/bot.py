import logging
import json
import yaml

from aiogram import html

from .ticker_diff import TickerDiff

logger = logging.getLogger("tickbybit.bot")


class IndentSafeDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentSafeDumper, self).increase_indent(flow, False)


def notify(diff) -> None:
    print(json.dumps(diff, indent=2))


def to_json(data: dict) -> str:
    return json.dumps(data, indent=2)


def to_yaml(data: dict) -> str:
    return yaml.dump(data, Dumper=IndentSafeDumper, allow_unicode=True)


def to_str1(data: dict, p: bool = False) -> str:
    price_pcnt = data['attrs']['markPrice']['pcnt']

    if p:
        price_pcnt = _plus(price_pcnt)

    return f"{data['interval']} сек | {data['symbol']} {price_pcnt}%"


def to_str2(data: dict, p: bool = False) -> str:
    price_pcnt = data['attrs']['markPrice']['pcnt']
    oi_pcnt = data['attrs']['openInterestValue']['pcnt']

    if p:
        price_pcnt = _plus(price_pcnt)
        oi_pcnt = _plus(oi_pcnt)

    return f"{data['interval']} сек | {data['symbol']} markPrice: {price_pcnt}%, openInterestValue: {oi_pcnt}%"


def to_tpl1(data: dict, p: bool = False, i: str = 'arrow') -> str:
    symbol = html.bold(data['symbol'])

    # Иконка триггера
    icon = _icon(data['icon'])

    indicator = globals()[f'_indicator_{i}']

    price_indicator = indicator(
        got=data['attrs']['markPrice']['pcnt'],
        expected=data['attrs']['markPrice']['filters']['absolute']['value']
    )
    price_pcnt = _plus(data['attrs']['markPrice']['pcnt'])

    oi_indicator = indicator(
        got=data['attrs']['openInterestValue']['pcnt'],
        expected=data['attrs']['openInterestValue']['filters']['absolute']['value']
    )
    oi_pcnt = _plus(data['attrs']['openInterestValue']['pcnt'])

    return (f"{icon}{data['interval']} сек | {symbol}\n\n"
            f"{price_indicator} Price  {price_pcnt}%    {oi_indicator} OI  {oi_pcnt}%")


def to_tpl2(data: dict, p: bool = False, i: str = 'circle') -> str:
    symbol = html.bold(data['symbol'])

    # Иконка триггера
    icon = _icon(data['icon'])

    indicator = globals()[f'_indicator_{i}']

    price_indicator = indicator(
        got=data['attrs']['markPrice']['pcnt'],
        expected=data['attrs']['markPrice']['filters']['absolute']['value']
    )
    price_pcnt = _plus(data['attrs']['markPrice']['pcnt'])

    oi_indicator = indicator(
        got=data['attrs']['openInterestValue']['pcnt'],
        expected=data['attrs']['openInterestValue']['filters']['absolute']['value']
    )
    oi_pcnt = _plus(data['attrs']['openInterestValue']['pcnt'])

    return (f"{icon}{data['interval']} сек | {symbol}\n\n"
            f"{price_indicator} <code>Price {price_pcnt}%</code>\n"
            f"{oi_indicator} <code>OI    {oi_pcnt}%</code>")


def _plus(value: int | float) -> str:
    return f"{'+' if value > 0 else ''}{value}"


def _icon(icon) -> str:
    if icon:
        return icon + ' '
    else:
        return ''


def _indicator_circle(got: int | float, expected: int | float = 0) -> str:
    if abs(got) >= expected:
        return '🟢' if got > 0 else '🔴' if got < 0 else '⚫'
    else:
        return '⚪'


def _indicator_square(got: int | float, expected: int | float = 0) -> str:
    if abs(got) >= expected:
        return '🟩' if got > 0 else '🟥' if got < 0 else '️️️️️️️️⬛️'
    else:
        return '⬜️'


def _indicator_arrow(got: int | float, expected: int | float = 0) -> str:
    if abs(got) >= expected:
        return '🡅' if got > 0 else '🡇' if got < 0 else '●'
    else:
        return '⭘'


def format(td: TickerDiff, format: str) -> str:
    data = td.model_dump()

    if format == 'json':
        return to_json(data)
    elif format == 'yaml':
        return to_yaml(data)
    elif format == 'str1':
        return to_str1(data)
    elif format == 'str1p':
        return to_str1(data, p=True)
    elif format == 'str2':
        return to_str2(data)
    elif format == 'str2p':
        return to_str2(data, p=True)
    elif format == 'tpl1pa':
        return to_tpl1(data, i='arrow')
    elif format == 'tpl1pc':
        return to_tpl1(data, i='circle')
    elif format == 'tpl1ps':
        return to_tpl1(data, i='square')
    elif format == 'tpl2pa':
        return to_tpl2(data, i='arrow')
    elif format == 'tpl2pc':
        return to_tpl2(data, i='circle')
    elif format == 'tpl2ps':
        return to_tpl2(data, i='square')

    else:
        logger.warning(f"Unknown format \"{format}\"; used default \"json\"")
        return to_json(data)
