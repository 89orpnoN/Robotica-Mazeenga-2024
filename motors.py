from gpiozero import Robot as __Robot, Motor as __Motor
from time import sleep as __sleep

robot = __Robot(left=__Motor(5, 6), right=__Motor(12, 13))

def test():
  robot.forward()
  __sleep(1)
  robot.backward()
  __sleep(1)
  robot.right()
  __sleep(1)
  robot.left()
  __sleep(1)
  robot.stop()
  __sleep(1)
