import time
import VL53L0X
from gpiozero import LED
from time import sleep


Xshut = LED(11)
Xshut2 = LED(13)
# Create a VL53L0X object
Xshut2.on()
time.sleep(0.1)
tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
Xshut2.off()
time.sleep(0.1)
Xshut.on()
tof2 = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x30)
Xshut.off()
# I2C Address can change before tof.open()
# tof.change_address(0x32)
tof.open()
# Start ranging
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing/1000))

for count in range(1, 301):
    distance = tof.get_distance()
    if distance > 0:
        print("%d mm, %d cm, %d" % (distance, (distance/10), count))

    time.sleep(timing/1000000.00)

tof.stop_ranging()
tof.close()
