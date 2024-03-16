
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

def Calibrate(mpu,samples,padding = 0.05,manualtemp = False, verbose = False):
    if manualtemp:
        mpu.TempOffset = int(input("offset temperatura: ")) #niente error check, se lo scrivi male sono affari tuoi

    print("#"*10  + "stabilizzare il robot" + "#"*10)
    sleep(3)

    accel = []
    gyro = []
    for i in range(samples):
        if verbose:
            print("misurazione: " + str(i))

        accel_data = mpu.Sensor.get_accel_data()
        accel_data = _3dDictToArr(accel_data)
        accel.append(accel_data)

        gyro_data = mpu.Sensor.get_gyro_data()
        gyro_data = _3dDictToArr(gyro_data)
        gyro.append(gyro_data)

        if verbose:
            print("accel_data: " + str(accel_data))
            print("gyro_data: " + str(gyro_data))



    AccelSamdwich = [accel[0].copy(),accel[0].copy(),accel[0].copy()] #sandwich perché è minore, medio e maggiore
    for i in accel: #trova le  x y z minori, maggiori e medie e salvale.
        for j in range(3):
            if AccelSamdwich[0][j] > i[j]:
                AccelSamdwich[0][j] = i[j]

            if AccelSamdwich[2][j] < i[j]:
                AccelSamdwich[2][j] = i[j]

            AccelSamdwich[1][j] += i[j]

    mpu.AccelOffset = [AccelSamdwich[1][x] / (-len(accel)) for x in range(3)]

    mpu.AccelIgnore = [numpy.add(AccelSamdwich[0],mpu.AccelOffset),numpy.add(AccelSamdwich[2],mpu.AccelOffset)]
    accel_abs_error = (numpy.absolute(mpu.AccelIgnore[0]) + numpy.absolute(mpu.AccelIgnore[1]))
    accel_error = accel_abs_error * padding
    mpu.AccelIgnore = [(mpu.AccelIgnore[0] + accel_error).tolist(),(mpu.AccelIgnore[1] + accel_error).tolist()]

    GyroSamdwich = [gyro[0].copy(),gyro[0].copy(),gyro[0].copy()]
    for i in gyro: #trova le  x y z minori, maggiori e medie e salvale.
        for j in range(3):
            if GyroSamdwich[0][j] > i[j]: #min
                GyroSamdwich[0][j] = i[j]

            if GyroSamdwich[2][j] < i[j]: #max
                GyroSamdwich[2][j] = i[j]

            GyroSamdwich[1][j] += i[j] #mean

    mpu.GyroOffset = [GyroSamdwich[1][x] / (-len(gyro)) for x in range(3)]
    mpu.GyroIgnore = [numpy.add(GyroSamdwich[0],mpu.GyroOffset), numpy.add(GyroSamdwich[2],mpu.GyroOffset)]
    gyro_abs_error = (numpy.absolute(mpu.GyroIgnore[0]) + numpy.absolute(mpu.GyroIgnore[1]))
    gyro_error = gyro_abs_error * padding
    mpu.GyroIgnore = [(mpu.GyroIgnore[0] + gyro_error).tolist(),(mpu.GyroIgnore[1] + gyro_error).tolist()]

    if verbose:
        print("AccelOffset: " + str(mpu.AccelOffset))
        print("AccelIgnore: " + str(mpu.AccelIgnore))
        print("accel_error: "+ str(accel_error))
        print("GyroOffset: "+str(mpu.GyroOffset))
        print("GyroIgnore: " + str(mpu.GyroIgnore))
        print("gyro_error: " + str(gyro_error))

def AddOffset(data,offset):
    return numpy.add(data, offset).tolist()

def GetAccelData(mpu): #da implementare
    accel_data = _3dDictToArr(mpu.Sensor.get_accel_data())
    offset_data = AddOffset(accel_data,mpu.AccelOffset)

    cross = numpy.greater(offset_data,mpu.AccelIgnore[1]) & numpy.less(offset_data,mpu.AccelIgnore[0])
    for i in range(3):
        if not cross[i]:
            offset_data[i] = 0.0
    return offset_data.tolist()

def GetGyroData(mpu): #da implementare
    gyro_data = _3dDictToArr(mpu.Sensor.get_gyro_data())
    offset_data = AddOffset(gyro_data, mpu.GyroOffset)

    cross = numpy.greater(offset_data, mpu.GyroIgnore[1]) & numpy.less(offset_data, mpu.GyroIgnore[0])
    for i in range(3):
        if not cross[i]:
            offset_data[i] = 0.0
    return offset_data.tolist()


def test():
    global mpu
    while True:
        print("#" * 20)
        print(GetGyroData(mpu))
        print(GetAccelData(mpu))
        print("#" * 20)


mpu = MPU6050()
Calibrate(mpu,1000,verbose = True,padding = 0.05)
test()

#poi ci sarà anche da fare il "mapper"? (cioè colui che calcola la tua posizione)