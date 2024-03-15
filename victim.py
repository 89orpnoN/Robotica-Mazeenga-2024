from gpiozero import LED as __LED

__led = __LED(16)
def victim():
  __led.blink(on_time=0.5, off_time=0.5, n=5)
