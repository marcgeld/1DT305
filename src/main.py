#!/usr/bin/env python

import time
import _thread
import pycom
import machine
from machine import RTC
from network import WLAN
from mqtt import MQTTClient
from network import Bluetooth

# Sensor import
from pycoproc_2 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

# Configuration
import config

# Globals
py = Pycoproc()
# Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
mp = MPL3115A2(py,mode=ALTITUDE)
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)
# Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
mpp = MPL3115A2(py,mode=PRESSURE)
wlan = WLAN()
bt = Bluetooth()

def init():
    """ Init function """
    pycom.heartbeat(False)

    # Turn off BlueTooth to save energy
    bt.deinit()

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
    wlan_connected = wlan.ifconfig()
    wlan_ip = wlan_connected[0]
    print('wlan connected '+str(wlan_connected))

    pycom.rgbled(0x00A000)


def clock_sync():
    """ Sync RTC time with NTP server for correct timestamps on Events """
    rtc = RTC()
    rtc.ntp_sync(server="pool.ntp.org")
    print('The RTC is synced via NTP')


def mqtt_callback(topic, msg):
    """ Mqtt callback """
    timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*time.gmtime()[:6])
    print("{timestamp} - {topic} : {msg}".format(timestamp=timestamp,topic=topic,msg=msg))


def loop(client):
    """ RunLoop """

    # Get interface addr.
    wlan_ip = wlan.ifconfig()[0]

    # Light channels (ch0 ~450nm violet-blue and ch1 ~770nm red
    (data0, data1) = lt.light()

    measurement = config.THING_ID
    id = machine.unique_id()
    unit="fipy/{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(id[0], id[1], id[2], id[3], id[4], id[5])
    humidity = str(si.humidity())
    dew = str(si.dew_point())
    temp_mp = str(mp.temperature())
    temp_si = str(si.temperature())
    battery = str(py.read_battery_voltage())
    pressure = str(mpp.pressure())
    light_450 = str(data0)
    light_770 = str(data1)
    lux = str(lt.lux())
    timestamp = str(time.time())


    # InfluxDB line-protocol
    #<measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]
    fmt = ("{measurement},unit={unit},ip={wlan_ip} "
        "humidity={humidity},dewPoint={dew},tempMp={temp_mp},tempSi={temp_si},battery={battery},"
        "pressure={pressure},light_450={light_450},light_770={light_770},lux={lux}"
        " {timestamp}")

    payload = fmt.format(measurement=measurement,unit=unit,wlan_ip=wlan_ip,humidity=humidity,dew=dew,
    temp_mp=temp_mp,temp_si=temp_si,battery=battery,pressure=pressure,
    light_450=light_450,light_770=light_770,lux=lux,timestamp=timestamp)

    print('Sending data:', payload)
    
    # Publish InfluxDB line-protocol to MQTT
    client.publish(topic=config.MQTT_TOPIC, msg=payload, qos=0)

    pycom.rgbled(0x001000)
    time.sleep(config.SLEEP_TIME)
    pycom.rgbled(0x00A000)

    # Check for MQTT msg
    client.check_msg()


def main():
    """ main app """

    print("Connect to mqtt")
    client = MQTTClient(
        config.THING_ID, config.MQTT_BROKER, 
        port=config.MQTT_PORT, 
        keepalive=int(config.MQTT_KEEPALIVE)
    )

    client.set_callback(mqtt_callback)
    resp = client.connect(clean_session=True)
    print("mqttClient connect call returned: {}".format(resp))
    if (resp == 0):
        print("Successfully connected to MQTT Broker")
    client.subscribe(config.MQTT_TOPIC)
    
    while True:
        try:
            loop(client)
            machine.idle()

        # Handle exception
        except KeyboardInterrupt:
            sys.exit(retval=0)

        except Exception as ex:
            sys.print_exception(ex)
            sys.exit(retval=-1)


# The App
print('Starting App')
init()
clock_sync()
main()
