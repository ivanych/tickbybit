from jsonpath_ng.ext import parse


def diff(settings: dict, pair: dict) -> list[dict]:
    """
    Найти изменения в отслеживаемых тикерах между старым и новым прайсами.

    :param settings: Настройки.
    :param pair: Пара сравниваемых прайсов.
    :return: Список изменений тикеров.
    """
    result = []

    # Цикл по отслеживаемым тикерам
    for symbol in settings['tickers']:
        ticker_diff = {
            'symbol': symbol,
            'is_alert': False,
            'time': pair['new']['time'],
            'interval': pair['new']['time'] - pair['old']['time'],
        }

        jsonpath = parse(f'result.list[?symbol = "{symbol}"]')

        old = jsonpath.find(pair['old'])[0]
        new = jsonpath.find(pair['new'])[0]

        # Цикл по атрибутам тикера
        for attr in settings['tickers'][symbol]:

            ticker_diff[attr] = {
                'alert_pcnt': settings['tickers'][symbol][attr]['alert_pcnt'],
                'is_alert': False,
                'old': old.value[attr],
                'new': new.value[attr],
                'pcnt': round(
                    number=float(new.value[attr]) / float(old.value[attr]) * 100 - 100,
                    ndigits=6
                ),
            }

            # Превышена разница по атрибуту?
            if abs(ticker_diff[attr]['pcnt']) >= settings['tickers'][symbol][attr]['alert_pcnt']:
                ticker_diff[attr]['is_alert'] = True
                ticker_diff['is_alert'] = True

        result.append(ticker_diff)

    return result
