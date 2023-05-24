import getch

import visualization as vis
from __Components import StandardServoMotor
from _config import load_components_config, save_components_to_config


def main():
    components: dict = load_components_config()

    changed: object = None

    # ingredient servo motor
    ingr1 = StandardServoMotor(components.get('motors').get('ingredient1'))
    ingr2 = StandardServoMotor(components.get('motors').get('ingredient2'))
    ingr3 = StandardServoMotor(components.get('motors').get('ingredient3'))

     # folding servo motor
    fold = StandardServoMotor(components.get('motors').get('fold'))
    # forming servo motor
    template = StandardServoMotor(components.get('motors').get('template'))

    motors: list[object] = [ingr1, ingr2, ingr3, fold, template]

    position: str = 'neutral'

    for motor in motors:
        motor.set_position(position)

    try: 
        while True:
            if changed:
                components.get('motors')[changed.key] = changed
                save_components_to_config(components)
                changed = None

            vis.print_title("Test Motors")
            vis.print_subtitle("Test all motors for correct positioning.")
            vis.print_centered("> Adjust Horn Position on the motors if necessary.")
            vis.print_centered("> Switch angles to change moving direction.       ")
            print()
            vis.print_centered("[Switch Key] : Switch Angle | Direction          ")
            vis.print_centered("     [Space] : Change position : Neutral | Active")
            vis.print_subtitle(f"Position: {position.upper():>7}")
            vis.print_centered(f"{8*' '}Motor{8*' '}: Neutral |  Active | Switch Key")
            vis.print_centered(f"{21*'-'}:{9*'-'}|{9*'-'}|{12*'-'}")

            for index, motor in enumerate(motors):
                vis.print_centered(f"{motor.name[:20]:20} :  {'>' if position == 'neutral' else ' '} {motor.neutral:3}° |  {'>' if position == 'active' else ' '} {motor.active:3}° |     {index+1}     ")

            print("\n\n")

            try:
                key = getch.getch().lower()
            except OverflowError: 
                vis.exit_terminal_menu(prompt=f"Motor Testing ended.")

            if key == ' ':
                for motor in motors:
                    position = 'active' if position == 'neutral' else 'neutral'
                    motor.set_position(position)
            elif key.isdigit():
                index = int(key) - 1
                if index < len(motors):
                    motor = motors[index]
                    motor.active, motor.neutral = motor.neutral, motor.active
                    motor.set_position(position)

            # print(components.get('motors'))

    except KeyboardInterrupt:
        vis.exit_terminal_menu(prompt=f"Motor Testing ended.")



if __name__ == '__main__':
    main()