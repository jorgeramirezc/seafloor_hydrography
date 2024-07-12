# Seafloor Hydrography Script
This script is used to perform hydrography of water bodies using the **USV Hydrone** from Seafloor, which has been modified by Tumi Robotics to integrate additional sensors and automate the data collection process.

# Hardware
The main components of this system are:

-   Modified control box (with added Rasp Pi 3b + PixHawk)
-   Multiparametric probe Manta
-   Single-beam echo sounder
-   GNSS antenna Trimble SPS 585

## Connection with Multiparametric Probe

The multiparametric probe connects via serial communication. It defaults to the RS232 communication protocol, so an RS232 to USB adapter is used.

## Connection with Single-beam Echo Sounder

The echo sounder used has a Bluetooth module, which includes an LED that indicates when a connection has been established. Once connected, the LED will show a steady blue light.

## Connection with Trimble GNSS Antenna

This connection is established automatically as long as it is the only connection stored in the internal configuration files of the Raspberry Pi. The GNSS antenna creates its own wireless network, which can be monitored from any device using the following address: [http://192.168.1.1/login_security.html](http://192.168.1.1/login_security.html)

There is an indicator LED on the antenna panel that will stop blinking once the connection is established.

# Configuration of Rasp Pi 3


After powering on the robot, the Raspberry Pi will automatically run the Python script. To achieve this, you need to configure the crontab process scheduler. Run the following in a terminal:

`crontab -e` 

This command opens the crontab file in the default editor.

After the editor opens, scroll to the bottom of the file. Add the following line:

`@reboot python3 /home/pi/seafloorusv/usv_hydro_v3.py`

# Diagram Connection

![Diagram Connection](URL_de_la_imagen)  
