#
# Code to access weather data from the Met Office DataPoint, and convert this into
# information that is sent to the BBC micro:bit
# Site specific data here is basically "Best Data", which is still
# the most accurate way of accessing site-specific data.
#
# Import the datapoint python library
# https://datapoint-python.readthedocs.io/en/latest/getting-started.html
# Note that this is a 3rd party library and not provided by Met Office datapoint
import datapoint

# Serial comms between Linux and micro:bit
import serial
# os library to expand path in filename
import os

#
# Information about Met Office data point is accessed via this page:
# https://www.metoffice.gov.uk/services/data/datapoint
# Here, I read the key for my own personal account
# from a file (not held in this repo)
#
key_filename = os.path.expanduser('~/personal_keys/MetOfficeDataPoint')
key_file = open(key_filename, 'r')
KEY = key_file.readline()
KEY = KEY[:-1] # Strip newline from the end of the key string

# Here, I set the location that I want the weather for
# For now, I'm using information for Kingsteignton
lat = 50.549083
lon = -3.598421

# Set up a dictionary for weather types. For simplicity, we map the weather types
# in Met Office datapoint onto the simpler weather types from OpenWeatherMaps.
# For a full list of datapoint weather types see:
# https://www.metoffice.gov.uk/binaries/content/assets/metofficegovuk/pdf/data/datapoint_api_reference.pdf


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

# Set up a datapoint connection
conn = datapoint.connection(api_key=KEY)

# Find the nearest forecast site location to my input lat/lon
site = conn.get_nearest_forecast_site(lat, lon)
print (site.name)

# Retrieve the forecast
forecast = conn.get_forecast_for_site(site.id, "3hourly")

# Set up some blank arrays in which to hold the forecast data
icons = []         # Weather symbols
times = []         # Forecast validity times
weathernames = []  # Met Office weather type names

# Loop through dates/times of the forecast to fill arrays
for day in forecast.days:
    for timestep in day.timesteps:
        # Date in datetime format
        times.append(timestep.date)
        # Weather type names (for local printing to screen)
        weathernames.append(timestep.weather.text)
        # Weather symbols mapped onto simpler scheme above
        icons.append(wx_codes[timestep.weather.value])

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
    string = string + str(times[fcr%len(icons)].hour).zfill(2)+':00 '+str(times[fcr%len(icons)].day).zfill(2)+'/'+str(times[fcr%len(icons)].month).zfill(2)
    return string

# Start with the first forecast range (fcr=0)
fcr = 0
# Put together the output string, for printing locally 
string_to_print = output_string(fcr,icons,times)
print (string_to_print)

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


