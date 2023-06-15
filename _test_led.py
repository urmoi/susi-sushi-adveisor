from Components import Led

from _config import load_components_config, load_dimensions_config
from visualization import reset_terminal

components = load_components_config()
leds = components.get('leds')

LED_ORANGE = Led(leds.get('orange'))
LED_GREEN = Led(leds.get('green'))

LEDS = [LED_ORANGE, LED_GREEN]

while True:
    reset_terminal()
    key = input('Press Enter to toggle LED or B to blink: ')
    for led in LEDS:
        if key.lower() == 'b':
            led.blink()
        else:
            led.toggle()
        print(led)