from com.mpu9250 import MPU9250


class SensorVector():

    vector = {}
    pins_imu = [  # SDA, SCL
        ('P10', 'P9'),
        ('P8', 'P7'),
        # ('P9', 'P8')
    ]

    def __init__(self):
        i = 0
        for pins in self.pins_imu:
            try:
                self.vector[i] = MPU9250(pins=pins)
                print("Enabling sensor id:{}".format(i))
            except Exception as err:
                print(err)
            i += 1

    def get(self, type=None, id=None):
        if id:
            return self.vector[id]
        else:
            return self.vector

    def length(self):
        return len(self.vector)
