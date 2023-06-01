# SensorBox-V1.1.0
Micropython code and on goingresearch for RP2040 based automatic plant monitoring system. This will be a dump of all my code and research and calibration files.

For now project is an automatic plant watering system that uses Raspberry Pi Pico as the microcontroller and is entirely written in MicroPython.
The system checks soil moisture every set time period and if the moisture is below a certain threshhold, then it activates a relay which turns on a pump to irrigate the crops.
The system also records the moisture data in a csv file for future data analysis.
It also stores the last 12 records in an array which can be sent to a phone for graph analysis via bluetooth to the custom app I created for it using MIT App Inventor.
