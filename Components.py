import time

import board

# GPIOpip  Library
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

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
        self.name: str = button.get('name')
        self.key: str = button.get('key')
        self.type: str = button.get('type')
        self.pin: str = button.get('pin')
        self.gpio: int = button.get('gpio')
        self._bounce_time: int = 500
        self._state: bool = False
        self._callback = None

        if self.gpio:
            # Set Switch GPIO as input + pull high (no magnet) by default
            GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # Listen for switch presses
            GPIO.add_event_detect(self.gpio, GPIO.FALLING, callback=self.pressed, bouncetime=self._bounce_time)


    def pressed(self, pin) -> None:
        if self.type == 'button':
            self.select()
        elif self.type == 'switch':
            self.toggle()
        if self._callback:
            if isinstance(self._callback, list):
                for callback in self._callback:
                    callback()
            else:
                self._callback()

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


class Led:
    def __init__(self, led: dict) -> None:
        self.name: str = led.get('name')
        self.key: str = led.get('key')
        self.type: str = led.get('type')
        self.pin: str = led.get('pin')
        self.gpio: int = led.get('gpio')

        # Set LED GPIO as output
        GPIO.setup(self.gpio, GPIO.OUT)
        # Set LED GPIO to low
        GPIO.output(self.gpio, GPIO.LOW)

    def on(self) -> None:
        GPIO.output(self.gpio, GPIO.HIGH)
    
    def off(self) -> None:
        GPIO.output(self.gpio, GPIO.LOW)
    
    def toggle(self) -> None:
        GPIO.output(self.gpio, not GPIO.input(self.gpio))

    def blink(self, on_time: float=0.5, off_time: float=0.5, n: int=1) -> None:
        for _ in range(n):
            self.on()
            time.sleep(on_time)
            self.off()
            time.sleep(off_time)


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
        self.key: str = stepper.get('key')
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
        self.key: str = servo.get('key')
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
        self.key: str = servo.get('key')
        self.type: str = servo.get('type')
        self.slot: int = servo.get('slot')
        self._servo = self._kit.servo[self.slot]
        self._servo.set_pulse_width_range(500, 2500)
        self.neutral: int = servo.get('neutral')
        self.active: int = servo.get('active')
        self._position: str = None

    def check_position(self) -> str:
        return self._position

    def set_position(self, position: str) -> None:
        if position == 'active':
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
            exit(1)

        self.name: str = tof.get('name')
        self.key: str = tof.get('key')
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
        reading = int(self._vl53.distance*10)
        if offset:
            reading -= offset
        return reading
    

class HallSensor:
    # https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/hall.py
    def __init__(self, hall: dict, callback=None):
        self.name: str = hall.get('name')
        self.key: str = hall.get('key')
        self.type: str = hall.get('type')
        self.pin: int = hall.get('pin')
        self.gpio: int = hall.get('GPIO')
        self._bounce_time: int = 200
        self._callback = callback
        # Set Switch GPIO as input + pull high (no magnet) by default
        if self.gpio:
            GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Listen for switch presses
        # if callback:
        #     GPIO.add_event_detect(self.GPIO, GPIO.BOTH, callback=self.state_changed, bouncetime=self._bounce_time)

    def check_init(self) -> bool:
        return bool(self.gpio)

    def sense_magnet(self) -> bool:
        # if Magnet -> LOW == not True
        return not GPIO.input(self.gpio)
    
    # def state_changed(self) -> bool:
    #     if self._callback:
    #         return self._callback(self.sense_magnet())
    #     return False
    

class GPIOPin:
    def __init__(self, gpio: int):
        self.gpio: int = gpio
        # Set Switch GPIO as input + pull high by default
        GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def sense(self) -> bool:
        return GPIO.input(self.gpio)