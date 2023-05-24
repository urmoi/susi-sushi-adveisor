import time

from Components import Button, LEDrgb
from _config import load_components_config
import visualization as vis



def main():
    buttons = load_components_config().get('buttons')
    leds = load_components_config().get('leds')

    # RGB LED
    RGBLED = LEDrgb(leds.get('rgbinfo'))

    # Ingredient Buttons
    BUTTON_INGR1 = Button(buttons.get('ingredient1'))
    BUTTON_INGR1.set_callback(callback=[lambda: print(" > INGR1 (blue)", end="\r"), lambda: RGBLED.color(0x0000FF)])

    BUTTON_INGR2 = Button(buttons.get('ingredient2'))
    BUTTON_INGR2.set_callback(callback=[lambda: print(" > INGR2 (yellow)", end="\r"), lambda: RGBLED.color(0xFFFF00)])

    BUTTON_INGR3 = Button(buttons.get('ingredient3'))
    BUTTON_INGR3.set_callback(callback=[lambda: print(" > INGR3 (magenta)", end="\r"), lambda: RGBLED.color(0xFF00FF)])

    # Menu Buttons
    BUTTON_START = Button(buttons.get('start'))
    BUTTON_START.set_callback(callback=[lambda: print(" > START (green)", end="\r"), lambda: RGBLED.color(0x00FF00)])
    BUTTON_RESET = Button(buttons.get('reset'))
    BUTTON_RESET.set_callback(callback=[lambda: print(" > RESET (red)", end="\r"), lambda: RGBLED.color(0xFF0000)])

    vis.print_title(f"Buttons and RGB LED")
    vis.print_subtitle(f"[Ctrl + C to exit]")

    try:
        while True:
            time.sleep(0.25)
        
    except KeyboardInterrupt:
        vis.exit_terminal_menu(prompt=f"Buttons and RGB LED ended.")


if __name__ == "__main__":
    main()