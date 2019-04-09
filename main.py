import ubinascii
from network import Bluetooth

from sensors import SensorVector
#from comdev import Comdev

sensorlist = SensorVector()

for id in range(sensorlist.length()):
    try:
        print(sensorlist.get(id).sensors())
    except Exception as err:
        print(err)
