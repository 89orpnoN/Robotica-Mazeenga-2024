
import VL53L0X
from gpiozero import LED
from time import sleep
def wait():
    sleep(0.5) #serve a gestire il delay dei pin I/O

class Tof_Switch:

  def __init__(self, bus,addr, pin): #salva le informazioni importanti per inizializzare il sensore e poi lo spegne
      self.Xshut = LED(pin)
      self.Off()

      self._IsOpen = False
      self._IsReady = False

      self._bus = bus
      self._address = addr
      self.VL53L0X = None

      self.Timing = None

  def Initialize(self, deactivate = True): #inizializza il sensore e poi lo spegne di default
      self.VL53L0X = VL53L0X.VL53L0X(i2c_bus=self._bus, i2c_address=self._address)

  def On(self): #attiva il sensore
      self.Xshut.on()
      wait()
      self.Activated = True

  def Off(self): #disattiva il sensore
      self.Xshut.off()
      wait()
      self.Activated = False

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

def Setup_Tofs(tofs): #cambia l'indirizzo dei tof in base al loro ordine nell'array
    i = 1
    for tof in tofs:
        if not tof._IsOpen and not tof.Activated:
            if i != 0:
                tof.Initialize(False)
                tof.On()
                ChangeAddress(tof, tof._address + 1)
                tof.Open()
                tof.Off() # una volta aperto non può essere spento ritardato

        else:
            raise Exception("Classe Tof_Switch già inizializzata")
        i+=1



tof = Tof_Switch(1,0x29,17) #canale I2C, Indirizzo base del sensore, pin di disattivazione

tof2 = Tof_Switch(1,0x29,27)

Setup_Tofs([tof,tof2])




tof.On()
StartRanging(tof,75)

tof2.On()
StartRanging(tof2,75)