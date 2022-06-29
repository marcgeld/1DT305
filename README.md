# 1DT305 - Introduction to Applied IoT

Marcus Gelderman – mg22nb 
(Course https://lnu-ftk.instructure.com/courses/233)


## Project overview

The general idea is to measure sun radiation (visual and infrared spectrum) using a TSL2591High Dynamic Range Digital Light Sensor. The sensor is placed inside a residential greenhouse and to collect metrics in to a InfluxDB database. The sensor is communicating with a Mosquitto MQTT Broker (https://mosquitto.org) via Telegraf middleware (https://www.influxdata.com/time-series-platform/telegraf/) to a InfluxDB (https://www.influxdata.com). Visualization of the data is made primarily in InfluxDB and/or in Chronograf (https://docs.influxdata.com/chronograf/v1.9/)

The design consideration to use the whole or parts of the TICK-stack (Telegraf, InfluxDB, Chronograf and Kapacitor, https://www.influxdata.com/time-series-platform/) is that it is an easy way to aggregate and transform data.

## Objective

The microclimate in our residential greenhouse differs quite a lot from surrounding environment as expected. Today we can measure the result of the solar radiation when that radiation has transformed to heat and are picked up by an array of RuuviTag sensors that continuously collect temperature readings. Usually, you can do a good estimate on the temperature inside the residential greenhouse just by a quick look on the surroundings. A sunny day gives a higher temperature, and a cloudy day gives lower temperature. But some days differs, and the temperature is much higher than expected. The absolute approach would be to use a photon counting device, a single-photon detector (SPD), but that would be immensely expense and clearly out of the bounds for a hobby project. The thesis is that a cheaper device that measuring the photon flux with a broader spectrum of visual and infrared lights will together with a massive amount of data points and applied artificial intelligence will give a good enough prediction about the future temperature within a given timeframe.

The device built within this project deliver at least some form of photon flux measurement and together with multiple [Ruuvi Tag](https://ruuvi.com) sensors and a [Netatmo Weather Station](https://www.netatmo.com/) all integrated to deliver metrics to InfluxDB might give the amount of data needed to see if the thesis is right.

## Bill of Material

Material used for the project is found in the [Bill of Material list](bom/BOM.md)

## External documentation

### Docker installations

To install the Docker engine there is a [guide](https://docs.docker.com/engine/install/ubuntu/) to help you get started. Another possibility is to [Running Docker Containers on Synology NAS](https://linuxhint.com/run-docker-containers-synology-nas/)

#### Mosquitto MQTT Broker

A Guide to [run the MQTT Broker Docker](https://blog.feabhas.com/2020/02/running-the-eclipse-mosquitto-mqtt-broker-in-a-docker-container/)

#### InfluxDB and Telegraf

I follow this guide [running InfluxDB 2.0 and Telegraf using docker](https://www.influxdata.com/blog/running-influxdb-2-0-and-telegraf-using-docker/) to run local
copies of InfluxDB and Telegraf on my Docker engine.

## Project details

### Verify connection to MQTT Broker

To verify the MQTT connection setup, you can use the supplied Python script in the [utility](utility/) folder.
If you are successfully connected to MQTT you will get something like this in the MQTT log:

```text
2022-06-27T23:44:03: Sending CONNACK to python-mqtt-399 (0, 0)
2022-06-27T23:44:03: Received PUBLISH from python-mqtt-399 (d0, q0, r0, m0, 'python_mqtt', ... (23 bytes))
2022-06-27T23:44:03: Client python-mqtt-399 closed its connection.
```

And something like this as output from the Python program

```text
Connected OK Returned code= 0
Send `messages to python_mqtt` to topic `python_mqtt`
```

## Computer setup

## Platforms used

The metrics from the sensor setup is sent to Mosquitto MQTT Broker via WiFi once per minute. The use of WiFi and a private WiFi network is chosen because of the simplicity of moving the sensor metrics to a local InfluxDB database. The WiFi network the sensor connects to is separated from the residential WiFi with a firewall and only the MQTT protocol is allowed to pass through. If another connection type like LoRaWAN or a cellular network where to be used, an off-site storage like [Amazon AWS](https://aws.amazon.com) or other cloud solution would be needed to temporary store the metrics and a polling mechanism to retrieve the metrics has to be used to handle the security constrains.

## Presenting the data

## Project tasks

- [x] Install Eclipse Mosquitto MQTT broker on Docker.

- [ ] Use the ambient light sensor (LTR-329ALS-01) together with the Temperature and Humidity Sensors (Si7006-A20) on the Pysense 2.0 X Shield to collect metrics and send to InfluxDB via MQTT. Use the Wifi connectivity to connect to the local Wifi access point.

- [x] Install Telegraf mniddleware on Docker.

- [x] Install InfluxDB on Docker.

- [ ] Use Network Time Protocol (NTP) to increase precision in timestamping the metrics.

- [ ] Add Monochrome 1.3" 128x64 OLED graphic display with driver SSD1306. The display will be used to display real-time metrics and connectivity data as a mean to simplify the placement in the residential greenhouse.

- [ ] Replace metrics from LTR-329ALS-01 with metrics from TSL2591High Dynamic Range Digital Light Sensor.

- [ ] Documentation.

