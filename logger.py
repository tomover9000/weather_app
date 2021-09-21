# this file is running of a cron task every 30 minutes
# it logs the timestamp and temperature into a logfile

from time import strftime
import Adafruit_DHT
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

# initializing the sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 15
# the amount of data that we keep from the past
# 48 data points means 1 day because i read 2 times an hour
DATA_COUNT = 48
logfile = "/home/pi/weather_app/logs/log.csv"
# read data from the sensor
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
# reading the csv into the DataFrame
df = pd.read_csv(logfile)
# add the new data to df
df_toAdd = pd.DataFrame([[strftime("%m-%d %H:%M"), "{:.1f}".format(temperature)]], columns=['timestamp', 'temperature'])
df = df.append(df_toAdd)
# we only keep the last DATA_COUNT entries
df = df.tail(DATA_COUNT)
# writing data to csv
df.to_csv(logfile, index=False, encoding='utf8')

