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


class Comdev(object):

    def __init__(self):
        if bt_enabled:
            self.ble = Bluetooth()
            self.chr1 = None
            self.ble.set_advertisement(name="jitback", service_uuid=b'1234567890abcdef')
            self.ble.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=self.__cb_ble_conn)
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

    @staticmethod
    def char1_cb_handler(characteristic):
        events = characteristic.events()
        if events & Bluetooth.CHAR_WRITE_EVENT:
            print("Write request with value = {}".format(characteristic.value()))
        elif events & Bluetooth.CHAR_READ_EVENT:
            print("Bluetooth.CHAR_READ_EVENT")

    def promote(self, device_id=0):
        if device_id == BT_PROMOTE:
            self.ble.advertise(True)
            srv1 = self.ble.service(uuid=b'0000000000001a01', isprimary=True)
            self.chr1 = srv1.characteristic(uuid=b'0000000000001b01', value=0)
            self.chr1.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT,
                               handler=self.char1_cb_handler)
        else:
            pass

    def set_value(self, data):
        if self.chr1 is not None:
            self.chr1.value(data)
