#!/usr/bin/env python

import sys
import logging
import re

from tickbybit import to_yaml
from tickbybit.settings import set_key, del_key

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

# Установить ключ
comm = 'format: str1'
args = re.split(r'\s*:\s*', comm.strip(), 1)
path = args[0]
value = (args[1:] + [None])[0]

settings_new = set_key(dirpath='.settings', path=path, value=value)
print(to_yaml(settings_new))

# Удалить ключ
comm = 'ticker.blablabla'
args = re.split(r'\s*:\s*', comm.strip(), 1)
path = args[0]

settings_new = del_key(dirpath='.settings', path=path)
print(to_yaml(settings_new))
