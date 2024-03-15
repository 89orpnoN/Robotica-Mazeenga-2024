import Vl53l0x
from victim import victim
from motors import robot
from gpiozero import Button
from time import sleep

WALL_THRESHOLD = 60

def is_free(tof): return Vl53l0x.Getrange(tof) > WALL_THRESHOLD

switch = Button(23)

while True:
  if switch.value == 0:
    robot.stop()
    continue

  if False:
    victim()

  if is_free(Vl53l0x.tof_dx):
    robot.right()
    sleep(2)
    robot.forward()
    sleep(2)
  elif is_free(Vl53l0x.tof_f):
    robot.forward()
  elif is_free(Vl53l0x.tof_sx):
    robot.left()
    sleep(2)
    robot.forward()
    sleep(2)
  else:
    robot.right()
    sleep(4)
    robot.forward()
