#!/usr/bin/env python
# boot.py -- run on boot-up
import pycom
pycom.lte_modem_en_on_boot(0)
pycom.smart_config_on_boot(0)