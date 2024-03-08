from gpiozero import LED
from signal import pause

red = LED(17)

red.blink()

pause()
#per usare diversi sensori Velox bisogna smanettare con gli indirizzi dei bus i2c, non so come funziona ma forse è possibile