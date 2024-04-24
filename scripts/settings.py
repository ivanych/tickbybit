#!/usr/bin/env python

import sys
import logging
import yaml

from tickbybit.settings import set_key, del_key

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

# Установить ключ
path = 'ticker.blabla.alert_pcnt'
value = 42

settings_new = set_key(dirpath='.settings', path=path, value=value)
print(yaml.dump(settings_new))

# Удалить ключ
path = 'ticker.blabla'

settings_new = del_key(dirpath='.settings', path=path)
print(yaml.dump(settings_new))
