
from mpu6050 import mpu6050
from time import sleep

sensor = mpu6050(0x68)

class  MPU6050:
    def __init__(self, bus = 1, addr = 0x68):
        self.Sensor = mpu6050(addr, bus)
        self.AccelOffset = [0,0,0] #XYZ
        self.GyroOffset = [0, 0, 0]  # XYZ
        self.TempOffset = 0
        self.GyroIgnore = [None,None]
        self.AccelIgnore = [None,None]




def Calibrate(mpu,manualtemp = False):
    if manualtemp:
        mpu.TempOffset = int(input("offset temperatura: ")) #niente error check, se lo scrivi male sono affari tuoi
    print("#"*10  + "stabilizzare il robot" + "#"*10)
    sleep(1)
    accel = []
    gyro = []
    for i in range(1000):
        print("misurazione: " + str(i))

        accel_data = mpu.Sensor.get_accel_data()
        accel.append(accel_data)

        gyro_data = mpu.Sensor.get_gyro_data()
        gyro.append(gyro_data)



    AccelSamdwich = [accel[0].copy()*3] #sandwich perché è minore, medio e maggiore
    for i in accel:
        for j in ["x","y","z"]:
            if AccelSamdwich[0][j] > i[j]:
                AccelSamdwich[0][j] = i[j]

            if AccelSamdwich[2][j] < i[j]:
                AccelSamdwich[2][j] = i[j]

            AccelSamdwich[1][j] += i[j]

    mpu.AccelOffset = AccelSamdwich[1]
    mpu.AccelIgnore = [AccelSamdwich[0],AccelSamdwich[2]]

    GyroSamdwich = [gyro[0].copy()*3]
    for i in gyro:
        for j in ["x", "y", "z"]:
            if GyroSamdwich[0][j] > i[j]: #min
                GyroSamdwich[0][j] = i[j]

            if GyroSamdwich[2][j] < i[j]: #max
                GyroSamdwich[2][j] = i[j]

            GyroSamdwich[1][j] += i[j] #mean

    mpu.GyroOffset = GyroSamdwich[1]
    mpu.GyroIgnore = [GyroSamdwich[0], GyroSamdwich[2]]


mpu = MPU6050()
Calibrate(mpu)