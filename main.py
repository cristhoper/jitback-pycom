import ubinascii
from network import Bluetooth

from sensors import SensorVector
from comdev import Comdev, ACC_BACK_MEASUREMENT, GYR_BACK_MEASUREMENT, MAG_BACK_MEASUREMENT

sensorlist = SensorVector()
devices = Comdev()
for id in range(sensorlist.length()):
    try:
        data = sensorlist.get(id).mag.x
        data = bytes(data)
        devices.set_value(characteristic=MAG_BACK_MEASUREMENT, value=data)
    except Exception as err:
        print(err)
