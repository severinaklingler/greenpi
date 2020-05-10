# greenpi
Experimentation with Raspberry Pi for gardening


Setup
'git clone git://github.com/severinaklingler/py-spidev
cd py-spidev/
sudo python3 setup.py install'


sudo apt-get install build-essential python-dev python-openssl git
git clone https://github.com/severinaklingler/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
sudo python3 setup.py install


Configure GIPO, sensor switch output must be set to low
gpio=22=op,dl
https://www.raspberrypi.org/documentation/configuration/config-txt/gpio.md


To run the script use
rm output.log
nohup python3 -u bonsaiservant.py &
