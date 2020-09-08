#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pywemo

devices = pywemo.discover_devices()
print(devices)

devCount = len(devices)
print( devCount, " devices found.")

#while (curDevIdx < devCount):
for dev in devices:
    print('Toggling ', dev.name)
    dev.toggle()

print('All Done Toggling!')
