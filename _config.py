import json

import visualization as vis


def load_config() -> dict:
    try:
        with open('./config.json', 'r') as json_file:
            config: dict = json.load(json_file)
    except FileNotFoundError:
        print("No config file (config.json) found.")
        exit(1)

    return config


def save_config(config: dict) -> bool:
    try:
        with open('./config.json', 'w') as json_file:
            json.dump(config, json_file, indent=4)
    except FileNotFoundError:
        print("No config file (config.json) Nothing saved.")
        exit(1)

    return True


def load_components_config() -> dict:
    try:
        components: dict = load_config().get('components')
    except AttributeError:
        print("No components found in config file (config.json).")
        exit(1)

    return components


def save_components_to_config(components: dict) -> bool:
    config: dict = load_config()

    config['components']: dict = components

    save_config(config=config)

    return True


def load_dimensions_config() -> dict:
    try:
        dimensions: dict = load_config().get('dimensions')
    except AttributeError:
        print("No dimensions found in config file (config.json).")
        exit(1)

    return dimensions


def save_dimensions_to_config(dimensions: dict) -> bool:
    config: dict = load_config()

    config['dimensions']: dict = dimensions

    save_config(config=config)

    return True


def show_config(section: str=None) -> bool:
    vis.reset_terminal()
    vis.print_title(f"Show Config{f' - {section.capitalize()}' if section else ''}")
    config: dict = load_config()
    for key, type in config.items():
        if section is None or key == section:
            print(f"\n    > {key.capitalize()}:\n")
            for key1, value in type.items():
                if key == "dimensions":
                    if key1 == "thread":
                        print(f"         {key1.capitalize()} : {value:3} mm")
                        continue
                    print(f"         {key1.capitalize()}:")
                    for key2, dim in value.items():
                        print(f"           -  {key2.capitalize()} : {dim:3 if dim else 'Not set' } mm")
                elif key == "components":
                    print(f"       # {key1.upper()}:")
                    for key2, group in value.items():
                        print(f"           {key2.capitalize()}:")
                        for key3, val in group.items():
                            if key3 == "key":
                                continue
                            print(f"             |- {key3:7} : {val}")
    
    show_config_menu()


def show_pins() -> bool:
    vis.reset_terminal()
    vis.print_title(f"Show Pin Setup (Raspberry Pi Zero)")
    print(f"{20 * ' '}Pins{28 * ' '}Board{6 * ' '}Pins")
    print(f"{64 * ' '}||")

    components = load_components_config()
    used_pins = [(component['pin'], component['name']) for group in components.values() for component in group.values() if 'pin' in component.keys() and component['pin'] is not None]

    for pin in vis.pins:
        sign = f"  "
        number = f"{pin[1]:2}"
        name = f"{pin[0][:10]:10}"
        if pin[2]:
            sign = f" •"
            for used_pin in used_pins:
                if pin[1] == used_pin[0]:
                    sign = f" o"
                    name = f"{used_pin[1][:10]:10}"

        # left side (odd pins)
        if pin[1]%2:
            print(f'  {sign}  {name}  {number}', end=" -- ")
        # right side (even pins)
        else:
            print(f'{number}  {name}  {sign}', end=" ")
        # print raspberry pi board
            if vis.raspberry_pi_ascii_art:
                print(f'{9*" "}{vis.raspberry_pi_ascii_art.pop(0)}', end="")
            print()
    
    show_config_menu()


def show_hat() -> bool:
    vis.reset_terminal()
    vis.print_title(f"Show HAT Setup (Servo HAT)")
    # hat header
    print(f"{43 * ' '}BRO <- Cables")
    print(f"{35 * ' '}Slots{3 * ' '}|||    Colors")
    components = load_components_config()
    used_slots: list[tuple[int, str]] = [(motor['slot'], motor['name']) for motor in components['motors'].values() if 'slot' in motor.keys() and motor['slot'] is not None] 

    for slot in range(16):
        sign = f" •"
        number = f"{slot:2}"
        name = f"{'Not set':20}"
        for used_slot in used_slots:
            if slot == used_slot[0]:
                sign = f" o"
                name = f"{used_slot[1][:20]:20}"
        
        print(f'  {sign}  {number}  {name} ', end="")
        if vis.servo_hat_ascii_art:
            print(f"  {9*' '}{vis.servo_hat_ascii_art.pop(0)}", end="")
        print()
    
    show_config_menu()


def reset_config() -> None:
    confirmed = False
    while True:
        vis.reset_terminal()
        vis.print_title("Reset Config")
        vis.print_subtitle("Reset config file (config.json).")

        options: list[tuple[str, str]] = [
            ("y", f"Yes{', sure!' if confirmed else ''}"),
            ("n", "No")
        ]
        reset = vis.print_options(options=options, prompt=f"Are you sure{' sure' if confirmed else ''} : ")

        if not reset == "y":
            vis.print_subtitle("Nothing happend.")
            exit(0)
        
        if confirmed:
            break

        confirmed = True
    
    result = save_config(__config)
    if not result:
        vis.print_subtitle("Reset config file (config.json) failed.")
        exit(1)

    vis.print_subtitle("Reset config file (config.json) done!.")

    show_config_menu()


def show_config_menu() -> None:
    options: list[tuple[str, str]] = [
        ("b", "Back"),
        ("q", "Quit")
    ]
    option = vis.print_options(options=options)
    if option == 'b':
        main()
    else:
        vis.exit_terminal_menu(prompt="Config Closed")


def main() -> None:
    try: 
        vis.reset_terminal()
        vis.print_title("Sushi Machine - Config")
        options: list[tuple[str, str]] = [
            ("s", "Show Config File"),
            ("d", "Show Dimensions"),
            ("c", "Show Components"),
            (),
            ("p", "Show Pin Setup (Raspberry Pi)"),
            ("h", "Show HAT Setup (Servo HAT)"),
            (),
            ("r", "Reset Config"),
            (),
            ("q", "Quit")
        ]
        option = vis.print_options(options=options)
        if option == 's':
            show_config()
        elif option == 'd':
            show_config(section='dimensions')
        elif option == 'c':
            show_config(section='components')
        elif option == 'p':
            show_pins()
        elif option == 'h':
            show_hat()
        elif option == 'r':
            reset_config()
        else:
            vis.exit_terminal_menu(prompt="Config Closed")
    except KeyboardInterrupt:
        vis.exit_terminal_menu(prompt="Config Closed with KeyboardInterrupt")


# Standarf config for reset
__config:dict = {
    "dimensions": {
        "size": {
            "x": None,
            "y": None
        },
        "offset": {
            "x": None,
            "y": None
        },
        "thread": 3
    },
    "components": {
        "position": {
            "pos_y": {
                "name": "Y Position (Hall)",
                "key": "pos_y",
                "type": "hall",
                "pin": 11,
                "GPIO": 17
            },
            "pos_x": {
                "name": "X Position (ToF)",
                "key": "pos_x",
                "type": "tof"
            }
        },
        "motors": {
            "move_y": {
                "name": "Stepper Y Movement",
                "key": "move_y",
                "type": "stepper",
                "up": "backward",
                "down": "forward",
                "steps": 200,
                "number": 1
            },
            "move_x": {
                "name": "Servo X Movement",
                "key": "move_x",
                "type": "servo_continous",
                "slot": 0,
                "right": -1,
                "left": 1,
                "speed": 1.0
            },
            "ingredient1": {
                "name": "Servo Ingredient 1",
                "key": "ingredient1",
                "type": "servo",
                "slot": 1,
                "neutral": 0,
                "active": 180
            },
            "ingredient2": {
                "name": "Servo Ingredient 2",
                "key": "ingredient2",
                "type": "servo",
                "slot": 2,
                "neutral": 0,
                "active": 180
            },
            "ingredient3": {
                "name": "Servo Ingredient 3",
                "key": "ingredient3",
                "type": "servo",
                "slot": 3,
                "neutral": 0,
                "active": 180
            },
            "fold": {
                "name": "Servo Folding Frame",
                "key": "fold",
                "type": "servo",
                "slot": 4,
                "neutral": 0,
                "active": 90
            },
            "template": {
                "name": "Servo Rice Template",
                "key": "template",
                "type": "servo",
                "slot": 5,
                "neutral": 0,
                "active": 90
            }
        },
        "buttons": {
            "ingredient1": {
                "name": "Button Ingredient 1",
                "key": "ingredient1",
                "type": "switch",
                "slot": 'B'
            },
            "ingredient2": {
                "name": "Button Ingredient  2",
                "key": "ingredient2",
                "type": "switch",
                "slot": 'C'
            },
            "ingredient3": {
                "name": "Button Ingredient 3",
                "key": "ingredient3",
                "type": "switch",
                "slot": 'D'
            },
            "start": {
                "name": "Button Start",
                "key": "start",
                "type": "button",
                "slot": 'A'
            },
            "reset": {
                "name": "Button reset",
                "key": "reset",
                "type": "button",
                "slot": 'E'
            }
        },
        "leds": {
            "rgbinfo": {
                "name": "LED Info",
                "key": "rgbinfo",
                "type": "rgbled",
                "blink_speed": 1.0,
            },
        },
        "hall_contacts": {
            "roller": {
                "name": "Hall Contact Rice Roller",
                "key": "roller",
                "type": "hall",
                "pin": None,
                "GPIO": None
            },
            "ingredients": {
                "name": "Hall Contact Ingredient Box",
                "key": "ingredients",
                "type": "hall",
                "pin": None,
                "GPIO": None
            },
            "template": {
                "name": "Hall Contact Rice Template",
                "key": "template",
                "type": "hall",
                "pin": None,
                "GPIO": None
            },
            "table": {
                "name": "Hall Contact Table",
                "key": "table",
                "type": "hall",
                "pin": None,
                "GPIO": None
            },
            "door": {
                "name": "Hall Contact Door",
                "key": "door",
                "type": "hall",
                "pin": None,
                "GPIO": None
            }
        }
    }
}


if __name__ == "__main__":
    main()