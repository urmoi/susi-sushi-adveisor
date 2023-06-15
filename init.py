from Components import (
    StepperMotor, ContinuousServoMotor, StandardServoMotor,
    ToFDistanceSensor, HallSensor,
    Button, Led, GPIOPin
)
from _config import load_config


__config: dict = load_config()
__components: dict = __config.get('components')
__dimensions: dict = __config.get('dimensions')


DIMENSIONS: dict = __dimensions

# BUTTONS
try:
    buttons: dict = __components.get('buttons')

    # Ingredient Buttons
    BUTTON_INGR1 = Button(buttons.get('ingredient1'))
    BUTTON_INGR2 = Button(buttons.get('ingredient2'))
    BUTTON_INGR3 = Button(buttons.get('ingredient3'))

    # Menu Buttons
    BUTTON_START = Button(buttons.get('start'))
    BUTTON_RESET = Button(buttons.get('reset'))

    BUTTON_INGREDIENTS: list = [BUTTON_INGR1, BUTTON_INGR2, BUTTON_INGR3]

except AttributeError:
    print("No buttons found.")


# LEDS
try:
    leds: dict = __components.get('leds')

    LED_ORANGE = Led(leds.get('orange'))
    LED_GREEN = Led(leds.get('green'))

    LEDS = [LED_ORANGE, LED_GREEN]

except AttributeError:
    print("No LEDs found.")

# POSITION SENSORS
try:
    # y-axis, hall sensor
    POS_Y = HallSensor(__components.get('position').get('pos_y'))
    # x-axis, tof sensor
    POS_X = ToFDistanceSensor(__components.get('position').get('pos_x'))

except AttributeError:
    print("No position sensors found.")


# MOTORS
# Movement
try:    
    # y-axis, stepper motor
    MOVE_Y = StepperMotor(__components.get('motors').get('move_y'))
    # x-axis, servo motor
    MOVE_X = ContinuousServoMotor(__components.get('motors').get('move_x'))

except AttributeError:
    print("No motors for movement found.")


# Helpers
try:
    # folding servo motor
    MOVE_FOLD = StandardServoMotor(__components.get('motors').get('fold'))
    # forming servo motor
    MOVE_TEMPLATE = StandardServoMotor(__components.get('motors').get('template'))

except AttributeError:
    print("No Helper motors (fold and template) found.")


# Ingredients
try:
    # ingredient servo motor
    MOVE_INGR1 = StandardServoMotor(__components.get('motors').get('ingredient1'))
    MOVE_INGR2 = StandardServoMotor(__components.get('motors').get('ingredient2'))
    MOVE_INGR3 = StandardServoMotor(__components.get('motors').get('ingredient3'))

    MOVE_INGREDIENTS: list = [MOVE_INGR1, MOVE_INGR2, MOVE_INGR3]

except AttributeError:
    print("No Ingredients motors found.")


# DEBUG PIN
DEPUG_PIN = GPIOPin(gpio=26)
