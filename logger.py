# this file is running of a cron task every 30 minutes
# it logs the timestamp and temperature into a logfile

from time import strftime
import Adafruit_DHT
import pandas as pd
import sys
import matplotlib.pyplot as plt

# initializing the sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 15

# defining the logfile path
logfile = "/home/pi/weather_app/logs/log.csv"

#defining the image path
imgfile = '/home/pi/weather_app/templates/images/history.png'

# writing the new data in the csv
with open(logfile, "a") as log:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    log.write("{},{:.1f}\n".format(strftime("%m-%d %H:%M"), temperature))
    log.close()


# writing the new image on the disk
df = pd.read_csv(logfile)
fig = plt.figure(num=None, figsize=(20, 10), dpi=200, facecolor='w', edgecolor='k')

# setting font size on the plot
plt.rcParams.update({'font.size': 22})

# plotting
plt.plot(df['timestamp'], df['temperature'])

# setting labels and axes limits
plt.xlabel('Timestamp')
plt.ylabel('Temperature')
axes = plt.gca()
axes.set_ylim([15, 30])
plt.tight_layout();
fig.autofmt_xdate()

# saving the image
plt.savefig(imgfile)

