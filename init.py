from Components import Button, HallSensor, StepperMotor, ContinuousServoMotor, StandardServoMotor, ToFDistanceSensor, LEDrgb
from _config import load_config


__config: dict = load_config()
__components: dict = __config.get('components')
__dimensions: dict = __config.get('dimensions')


DIMENSIONS: dict = __dimensions

# BUTTONS
try:
    buttons = __components.get('buttons')

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


# RBG LED
try:
    leds = __components.get('leds')

    RGBLED = LEDrgb(leds.get('rgbinfo'))

except AttributeError:
    print("No RGB LED found.")


# HALL CONTACTS
try:
    contacts: dict = __components.get('hall_contacts')

    # Element Contact
    roller_contact = HallSensor(contacts.get('roller'))
    ingredients_contact  = HallSensor(contacts.get('ingredients'))
    template_contact = HallSensor(contacts.get('template'))
    table_contact = HallSensor(contacts.get('table'))

    # Door Contact
    door_contact = HallSensor(contacts.get('door'))

except AttributeError:
    print("No hall contacs found.")


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