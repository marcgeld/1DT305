# 1DT305 - Introduction to Applied IoT
(Course https://lnu-ftk.instructure.com/courses/233)


## Project overview

The general idea is to measure sun radiation (visual and infrared spectrum) using a TSL2591High Dynamic Range Digital Light Sensor. The sensor is placed inside a green house and to collect metrics in to a InfluxDB database. The sensor is communicating with a Mosquitto MQTT Broker (https://mosquitto.org) via Telegraf middleware (https://www.influxdata.com/time-series-platform/telegraf/) to a InfluxDB (https://www.influxdata.com). Visualization of the data is made primarily in InfluxDB and/or in Chronograf (https://docs.influxdata.com/chronograf/v1.9/)

The design consideration to use the whole or parts of the TICK-stack (Telegraf, InfluxDB, Chronograf and Kapacitor, https://www.influxdata.com/time-series-platform/) is that it is an easy way to aggregate and transform data.

## Objective
The microclimate in our garden greenhouse differs quite a lot from surrounding environment as expected. Today we can measure the result of the solar radiation when that radiation has transformed to heat and are picked up by an array of RuuviTag sensors that continuously collect temperature readings. Usually, you can do a good estimate on the temperature inside the garden greenhouse just by a quick look on the surroundings. A sunny day gives a higher temperature, and a cloudy day gives lower temperature. But some days differs, and the temperature is much higher than expected. The absolute approach would be to use a photon counting device, a single-photon detector (SPD), but that would be immensely expense and clearly out of the bounds for a hobby project. The thesis is that a cheaper device that measuring the photon flux with a broader spectrum of visual and infrared lights will together with a massive amount of data points and applied artificial intelligence will give a good enough prediction about the future temperature within a given timeframe.

The device built within this project deliver at least some form of photon flux measurement and together with multiple [Ruuvi Tag](https://ruuvi.com) sensors and a [Netatmo Weather Station](https://www.netatmo.com/) all integrated to deliver metrics to InfluxDB might give the amount of data needed to see if the thesis is right.

## Bill of Material
Material used for the project is found in the [List here](bom/BOM.md)

## External documentation
[List here](docs)
## Project details

## Computer setup

## Platforms used

## Presenting the data

## Project tasks

- [x] Install Eclipse Mosquitto MQTT broker on Docker.

- [ ] Use the ambient light sensor (LTR-329ALS-01) together with the Temperature and Humidity Sensors (Si7006-A20) on the Pysense 2.0 X Shield to collect metrics and send to InfluxDB via MQTT. Use the Wifi connectivity to connect to the local Wifi access point.

- [ ] Install Telegraf mniddleware on Docker.

- [ ] Install InfluxDB on Docker.

- [ ] Use Network Time Protocol (NTP) to increase precision in timestamping the metrics.

- [ ] Add Monochrome 1.3" 128x64 OLED graphic display with driver SSD1306. The display will be used to display real-time metrics and connectivity data as a mean to simplify the placement in the green house.

- [ ] Replace metrics from LTR-329ALS-01 with metrics from TSL2591High Dynamic Range Digital Light Sensor.

- [ ] Documentation.

