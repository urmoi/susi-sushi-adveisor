import board

import buttonshim
import adafruit_vl53l4cd
from adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit

try:
    buttonshim.setup()
except OSError:
    print("ButtonSHIM : not installed")

try:
    kit = MotorKit(i2c=board.I2C())
except ValueError:
    print("Stepper HAT :  not installed")
            
try:
    kit = ServoKit(channels=16)
except ValueError:
    print("Servo HAT : not installed")

try:
    vl53 = adafruit_vl53l4cd.VL53L4CD(board.I2C())
except ValueError:
    print("ToF Board :  not installed")