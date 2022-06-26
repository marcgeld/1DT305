# 1DT305 - Introduction to Applied IoT
(Course https://lnu-ftk.instructure.com/courses/233)


## Project overview

The general idea is to measure sun radiation (visual and infrared spectrum) using a TSL2591High Dynamic Range Digital Light Sensor. The sensor is placed inside a green house and to collect metrics in to a InfluxDB database. The sensor is communicating with a Mosquitto MQTT Broker (https://mosquitto.org) via Telegraf middleware (https://www.influxdata.com/time-series-platform/telegraf/) to a InfluxDB (https://www.influxdata.com). Visualization of the data is made primarily in InfluxDB and/or in Chronograf (https://docs.influxdata.com/chronograf/v1.9/)

The design consideration to use the whole or parts of the TICK-stack (Telegraf, InfluxDB, Chronograf and Kapacitor, https://www.influxdata.com/time-series-platform/) is that it is an easy way to aggregate and transform data.


## Project details


## Project tasks

- [x] Install Eclipse Mosquitto MQTT broker on Docker.

- [ ] Use the ambient light sensor (LTR-329ALS-01) together with the Temperature and Humidity Sensors (Si7006-A20) on the Pysense 2.0 X Shield to collect metrics and send to InfluxDB via MQTT. Use the Wifi connectivity to connect to the local Wifi access point.

- [ ] Install Telegraf mniddleware on Docker.

- [ ] Install InfluxDB on Docker.

- [ ] Use Network Time Protocol (NTP) to increase precision in timestamping the metrics.

- [ ] Add Monochrome 1.3" 128x64 OLED graphic display with driver SSD1306. The display will be used to display real-time metrics and connectivity data as a mean to simplify the placement in the green house.

- [ ] Replace metrics from LTR-329ALS-01 with metrics from TSL2591High Dynamic Range Digital Light Sensor.

- [ ] Documentation.
