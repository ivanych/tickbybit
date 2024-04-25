#!/usr/bin/env python

import sys
import logging
import yaml
import re

from tickbybit.settings import set_key, del_key

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

# Установить ключ
comm = 'ticker.blablabla.alert_pcnt: 1'
args = re.split(r'\s*:\s*', comm.strip(), 1)
path = args[0]
value = (args[1:] + [None])[0]

settings_new = set_key(dirpath='.settings', path=path, value=value)
print(yaml.dump(settings_new))

# Удалить ключ
comm = 'ticker.blablabla'
args = re.split(r'\s*:\s*', comm.strip(), 1)
path = args[0]

settings_new = del_key(dirpath='.settings', path=path)
print(yaml.dump(settings_new))
