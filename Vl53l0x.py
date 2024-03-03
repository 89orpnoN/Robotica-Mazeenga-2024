
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
      if self.VL53L0X != None and self.VL53L0X._dev != None: return True
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
      print("%d mm, %d cm, %d" % (distance, (distance / 10), count))



def Getrange(tof): # Ottiene un singolo range
    if not tof.IsOpen():
        tof.Open()
    print("distanza")
    distance = tof.VL53L0X.get_distance()
    sleep(tof.Timing / 1000000.00) #si può fare meglio ma così va bene per ora
    return distance

def Setup_Tofs(tofs): #cambia l'indirizzo dei tof in base al loro ordine nell'array
    i = 0
    for tof in tofs:
        if not tof.IsOpen() and not tof.Activated:
            if i != 0:
                print("diverso da 1 inizio")
                tof.Initialize(False)
                ChangeAddress(tof, 0x32)
                tof.Open()
                tof.Off()
                print("diverso da 1 fine")
            else:
                tof.Initialize(False)
                tof.Open()
                tof.Off()
                print("uguale a 1")
        else:
            raise Exception("Classe Tof_Switch già inizializzata")
        i+=1



tof = Tof_Switch(1,0x29,17) #canale I2C, Indirizzo base del sensore, pin di disattivazione

tof2 = Tof_Switch(1,0x29,27)

Setup_Tofs([tof,tof2])

print("uscito dal setup")



tof.On()
print("acceso tof")
StartRanging(tof,75)
print("prese misure")

tof2.On()
StartRanging(tof2,75)