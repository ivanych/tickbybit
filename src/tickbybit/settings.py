import json


def settings() -> dict:
    result = {
        'period': 5 * 60 * 1000,  # миллисекунды (5 минут)
        'tickers': {
            'BTCUSDT': {
                'markPrice': {
                    'alert_pcnt': 0.08,  # проценты
                },
                'openInterestValue': {
                    'alert_pcnt': 0.3,  # проценты
                }
            },
            'XCNUSDT': {
                'markPrice': {
                    'alert_pcnt': 0.1,  # проценты
                },
                'openInterestValue': {
                    'alert_pcnt': 0.1,  # проценты
                },
            },
        },
    }

    return result
