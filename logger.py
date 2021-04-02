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
DATA_COUNT = 30 

# defining the logfile path
logfile = "/home/pi/weather_app/logs/log.csv"

# defining the image path
imgfile = '/home/pi/weather_app/templates/images/history.png'

# read data from the sensor
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

# reading the csv into the DataFrame
df = pd.read_csv(logfile)
# add the new data to df
df_toAdd = pd.DataFrame([[strftime("%m-%d %H:%M"), "{:.1f}".format(temperature)]], columns=['timestamp', 'temperature'])
df = df.append(df_toAdd)
# we only keep the last DATA_COUNT entries
df = df.tail(DATA_COUNT)
size = len(df.index)
# fig size
fig = plt.figure(num=None, figsize=(20, 10), dpi=200, facecolor='w', edgecolor='k')

# setting font size on the plot
plt.rcParams.update({'font.size': 22})

# plotting
plt.plot(df['timestamp'], df['temperature'])

plt.xlabel('Timestamp')
plt.ylabel('Temperature')

# setting only a number of ticks on x axis
# so that they don't overlap
timestamps = df['timestamp']
xticks_count = 20

plt.xticks(np.arange(0, size, size//xticks_count), timestamps[::size//xticks_count])
# setting labels and axes limits
#axes = plt.gca()
#axes.set_ylim([15, 30])
plt.tight_layout();
fig.autofmt_xdate()

# writing data to csv
df.to_csv(logfile, index=False, encoding='utf8')

# saving the image
plt.savefig(imgfile)

