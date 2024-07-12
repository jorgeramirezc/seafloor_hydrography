import os
import os.path
import requests
import time
import sys
import xml.etree.ElementTree as ET
import csv
from bluetooth import *
from subprocess import call
import serial

# Wait for the Bluetooth module to load correctly.
time.sleep(3)
print "performing inquiry..."

###### Code section to identify the device to pair with #####
#nearby_devices = discover_devices(lookup_names=True)

#print "found %d devices" % len(nearby_devices)

#for name, addr in nearby_devices:
	#print " %s - %s" % (addr,name)

##############################################################

#Create the client socket
client_socket=BluetoothSocket(RFCOMM)

# Bluetooth connection with Echosounder
client_socket.connect(("00:01:95:35:67:A0",1))
#client_socket.connect(("68:86:E7:07:E3:AD",1))

i=0
j=0
cadena=" "
line2=" "
line3=" "
line1=" "
inicio=1
graba=0

# Set the path to the main directory
path="/home/pi/seafloorusv"

# Create a csv file with all the data collected
csvfiles=[ f for f in os.listdir(path) if f.endswith(".csv")]
csvfiles=sorted(csvfiles)
print csvfiles

if csvfiles:
	ultimo = csvfiles[-1]
	numero = int(ultimo[ultimo.find("-")+1:ultimo.find(".")])
	numero = numero+1
else:
	numero = 0

#Serial Connection with Manta Multiprobe
manta = serial.Serial('/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0', 19200)


with open(path + '/datos-%04i.csv' % (numero),'w') as f:
	#f.write("inicio")
	print "connection done"
	#sys.exit(0)
	while True:
		try:
			data=client_socket.recv(1)
			if (inicio==1):
				if (data=="1"):
					inicio=0
					graba=1
			if (graba==1):
				cadena=cadena+data
				i=i+1

			if (data=='\n'):
				#Read and write multiprobe data
				manta.write('READ\r\n')
				line1 = manta.readline()
				time.sleep(4)

				inicio=1
				graba=0
				#print cadena
				line2=cadena[0:-2]
				cadena=""
				i=0
				#print i
				# Get data from the Trimble GNSS through wireless connection
				response=requests.get('http://192.168.142.1/CACHEDIR2164924914/xml/dynamic/merge.xml?posData=&svData=&configData=')
				xmltext=response.content
        			root=ET.fromstring(xmltext)
       				lat=root.find('.//lat')
				#print lat.text
       				lon=root.find('.//lon')
       				#print lon.text
       				alt=root.find('.//hgt')
       				#print alt.text
       				vel_east=root.find('.//East')
       				#print vel_east.text
       				vel_north=root.find('.//North')
				#print vel_north.text
       				vel_up=root.find('.//Up')
       				#print vel_up.text
      				time_seg=root.find('.//sec')
        			#print time_seg.text
				line3= time_seg.text+" "+vel_up.text+" "+vel_north.text+" "+vel_east.text+" "+alt.text+" "+lon.text+" "+lat.text+" "+line2+" "+line1
				print line3
				# Save all the data of this iteration
				f.write(line3)
                                f.write('\r\n')
				line2=""
				line3=""

#Exceptions handlings				
				
	#except (requests.exceptions.RequestException):        	
	#	print "Wifi communication loss"
	#	time.sleep(40)
	#	response=requests.get('http://192.168.142.1/CACHEDIR216924914/xml/dynamic/merge.xml?posData=&svData=&configData=')
	
		except (btcommon.BluetoothError):
			print "Bluetooth communication loss"
			client_socket.close()
			call("sudo shutdown -h now",shell=True)
			time.sleep(2.5)
			#client_socket=BluetoothSocket(RFCOMM)
			#client_socket.connect(("00:01:95:35:67:A0",1))
			#client_socket.connect(("68:86:E7:07:E3:AD",1))
			#call("sudo shutdown -h now",shell=True)



