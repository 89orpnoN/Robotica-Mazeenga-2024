import time
import VL53L0X
from gpiozero import LED
from time import sleep
def wait():
    time.sleep(0.5)

class Tof_Switch:

  def __init__(self, bus,addr, pin):
    self.Xshut = pin
    self.Activated = None

    self._bus = bus
    self._address = addr
    self.VL53L0X = None

  def Initialize(self, deactivate = True):
      self.Xshut = LED(self.Xshut)
      self.Xshut.on()
      self.Activated = False

      self.VL53L0X = VL53L0X.VL53L0X(i2c_bus=self._bus, i2c_address=self._address)
      if deactivate: self.On()
  def On(self):
      self.Xshut.on()
      self.Activated = True

  def Off(self):
      self.Xshut.off()
      self.Activated = False


def ChangeAddress(tof,new_addr):
      tof._address = new_addr
      tof.VL53L0X.change_address(new_addr)

def StartRanging(tof, ranges):
    tof.VL53L0X.open()
    tof.VL53L0X.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

    timing = tof.VL53L0X.get_timing()
    if timing < 20000:
      timing = 20000
    print("Timing %d ms" % (timing / 1000))

    for count in range(1, ranges):
      distance = tof.VL53L0X.get_distance()
      if distance > 0:
          print("%d mm, %d cm, %d" % (distance, (distance / 10), count))

      time.sleep(timing / 1000000.00)

    tof.VL53L0X.stop_ranging()
    tof.VL53L0X.close()


tof = Tof_Switch(1,0x29,11)
tof2 = Tof_Switch(1,0x29,13)



tof.Initialize()
tof.Off()


wait()
tof2.Initialize()

wait()
tof.On()
wait()

StartRanging(tof,50)

StartRanging(tof2,50)