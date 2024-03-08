
import VL53L0X
from gpiozero import LED
from time import sleep
def wait():
    sleep(0.5) #serve a gestire il delay dei pin I/O

_base_bus = 1
_base_address = 0x29
_base_rangeMode = VL53L0X.Vl53l0xAccuracyMode.BETTER

class Tof_Switch:

  def __init__(self, bus,addr, pin): #salva le informazioni importanti per inizializzare il sensore e poi lo spegne
      self.Xshut = LED(pin)

      self._IsOpen = False
      self._IsReady = False

      self.Off()


      self._bus = bus
      self._address = addr
      self.VL53L0X = None

      self.Timing = None

  def Initialize(self): #inizializza il sensore e poi lo spegne di default
      self.VL53L0X = VL53L0X.VL53L0X(i2c_bus=self._bus, i2c_address=_base_address)
      self.On()
      ChangeAddress(self.VL53L0X, self._address)
      self.Open()

  def On(self): #attiva il sensore
      self.Xshut.on()
      wait()
      self.Activated = True

  def Off(self): #disattiva il sensore
      if self._IsOpen or self._IsReady:
          raise Exception("Tentativo di disattivazione prima della chiusura")
      self.Xshut.off()
      wait()
      self.Activated = False
      self._IsOpen = False
      self._IsReady = False

  def Open(self):
      self.VL53L0X.open()

      self._IsOpen = True


  def StartRange(self):
      self.VL53L0X.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
      self.Timing = tof.VL53L0X.get_timing()

      self._IsReady = True

  def Close(self):
      self.VL53L0X.stop_ranging()
      self.VL53L0X.close()

      self._IsOpen = False
      self._IsReady = False

def ChangeAddress(tof,new_addr): #cambia l'indirizzo del/dei sensore/i
      tof._address = new_addr
      tof.VL53L0X.change_address(new_addr)


def StartRanging(tof, ranges): # funzione di prova, poco utile in gara

    for count in range(1, ranges):
      distance = Getrange(tof)
      print("%d mm, %d cm, %d" % (distance, (distance / 10), count))


def Getrange(tof): # Ottiene un singolo range
    if not tof._IsOpen:
        tof.Open()
    if not tof._IsReady:
        tof.StartRange()

    distance = tof.VL53L0X.get_distance()
    sleep(tof.Timing / 1000000.00) #si può fare meglio ma così va bene per ora
    return distance


def Setup_Tofs(pins): #cambia l'indirizzo dei tof in base al loro ordine nell'array
    i = 1
    tofs = []
    for pin in pins:
        tof = Tof_Switch(_base_bus,_base_address + i,pin)
        tof.Initialize()
        tofs.append(tof)        
        i+=1

    return tofs

tof, tof2 = Setup_Tofs([17,27])


StartRanging(tof,75)

StartRanging(tof2,75)