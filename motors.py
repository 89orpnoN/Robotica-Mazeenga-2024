from gpiozero import Robot as __Robot, Motor as __Motor
from time import sleep as __sleep

robot = __Robot(left=__Motor(5, 6), right=__Motor(12, 13))

def test():
  print("forward")
  robot.forward()
  __sleep(1)
  print("backward")
  robot.backward()
  __sleep(1)
  print("right")
  robot.right()
  __sleep(1)
  print("left")
  robot.left()
  __sleep(1)
  print("stop")
  robot.stop()
  __sleep(1)
