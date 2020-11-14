#
# Code to access weather data from Open Weather Map (OWM), and convert this into
# information that is sent to the BBC micro:bit
#
# Corresponding micro:bit code is in ~/mu_code/microbit-code/owm_weather.py

# Import the OWM python library
# https://pyowm.readthedocs.io/en/latest
import pyowm

# Serial comms between Linux and micro:bit
import serial
# os library to expand path in filename
import os

#
# Information about OWM and the OWM API is accessed via this page:
# https://home.openweathermap.org/home
# Here, I read the key for my own personal account
# from a file (not held in this repo)
#
key_filename = os.path.expanduser('~/personal_keys/OpenWeatherMap')
key_file = open(key_filename, 'r')
KEY = key_file.readline()
KEY = KEY[:-1] # Strip newline from the end of the key string

KEY = '5a760e7195cfe829829acb5c6368365d'
# Here, I set the location that I want the weather for
# Again, the right format can found by searching on this page:
# https://openweathermap.org/find
location = 'Kingsteignton, GB'

# Retrieve weather from OWM into fc
owm = pyowm.OWM(KEY)
mgr = owm.weather_manager()
forecast = mgr.three_hours_forecast(location)
fc = forecast.get_forecast()

# fill arrays of weather symbols, temperatures and times
icons = [weather.get_weather_icon_name() for weather in fc]
temps = [weather.get_temperature(unit='celsius') for weather in fc]
times = [weather.get_reference_time('date') for weather in fc]

# Examples of how to extract a single date/time string, temperature and icon
#icon=0
#dt_str=str(times[icon%len(icons)].hour).zfill(2)+':00 '+str(times[icon%len(icons)].day)+'/'+str(times[icon%len(icons)].month)
#temp=temps[icon]["temp"]
#icon=icons[icon]
#print (dt_str,icon,temp)

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
        if b == 'True':
            # Move the previous next range
            fcr += 1
            string_to_send = output_string(fcr,icons,times)
            print(string_to_send)
    except:
        pass
ser.close()

