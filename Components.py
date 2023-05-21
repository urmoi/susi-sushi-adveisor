import time

import board

# GPIOpip  Library
import RPi.GPIO as GPIO

# Button Hat Library
# https://github.com/pimoroni/button-shim
import buttonshim

# ToF Library
# https://github.com/adafruit/Adafruit_CircuitPython_VL53L4CD
import adafruit_vl53l4cd

# Stepper Motor Kit
# https://github.com/adafruit/Adafruit_CircuitPython_MotorKit
# https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/using-stepper-motors
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper as stepper_settings

# Servo Motor Kit
# https://github.com/adafruit/Adafruit_CircuitPython_ServoKit
# https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/using-the-python-library
from adafruit_servokit import ServoKit


class Button:
    def __init__(self, button: dict):
        try:
            buttonshim.setup()
        except OSError:
            print("ButtonSHIM not installed")
            exit(1)
        
        self._shim_slot = self._find_shim_slot(button.get('slot'))
        self.name: str = button.get('name')
        self.type: str = button.get('type')
        self._state: bool = False
        self._callback = None

        @buttonshim.on_press(self._shim_slot)
        def button_press(button, pressed):
            self.pressed()  

        @buttonshim.on_release(self._shim_slot)
        def button_hold(button, pressed):
            self.released()

    def pressed(self) -> None:
        if self.type == 'button':
            self.select()
        elif self.type == 'toggle':
            self.toggle()
        if self._callback:
            if isinstance(self._callback, list):
                for callback in self._callback:
                    callback()
            else:
                self._callback()

    def released(self) -> None:
        if self.type == 'button':
            self.deselect()
        elif self.type == 'toggle':
            self.toggle()

    def status(self) -> bool:
        return self._state

    def select(self) -> None:
        self._state = True

    def deselect(self) -> None:
        self._state = False

    def toggle(self) -> None:
        self._state = not self._state

    def set_callback(self, callback=None) -> None:
        self._callback = callback

    def _find_shim_slot(self, slot:str) -> int:
        # Find the slot of the button on the Button Shim
        if slot == "A":
            return buttonshim.BUTTON_A
        elif slot == "B":
            return buttonshim.BUTTON_B
        elif slot == "C":
            return buttonshim.BUTTON_C
        elif slot == "D":
            return buttonshim.BUTTON_D
        elif slot == "E":
            return buttonshim.BUTTON_E
        else:
            return None
        

class LEDrgb:
    def __init__(self, led: dict) -> None:
        try:
            buttonshim.setup()
        except OSError:
            print("ButtonSHIM not installed")
            exit(1)
    
        self.name: str = led.get('name')
        self.type: str = led.get('type')
        self._blink_speed = led.get('blink_speed')

    def color(self, rgb_hex: str=0x000000) -> None:
        r, g, b = self._str_2_rgb(rgb_hex)
        buttonshim.set_pixel(r, g, b)

    def blink(self, on_color: str=0x000000, n: int=1) -> None:
        r, g, b = self._str_2_rgb(on_color)
        for _ in range(n):
            buttonshim.set_pixel(r, g, b)
            time.sleep(self._blink_speed/2)
            buttonshim.set_pixel(0x00, 0x00, 0x00)
            time.sleep(self._blink_speed/2)

    def brightness(self, brightness: int) -> None:
        buttonshim.set_brightness(brightness)

    def off(self) -> None:
        buttonshim.set_pixel(0x00, 0x00, 0x00)

    def _str_2_rgb(self, rgb_hex: str) -> tuple:
        # Convert the hexadecimal string to RGB values
        return tuple(int(rgb_hex[i:i+2], 16) for i in (0, 2, 4))
        

class HallSensor:
    # https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/hall.py
    def __init__(self, hall: dict, callback=None):
        self.name: str = hall.get('name')
        self.type: str = hall.get('type')
        self.pin: int = hall.get('pin')
        self.GPIO: int = hall.get('GPIO')
        self._bounce_time: int = 200
        self._callback = callback
        # Set Switch GPIO as input + pull high (no magnet) by default
        if self.GPIO:
            GPIO.setup(self.GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Listen for switch presses
        if callback:
            GPIO.add_event_detect(self.GPIO, GPIO.BOTH, callback=self.state_changed, bouncetime=self._bounce_time)

    def check_init(self) -> bool:
        return bool(self.GPIO)

    def sense_magnet(self) -> bool:
        # if Magnet -> LOW == not True
        return not GPIO.input(self.GPIO)
    
    def state_changed(self) -> bool:
        if self._callback:
            return self._callback(self.sense_magnet())
        return False


class StepperMotor:
    _direction_options = {
        "forward": stepper_settings.FORWARD,
        "backward": stepper_settings.BACKWARD
    }
    def __init__(self, stepper: dict):
        try:
            self._kit = MotorKit(i2c=board.I2C())
        except ValueError:
            print("Stepper HAT not installed")
            exit(1)

        self.name: str = stepper.get('name')
        self.type: str = stepper.get('type')
        self.steps: int = stepper.get('steps')
        self._number: int = stepper.get('number')
        self._stepper1 = self._kit.stepper1
        self._stepper2 = self._kit.stepper2 if self._number == 2 else None
        self._up = self._direction_options[stepper.get('up')]
        self._down = self._direction_options[stepper.get('down')]
        self._style = stepper_settings.DOUBLE
        self.movement: str = None

    def move_up(self, steps: int=1) -> None:
        self.movement = 'up'
        # loop through the number of steps
        for _ in range(steps):
            self._stepper1.onestep(direction=self._up, style=self._style)
            if self._stepper2:
                self._stepper2.onestep(direction=self._up, style=self._style)
        self.movement = None

    def move_down(self, steps: int=1) -> None:
        self.movement = 'down'
        # loop through the number of steps
        for _ in range(steps):
            self._stepper1.onestep(direction=self._down, style=self._style)
            if self._stepper2:
                self._stepper2.onestep(direction=self._down, style=self._style)
        self.movement = None

    def release(self) -> None:
        self._stepper1.release()
        if self._stepper2:
            self._stepper2.release()
        self.movement = None

    def stop(self) -> None:
        self.release()


class ContinuousServoMotor:
    def __init__(self, servo: dict):
        try:
            self._kit = ServoKit(channels=16)
        except ValueError:
            print("Servo HAT not installed")
            exit(1)

        self.name: str = servo.get('name')
        self.type: str = servo.get('type')
        self.slot: int = servo.get('slot')
        self._servo = self._kit.continuous_servo[self.slot]
        self.speed: float = servo.get('speed')
        self._right: float = servo.get('right') * self.speed
        self._left: float = servo.get('left') * self.speed
        self._movement: str = None

    def get_movement(self) -> str:
        return self._movement

    def move_right(self) -> None:
        self._servo.throttle = self._right
        self.movement = 'right'

    def move_left(self) -> None:
        self._servo.throttle = self._left
        self.movement = 'left'

    def stop(self) -> None:
        self._servo.throttle = 0
        self.movement = None


class StandardServoMotor:
    def __init__(self, servo:dict):
        try:
            self._kit:object = ServoKit(channels=16)
        except ValueError:
            print("Servo HAT not installed")
            exit(1)

        self.name: str = servo.get('name')
        self.type: str = servo.get('type')
        self.slot: int = servo.get('slot')
        self._servo = self._kit.servo[self.slot]
        self.neutral: int = servo.get('neutral')
        self.active: int = servo.get('active')
        self._position: str = None

    def check_position(self) -> str:
        return self._position

    def set_position(self, active: bool) -> None:
        if active:
            self.move_active()
        else:
            self.move_neutral()

    def move_neutral(self) -> None:
        self._servo.angle = self.neutral
        self._position = 'neutral'

    def move_active(self) -> None:
        self._servo.angle = self.active
        self._position = 'active'


class ToFDistanceSensor:
    def __init__(self, tof: dict):
        try:
            self._vl53 = adafruit_vl53l4cd.VL53L4CD(board.I2C())
        except ValueError:
            print("ToF Board not installed")

        self.name: str = tof.get('name')
        self.type: str = tof.get('type')
        # self.vl53.inter_measurement = 0
        # self.vl53.timing_budget = 200
        self._vl53.start_ranging()

    def read_distance(self, offset: int=0) -> int:
        # wait for data to be ready
        while not self._vl53.data_ready:
            pass
        # clear the interrupt
        self._vl53.clear_interrupt()
        # return the distance in mm minus the offset
        # reflecting area is not at the front of the table
        return int(self._vl53.distance*10) - offset