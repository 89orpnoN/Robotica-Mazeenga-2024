from ctypes import pointer, c_int

import VL53L0X
from gpiozero import LED
from time import sleep
from py import io


def wait():
    sleep(0.5) #serve a gestire il delay dei pin I/O

def LoadCLib(): #mi serve per accedere direttamente alla API scritta in C
    import sysconfig
    from ctypes import CDLL, c_int,pointer
    import site
    global _TOF_LIBRARY
    # Load VL53L0X shared lib
    suffix = sysconfig.get_config_var('EXT_SUFFIX')
    if suffix is None:
        suffix = ".so"
    _POSSIBLE_LIBRARY_LOCATIONS = ['../bin'] + site.getsitepackages() + [site.getusersitepackages()]
    for lib_location in _POSSIBLE_LIBRARY_LOCATIONS:
        try:
            _TOF_LIBRARY = CDLL(lib_location + '/vl53l0x_python' + suffix)
            break
        except OSError:
            pass
    else:
        raise OSError('Could not find vl53l0x_python' + suffix)

_base_bus = 1
_base_address = 0x29
_base_rangeMode = VL53L0X.Vl53l0xAccuracyMode.BETTER
_TOF_LIBRARY = None
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
      self.On()
      self.VL53L0X = VL53L0X.VL53L0X(i2c_bus=self._bus, i2c_address=_base_address)
      ChangeAddress(self, self._address)
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

        tof = Tof_Switch(_base_bus, _base_address + i, pin)
        #setup del sensore

        tof.Initialize()
        tofs.append(tof)
        wait()
        #controllo che non sia andato a puttane
        err = pointer(c_int(100))
        _TOF_LIBRARY.VL53L0X_GetDeviceErrorStatus(tof.VL53L0X._dev,err)
        err = err.contents.value


        i+=1


    return tofs

LoadCLib()

tof, tof2, tof3 = Setup_Tofs([17,27,22])


#StartRanging(tof,75)

#StartRanging(tof2,75)

#StartRanging(tof3,75)