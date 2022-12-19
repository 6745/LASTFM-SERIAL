import serial
import time
import requests
import json

with open('config.json') as config_file:
  config = json.load(config_file)
  user = config['user']
  api_key = config['api_key']
  serial_port = config['serial_port']
  baud_rate = config['baud_rate']

try:
  ser = serial.Serial( # set parameters, in fact use your own :-)
    port=serial_port,
    baudrate=baud_rate,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE
  )
  ser.isOpen() # try to open port, if possible print message and proceed with 'while True:'
  print ("port is open! \n Sending data.")

except IOError: # if port is already opened, close it and open it again and print message
  ser.close()
  ser.open()
  print ("port was already open, was closed and opened again!")

while True:
    response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&format=json&user={user}&api_key={api_key}&limit=1") #last api limits is 1 request per second.
    data = response.json()
    track = data['recenttracks']['track'][0]
    artist = track['artist']['#text']
    name = track['name']
    text = f'Now playing: {artist} - {name}'+"\n" # Send the text over the serial port
    ser.write(text.encode())
    time.sleep(3) 
