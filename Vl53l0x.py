import time
import VL53L0X
from gpiozero import LED
from time import sleep
def wait():
    time.sleep(0.5)

class Tof_Switch:

  def __init__(self, bus,addr, pin):
    self.Xshut = pin
    self.VL53L0X = None
    self._bus = bus
    self._address = addr

  def Initialize(self, deactivate = True):
      self.Xshut = LED(self.Xshut)
      self.Xshut.off()
      self.VL53L0X = VL53L0X.VL53L0X(i2c_bus=self._bus, i2c_address=self._address)
      self.VL53L0X.open()
      if deactivate: self.open()
  def open(self):
      self.Xshut.off()

  def close(self):
      self.Xshut.on()

  def ChangeAddress(self,new_addr):
      self._address = new_addr
      self.VL53L0X.change_address(new_addr)

tof = Tof_Switch(1,0x29,11)
tof2 = Tof_Switch(1,0x29,13)


tof.Initialize()

wait()

wait()
tof2.Initialize(False)
tof2.ChangeAddress(0x32)
tof2.close()

wait()
tof.open()
wait()

# Start ranging
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.VL53L0X.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing/1000))

for count in range(1, 101):
    distance = tof.VL53L0X.get_distance()
    if distance > 0:
        print("%d mm, %d cm, %d" % (distance, (distance/10), count))

    time.sleep(timing/1000000.00)

tof.VL53L0X.stop_ranging()
tof.VL53L0X.close()
