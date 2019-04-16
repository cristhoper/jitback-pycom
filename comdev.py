import ubinascii
from network import Bluetooth

BT_PROMOTE = 1
WF_PROMOTE = 2
LR_PROMOTE = 3

# Get values from sys configuration
bt_enabled = True
wifi_enable = False
lora_enabled = False
wifi_config = None

# https://docs.pycom.io/firmwareapi/pycom/network/bluetooth/
# https://github.com/pycom/pycom-micropython-sigfox/issues/40

POSITION_SERVICE = b'000000000000180d'

ACC_BACK_MEASUREMENT = b'0000000000002a38'
GYR_BACK_MEASUREMENT = b'0000000000002a3b'
MAG_BACK_MEASUREMENT = b'0000000000002a3f'


class Comdev(object):

    def __init__(self):
        if bt_enabled:
            self.ble = Bluetooth()
            self.chr1 = None
            self.ble.set_advertisement(name="jitback", service_uuid=POSITION_SERVICE)
            self.ble.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED,
                              handler=self.__cb_ble_conn)
            self.promote(BT_PROMOTE)
        if wifi_enable and wifi_config:
            # TODO wifi staffs and get configuration to set_advertisement
            pass
        if lora_enabled:
            # TODO wifi staffs and get configuration to set_advertisement
            pass

    def __cb_ble_conn(self, bt):
        """
        Callback for connection
        """
        e = bt.events()
        if e & Bluetooth.CLIENT_CONNECTED:
            print("connected")
            self.ble.advertise(False)
        elif e & Bluetooth.CLIENT_DISCONNECTED:
            print("disconnected")
            self.promote(BT_PROMOTE)

    def characteristic_cb(self, characteristic):
        events = characteristic.events()
        if events & Bluetooth.CHAR_WRITE_EVENT:
            print("Write request with value = {} for {}".format(characteristic.value(), characteristic.uuid()))
        elif events & Bluetooth.CHAR_READ_EVENT:
            print("Bluetooth.CHAR_READ_EVENT")

    def promote(self, device_id=0):
        if device_id == BT_PROMOTE:
            self.ble.advertise(True)
            srv1 = self.ble.service(uuid=POSITION_SERVICE, isprimary=True)
            self.chr1 = srv1.characteristic(uuid=ACC_BACK_MEASUREMENT, value=1)
            self.chr2 = srv1.characteristic(uuid=GYR_BACK_MEASUREMENT, value=2)
            self.chr3 = srv1.characteristic(uuid=MAG_BACK_MEASUREMENT, value=3)
            self.chr1.callback(Bluetooth.CHAR_READ_EVENT, handler=self.characteristic_cb)
            self.chr2.callback(Bluetooth.CHAR_READ_EVENT, handler=self.characteristic_cb)
            self.chr3.callback(Bluetooth.CHAR_READ_EVENT, handler=self.characteristic_cb)
        else:
            pass

    def set_value(self, characteristic, data):
        if characteristic is None:
            return
        elif characteristic == ACC_BACK_MEASUREMENT:
            self.chr1.value(value=data)
        elif characteristic == GYR_BACK_MEASUREMENT:
            self.chr2.value(value=data)
        elif characteristic == MAG_BACK_MEASUREMENT:
            self.chr3.value(value=data)
