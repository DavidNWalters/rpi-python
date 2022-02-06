#
# Code to access weather data from the Met Office DataHub, and convert this into
# information that is sent to the BBC micro:bit
# Site specific data here is still using "Best Data", which is the most accurate
# way of currently accessing site-specific data.
# Eventually, this will be replaced by IMPROVER data
#
# Import the datahub python library
# https://github.com/bfayers/datahub-python
# Library cloned from github and installed locally using:
# python setup.py install --user
# python3 setup.py install --user
#
# Note that this is a 3rd party library and not provided by Met Office datahub
import datahub
from datahub.Helpers import weather_codes

# Serial comms between Linux and micro:bit
import serial
# os library to expand path in filename
import os
# numpy
import numpy as np

#
# Information about Met Office data point is accessed via this page:
# https://metoffice.apiconnect.ibmcloud.com
# Here, I read the key for my own personal account
# from a file (not held in this repo)
#
key_filename = os.path.expanduser('~/personal_keys/MetOfficeDataHub_WW2MB')
key_file = open(key_filename, 'r')
key = key_file.readline()
key = key[:-1] # Strip newline from the end of the key string
secret = key_file.readline()
secret = secret[:-1] # Strip newline from the end of the key string

# Here, I set the location that I want the weather for
# For now, I'm using information for Kingsteignton
lat = 50.549083
lon = -3.598421

# Set up a list of signifciant weather codes. For simplicity, we map the weather codes
# in Met Office datahub onto the simpler weather types from OpenWeatherMaps.
# For a full list of datahub weather types see the point data FAQ:
# https://metoffice.apiconnect.ibmcloud.com/metoffice/production/faq
#
# These are also available in the datahub module as datahub.Helpers.weather_codes

wx_codes = {'1':'01d', '0':'01n',                         # Clear day/night
            '2':'02d', '3':'02d',                         # Some cloud
            '5':'50d', '6':'50d',                         # Mist/fog
            '7':'03d', '8':'03d',                         # Lots of cloud
            '9':'09n', '10':'09d', '13':'09n', '14':'09d', # Showers
            '11':'10d', '12':'10d', '15':'10d',             # Rain
            '16':'09n', '17':'09d', '19':'09n', '20':'09d', # Sleet/hail showers
            '21':'09n', '25':'09n', '26':'09d',             # Sleet/hail showers
            '18':'13d', '24':'13d', '25':'13n', '26':'13d', # Sleet/snow
            '27':'13d',                                     # Sleet/snow
            '28':'11d', '29':'11d', '30':'11d'}             # Thunder storm

# Set up a datahub connection
conn = datahub.connection(key,secret)

# Retrieve the forecast
forecast = conn.get_forecast(frequency="three-hourly", latitude=lat, longitude=lon)

# Set up some blank arrays in which to hold the forecast data
icons = []         # Weather symbols
times = []         # Forecast validity times
weathernames = []  # Met Office weather type names

# Loop through dates/times of the forecast to fill arrays
for day in forecast.days:
    for i in np.arange(len(day)):
        # Date in datetime format
        times.append(day[i]['time'])
        # Weather type names (for local printing to screen)
        weathernames.append(weather_codes[day[i]['significantWeatherCode']])
        # Weather symbols mapped onto simpler scheme above
        icons.append(wx_codes[str(day[i]['significantWeatherCode'])])

# Device port for micro:bit connected by USB
PORT = "/dev/ttyACM0"

# And settings for the USB serial comms
BAUD = 115200
ser = serial.Serial(PORT)
ser.baudrate = BAUD
ser.parity   = serial.PARITY_NONE
ser.databits = serial.EIGHTBITS
ser.stopbits = serial.STOPBITS_ONE
ser.readline()

#
# Function to put together the output string to write to the screen and the micro:bit
#
def output_string(fcr,icons,times):
    # Start with the weather icon
    string = icons[fcr%len(icons)]
    # Then add the date/time: formatted "hh:00 dd/mm"
    string = string + times[fcr%len(icons)][11:16] + ' ' + times[fcr%len(icons)][8:10] + '/' \
                    + times[fcr%len(icons)][5:7]
    return string

# Start with the first forecast range (fcr=0)
fcr = 0
# Put together the output string, for printing locally 
string_to_print = output_string(fcr,icons,times)
print(string_to_print)
print(weathernames[fcr])

# Set up a continuous loop, sending the output string to the micro:bit whilst waiting for commands to move the forecast range (fcr)
# forward and backward from the micro:bit button presses
while True:
    # Set up the output string
    string_to_send = output_string(fcr,icons,times)
    # and encode this into a bytestring
    ser.write(string_to_send.encode('utf-8'))

    # Look for incoming data from the micro:bit to treat as instructions 
    data = ser.readline().decode('UTF-8')
    data_list = data.rstrip().split(' ')

    # Read button presses in from the serial port
    try:
        a,b = data_list
        if a == 'True':
            # Move the previous forecast range
            fcr -= 1
            string_to_send = output_string(fcr,icons,times)
            print(string_to_send)
            print(weathernames[fcr])
        if b == 'True':
            # Move the previous next range
            fcr += 1
            string_to_send = output_string(fcr,icons,times)
            print(string_to_send)
            print(weathernames[fcr])
    except:
        pass
ser.close()


