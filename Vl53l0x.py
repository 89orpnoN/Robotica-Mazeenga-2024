
import VL53L0X
from gpiozero import LED
from time import sleep
def wait():
    sleep(0.1) #serve a gestire il delay dei pin I/O

class Tof_Switch:

  def __init__(self, bus,addr, pin): #salva le informazioni importanti per inizializzare il sensore e poi lo spegne
      self.Xshut = LED(pin)
      self.Off()

      self._bus = bus
      self._address = addr
      self.VL53L0X = None

      self.Timing = None

  def Initialize(self, deactivate = True): #inizializza il sensore e poi lo spegne di default
      self.On()


      self.VL53L0X = VL53L0X.VL53L0X(i2c_bus=self._bus, i2c_address=self._address)
      if deactivate: self.Off()
  def On(self): #attiva il sensore
      self.Xshut.on()
      self.Activated = True
      wait()

  def Off(self): #disattiva il sensore
      self.Xshut.off()
      self.Activated = False
      wait()

  def IsOpen(self):
      if self.VL53L0X._dev != None: return True
      return False

  def Open(self):
      self.VL53L0X.open()
      self.VL53L0X.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
      self.Timing = tof.VL53L0X.get_timing()


  def Close(self):
      self.VL53L0X.stop_ranging()
      self.VL53L0X.close()

def ChangeAddress(tof,new_addr): #cambia l'indirizzo del/dei sensore/i
      tof._address = new_addr
      tof.VL53L0X.change_address(new_addr)


def StartRanging(tof, ranges): # funzione di prova, poco utile in gara
    if not tof.IsOpen():
        tof.Open()

    for count in range(1, ranges):
      distance = Getrange(tof)
      if distance > 0:
          print("%d mm, %d cm, %d" % (distance, (distance / 10), count))



def Getrange(tof): # funzione di prova, poco utile in gara
    if not tof.IsOpen():
        tof.Open()
    distance = tof.VL53L0X.get_distance()
    sleep(tof.Timing / 1000000.00)
    return distance



tof = Tof_Switch(1,0x29,17)
wait()
tof2 = Tof_Switch(1,0x29,27)
tof2.Initialize(False)
wait()
ChangeAddress(tof2,0x32)
wait()

tof.Initialize()





wait()
tof.On()
wait()

print(StartRanging(tof,75))

print(StartRanging(tof2,75))