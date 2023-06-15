import time

from Components import Button
from _config import load_components_config, load_dimensions_config
from visualization import reset_terminal

components = load_components_config()
buttons = components.get('buttons')

# Ingredient Buttons
BUTTON_INGR1 = Button(buttons.get('ingredient1'))
BUTTON_INGR2 = Button(buttons.get('ingredient2'))
BUTTON_INGR3 = Button(buttons.get('ingredient3'))

# Menu Buttons
BUTTON_START = Button(buttons.get('start'))
BUTTON_RESET = Button(buttons.get('reset'))

BUTTON_INGREDIENTS: list = [BUTTON_INGR1, BUTTON_INGR2, BUTTON_INGR3]

BUTTONS = [BUTTON_INGR1, BUTTON_INGR2, BUTTON_INGR3, BUTTON_START, BUTTON_RESET]

while True:
    reset_terminal()
    for button in BUTTONS:
        print(f"{button.name:20} : {button.status()}")

    BUTTON_START.deselect()
    BUTTON_RESET.deselect()
    time.sleep(0.5)
