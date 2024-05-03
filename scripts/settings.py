#!/usr/bin/env python

import sys
import logging

from tickbybit.settings import get_key, set_key, del_key

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

file = '.settings/settings.yaml'

print("--- key (str)---")
path = 'test1.test1.str'
setvalue = 'testvalue'
set_key(file=file, path=path, value=setvalue)
getvalue = get_key(file=file, path=path)
assert getvalue == setvalue, f'get_key: getvalue = {getvalue}'
del_key(file=file, path=path)
getvalue = get_key(file=file, path=path)
assert getvalue is None, f'get_key: getvalue = {getvalue}'

print("--- key (None) ---")
path = 'test2.test2.none'
setvalue = None
set_key(file=file, path=path, value=setvalue)
getvalue = get_key(file=file, path=path)
assert getvalue == setvalue, f'get_key: getvalue = {getvalue}'
del_key(file=file, path=path)
getvalue = get_key(file=file, path=path)
assert getvalue is None, f'get_key: getvalue = {getvalue}'

print("--- key (dict) ---")
path = 'test3.test3.dict'
setvalue = {'k1': 'v1', 'k2': 'v2'}
set_key(file=file, path=path, value=setvalue)
getvalue = get_key(file=file, path=path)
assert getvalue == setvalue, f'get_key: getvalue = {getvalue}'
del_key(file=file, path=path)
getvalue = get_key(file=file, path=path)
assert getvalue is None, f'get_key: getvalue = {getvalue}'

del_key(file=file, path='*')
