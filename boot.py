# boot.py -- run on boot-up
from machine import UART
import os
uart = UART(0, 115200)
os.dupterm(uart)

import machine
from network import WLAN

IP = '192.168.43.192'
SUBNET = '255.255.255.0'
GATEWAY = '192.168.43.76'
DNS_SERVER = '8.8.8.8'
SSID = 'nokia hotspot'
WIFI_PASS = 'anustart'

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, WIFI_PASS), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

machine.main('main.py')
