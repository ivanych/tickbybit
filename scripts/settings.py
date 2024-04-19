#!/usr/bin/env python

from tickbybit.settings import set_key, del_key

dirpath = '.settings'

path='tickers.BTCUSDT1'
value= {'k1':'v1', 'k2': 'v2'}

# Настройки
#set_key(dirpath=dirpath, path=path)

del_key(dirpath=dirpath, path=path)
