import Accelerometer as am #citazione ad IHNMAIMS (i have no mouth)
import time
import numpy

Angular_V = numpy.array([0,0,0]) #XYZ
gyro_data = None
current_rotation = numpy.array([0,0,0])
cycle_T = time.process_time_ns()
def nm_to_s(int): return int / 1000000
def deltaT(time):
    return time.process_time_ns() - time
while True:
    gyro_data = numpy.array(am.GetGyroData(am.mpu))
    added_velocity = gyro_data * nm_to_s(deltaT(cycle_T))
    Angular_V = Angular_V + added_velocity
    current_rotation = current_rotation + (Angular_V * nm_to_s(deltaT(cycle_T)))
    print("current_rotation: " + str(current_rotation))
    print("added_velocity: " + str(added_velocity))
    print("Angular_V: " + str(Angular_V))
    print("gyro_data: " + str(gyro_data))
    print("cycle_T: " + str(cycle_T))

    cycle_T = time.process_time_ns()

