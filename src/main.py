#!/usr/bin/env python

import time
import _thread
import pycom
import machine
from machine import RTC
from network import WLAN
from mqtt import MQTTClient

from network import Bluetooth
from pycoproc_2 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

import config

pycom.heartbeat(False)

# Turn off BlueTooth to save energy
bt = Bluetooth()
bt.deinit()

wlan = WLAN()
print("Connect to WiFi")
wlan.deinit()
time.sleep(1)
wlan.init(mode=WLAN.STA)
time.sleep(1)
wlan.ifconfig(id=0, config='dhcp')
time.sleep(1)

wlan.connect(ssid=config.WIFI_SSID, auth=(WLAN.WPA2, config.WIFI_PASS))
pycom.rgbled(0x200000)

while not wlan.isconnected():
    pycom.rgbled(0x205020)
    time.sleep(1)
    pycom.rgbled(0x502050)
    time.sleep(2)


print("WiFi connected succesfully")
print('wlan connected '+str(wlan.ifconfig()))
pycom.rgbled(0x00A000)


# Sync time via NTP server for GW timestamps on Events
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")
print('The RTC is synced via NTP')

py = Pycoproc()
# Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
mp = MPL3115A2(py,mode=ALTITUDE)
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)
# Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
mpp = MPL3115A2(py,mode=PRESSURE)

## mqtt
print("Connect to mqtt")
#client = MQTTClient(config.THING_ID, config.MQTT_BROKER, port=int(config.MQTT_PORT), keepalive=int(config.MQTT_KEEPALIVE))
client = MQTTClient(config.THING_ID, config.MQTT_BROKER, port=config.MQTT_PORT, keepalive=int(config.MQTT_KEEPALIVE))

resp = client.connect(clean_session=True)
print("mqttClient connect call returned: {}".format(resp))
if (resp == 0):
    print("Successfully connected to MQTT Broker")

while True:

    # Light channels (ch0 ~450nm violet-blue and ch1 ~770nm red
    (data0, data1) = lt.light()


    measurement = "FiPy"
    unit = wlan.mac()
    humidity = str(si.humidity())
    dew = str(si.dew_point())
    temp_mp = str(mp.temperature())
    temp_si = str(si.temperature())
    battery = str(py.read_battery_voltage())
    pressure = str(mpp.pressure())
    light_450 = str(data0)
    light_770 = str(data1)
    lux = str(lt.lux())
    #timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*time.gmtime()[:6])
    timestamp = str(time.time())


    # InfluxDB line-protocol
    #<measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]

    d = ("{measurement},unit={unit} "
        "humidity={humidity},dewPoint={dew},tempMp={temp_mp},tempSi={temp_si},battery={battery},"
        "pressure={pressure},light_450={light_450},light_770={light_770},lux={lux}"
        " {timestamp}")

    msg = d.format(measurement=measurement,unit=unit,humidity=humidity,dew=dew,
    temp_mp=temp_mp,temp_si=temp_si,battery=battery,pressure=pressure,
    light_450=light_450,light_770=light_770,lux=lux,timestamp=timestamp)

    print(msg)

    client.publish(topic=config.MQTT_TOPIC, msg=msg)
    time.sleep(config.SLEEP_TIME)





