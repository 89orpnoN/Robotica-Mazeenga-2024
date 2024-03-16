
from mpu6050 import mpu6050
from time import sleep
import numpy
sensor = mpu6050(0x68)


def _3dDictToArr(dictionary): #il ritardato che ha fatto sta libreria ha strutturato in modo strano i valori
    val = []
    for i in ["x","y","z"]:
        val.append(dictionary[i])
    return val
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
        accel_data = _3dDictToArr(accel_data)
        accel.append(accel_data)

        gyro_data = mpu.Sensor.get_gyro_data()
        gyro_data = _3dDictToArr(gyro_data)
        gyro.append(gyro_data)

        print("accel_data: " + str(accel_data))
        print("gyro_data: " + str(gyro_data))



    AccelSamdwich = [accel[0].copy(),accel[0].copy(),accel[0].copy()] #sandwich perché è minore, medio e maggiore
    for i in accel:
        for j in range(3):
            if AccelSamdwich[0][j] > i[j]:
                AccelSamdwich[0][j] = i[j]

            if AccelSamdwich[2][j] < i[j]:
                AccelSamdwich[2][j] = i[j]

            AccelSamdwich[1][j] += i[j]

    mpu.AccelOffset = [AccelSamdwich[1][x] / (-len(accel)) for x in range(3)]

    mpu.AccelIgnore = [numpy.add(AccelSamdwich[0],mpu.AccelOffset),numpy.add(AccelSamdwich[2],mpu.AccelOffset)]

    GyroSamdwich = [gyro[0].copy(),gyro[0].copy(),gyro[0].copy()]
    for i in gyro:
        for j in range(3):
            if GyroSamdwich[0][j] > i[j]: #min
                GyroSamdwich[0][j] = i[j]

            if GyroSamdwich[2][j] < i[j]: #max
                GyroSamdwich[2][j] = i[j]

            GyroSamdwich[1][j] += i[j] #mean

    mpu.GyroOffset = [GyroSamdwich[1][x] / (-len(gyro)) for x in range(3)]
    mpu.GyroIgnore = [numpy.add(GyroSamdwich[0],mpu.GyroOffset).tolist(), numpy.add(GyroSamdwich[2],mpu.GyroOffset).tolist()]

    print("GyroOffset: "+str(mpu.GyroOffset))
    print("GyroIgnore: " + str(mpu.GyroIgnore))
    print("AccelOffset: " + str(mpu.AccelOffset))
    print("AccelIgnore: " + str(mpu.AccelIgnore))

def GetAccelData(mpu): #da implementare
    accel_data = mpu.Sensor.get_accel_data()

def GetAccelData(mpu): #da implementare
    None

mpu = MPU6050()
Calibrate(mpu)

#poi ci sarà anche da fare il "mapper"? (cioè colui che calcola la tua posizione