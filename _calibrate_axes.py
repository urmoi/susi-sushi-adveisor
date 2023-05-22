import getch
import time

from Components import ContinuousServoMotor, ToFDistanceSensor, StepperMotor, HallSensor

import visualization as vis
from _config import load_config, save_config, save_dimensions_to_config


def axes_list(saved):
    vis.print_title("Axes Calibration - Select Axis")
    vis.print_ascii_art(vis.sushi_machine_ascii_art, 4)
    if saved == True:
        vis.print_subtitle(f"[Calibation finished, Values saved]")
    elif saved == False:
        vis.print_subtitle(f"[Calibation aborted, Nothing saved]")
    options: list[tuple[str, str]] = [
        ("x", f"X-Axis (Servo   Movement + ToF  Sensor)"),
        ("y", f"Y-Axis (Stepper Movement + Hall Sensor)"),
        (),
        ("q", "Quit")
    ]
    option = vis.print_options(options=options)

    if option == 'q':
        stop_calibration()
    else:
        return option
    

def calibrate_axis(components, dimensions, axis):
    step = 0
    ask = None

    motor = None
    sensor = None
    steps = None

    if axis == 'x':
        motor = ContinuousServoMotor(components.get('motors').get('move_x'))
        sensor = ToFDistanceSensor(components.get('position').get('pos_x'))
        steps = [
            (0, "Overview", None),
            (1, "Move to  left frame \u2190", move_x_left),
            (2, "Move to right frame \u2192", move_x_right),
            (3, "Test by moving \u2190 \u2192", test_x),
            (4, "Save to config", None)
        ]
    elif axis == 'y':
        motor = StepperMotor(components.get('motors').get('move_y'), 0)
        sensor = HallSensor(components.get('position').get('pos_y'))
        steps = [
            (0, "Overview", None),
            (1, "Move down \u2191", move_y_down),
            (2, "Move   up \u2193", move_y_up),
            (3, "Test by moving \u2191 \u2193", test_y),
            (4, "Save to config", None)
        ]
    try: 
        while True:
            vis.print_title(f"Calibrate {axis.upper()}-Axis")
            vis.print_subtitle(f"Offset: {dimensions['offset'][axis]} mm | Size: {dimensions['size'][axis]} mm")

            for step_number, description, _ in steps:
                print(f"   {'>' if step_number == step else ' '} Step {step_number} : {description}")
        

            if step == len(steps)-1:
                break

            if steps[step][2] and not ask:
                if step < len(steps):
                    print()
                    print()
                    function_to_call = steps[step][2]
                    dimensions = function_to_call(motor, sensor, dimensions)
                    ask = True

                continue

            options: list[tuple[str, str]] = [
                ("y", "Yes, continue to next step"),
                ("n", "No, repeat step"),
            ]
            option = vis.print_options(options=options, prompt=f"Continue to Step {step+1} : ")

            if option == 'n':
                if step == 0:
                    break
                else:
                    ask = False
                    continue

            step += 1
            ask = False

        if step == len(steps)-1:
            if save_dimensions(dimensions):
                return True
        return False
    
    except KeyboardInterrupt:
        stop_calibration(motor)


def move_x_left(servo, tof, dimensions):
    return move_x(servo, tof, dimensions, 'left')

def move_x_right(servo, tof, dimensions):
    return move_x(servo, tof, dimensions, 'right') 
    
def move_x(servo, tof, dimensions, direction):
    servo.stop()
    vis.print_subtitle(f"[Space] : Accept Position and continue")
    vis.print_centered(f" \u2190[Q]   [E]\u2192  : move 1 mm on press")
    vis.print_centered(f"\u2190\u2190[A]   [D]\u2192\u2192 : move|stop on press")
    print()

    while True:

        vis.print_context_update(f"Current Position (raw reading): {tof.read_distance():3} mm")

        try:
            key = getch.getch().lower()
        except OverflowError:
            stop_calibration(servo)

        if key == ' ':
            servo.stop()
            break
        elif key == 'q' or key == 'e':
            goal = tof.read_distance()
            if key == 'q':
                goal -= 1
            elif key == 'e':
                goal += 1
            while True:
                pos = tof.read_distance()
                vis.print_context_update(f"Current Position (raw reading): {pos:3} mm")
                if pos < goal:
                    servo.move_right()
                elif pos > goal:
                    servo.move_left()
                else:
                    servo.stop()
                    break
                time.sleep(0.2)

        elif key == 'a':
            if servo.get_movement() == 'left':
                servo.stop()
            else:
                servo.move_left()
        elif key == 'd':
            if servo.get_movement() == 'right':
                servo.stop()
            else:
                servo.move_right()

    reading = tof.read_distance()
    if direction == 'right':
        dimensions['offset']['x'] = reading
    elif direction == 'left':
        dimensions['size']['x'] = reading - dimensions['offset']['x']
    return dimensions


def test_x(servo, tof, dimensions):
    left_tested = False
    right_tested = False
    servo.stop()

    print(f" Move left \u2190, then right \u2192 to test x-dimensions")

    while True:
        print(f"   [Enter] : ", end="")
        if not left_tested:
            print(f"Start Test (move right \u2190)  ", end="\r")
        elif not right_tested:
            print(f"Continue Test (move left \u2192)", end="\r")
        else:
            print(f"End Test and continue        ", end="\r")

        try:
            key = getch.getch().lower()
        except OverflowError:
            stop_calibration(servo)

        if key == '\n':
            goal_position = None
            if not left_tested:
                goal_position = 0 + dimensions['offset']['x']
                left_tested = True
            elif not right_tested:
                goal_position = dimensions['size']['x'] + dimensions['offset']['x']
                right_tested = True
            else:
                break

            while True:
                position = tof.read_distance()
                if position < goal_position:
                    servo.move_right()
                elif position > goal_position:
                    servo.move_left()
                else:
                    break
            servo.stop()

    servo.stop()
    return dimensions


def move_y_down(stepper, hall, dimensions):
    return move_y(stepper, hall, dimensions, 'down')

def move_y_up(stepper, hall, dimensions):
    return move_y(stepper, hall, dimensions, 'up')

def move_y(stepper, hall, dimensions, direction):
    stepper.release()
    if direction == 'down':
        vis.print_subtitle(f"[Ctrl-C] : Abort calibration in case hall sensor is not working")
        vis.print_context_update(f"[Space] : Start calibration to find magnet sensed by hall sensor")
        

        try:
            while True:
                key = getch.getch().lower()
                if key == ' ':
                    break
        except OverflowError:
            stop_calibration(stepper)

        if hall.sense_magnet():
            while hall.sense_magnet():
               stepper.move_up()
            stepper.move_up(stepps=2*stepper.steps)
        while not hall.sense_magnet():
            vis.print_context_update(f"Moving down \u2193...")
            stepper.move_down()
        vis.print_context_update(f"Magnet sensed, stopping...")

    distance = 0

    distance_per_step = dimensions['thread'] / stepper.steps
    small_step = (1, int(1 / distance_per_step))
    big_step = (10, int(10 / distance_per_step))

    vis.print_subtitle(f"[Space] : Accept Position and continue")
    if direction == 'down':
        vis.print_centered(f"     \u2191  [W]")
        vis.print_centered(f"move in 1 mm steps")
        vis.print_centered(f"     \u2193  [S]")
    elif direction == 'up':
        vis.print_centered(f"[Q]  \u2191  [W]")
        vis.print_centered(f"move in 10 or 1 mm steps")
        vis.print_centered(f"[A]  \u2193  [S]")
    print()

    while True:
        vis.print_context_update(f"waiting...")

        try:
            key = getch.getch().lower()
        except OverflowError:
            stop_calibration(stepper)

        if key == ' ':
            break
        elif key == 'q' and direction == 'up':
            vis.print_context_update(f"moving up \u2191...")
            stepper.move_up(steps=big_step[1])
            distance += big_step[0]
        elif key == 'w':
            vis.print_context_update(f"moving up \u2191...")
            stepper.move_up(steps=small_step[1])
            distance += small_step[0]
        elif key == 'a' and direction == 'up':
            vis.print_context_update(f"moving down \u2193...")
            stepper.move_down(steps=big_step[1])
            distance -= big_step[0]
        elif key == 's':
            vis.print_context_update(f"moving up \u2193...")
            stepper.move_down(steps=small_step[1])
            distance -= small_step[0]

    stepper.release()
    if direction == 'down':
        dimensions['offset']['y'] = distance
    elif direction == 'up':
        dimensions['size']['y'] = distance
    return dimensions
    

def test_y(stepper, hall, dimensions):
    down_tested = False
    up_tested = False

    distance_per_step = dimensions['thread'] / stepper.steps
    steps = int(dimensions['size']['y'] / distance_per_step)

    print(f" Move down \u2193, then up \u2191 to test y-dimensions")

    while True:
        print(f"   [Enter] : ", end="")
        if not down_tested:
            print(f"Start Test (move down \u2193) ", end="\r")
        elif not up_tested:
            print(f"Continue Test (move up \u2191)", end="\r")
        else:
            print(f"End Test and continue    ", end="\r")
        
        try:
            key = getch.getch().lower()
        except OverflowError:
            stop_calibration(stepper)

        if key == '\n':
            if not down_tested:
                while not hall.sense_magnet():
                    stepper.move_down()
                stepper.move_down(steps=steps)
                down_tested = True
            elif not up_tested:
                stepper.move_up(steps=steps)
                up_tested = True
            else:
                break
    stepper.release()
    return True


def main():
    settings = load_config()
    components = settings.get("components")
    dimensions = settings.get("dimensions")

    axis = None
    saved = None

    try:
        while True:
            if not axis:
               axis = axes_list(saved)
               saved = None
            else:
                saved = calibrate_axis(components, dimensions, axis)
                axis = None

    except KeyboardInterrupt:
        stop_calibration()

def save_dimensions(dimensions):
    options: list[tuple[str, str]] = [
        ("y", "Yes"),
        ("n", "No")
    ]
    option = vis.print_options(options=options, prompt="Save dimensions : ")
    if option == 'n':
        return None
    save_dimensions_to_config(dimensions)
    return dimensions


def stop_calibration(motor=None):
    if motor:
        motor.stop()
    vis.exit_terminal_menu(prompt="Calibration Closed")


if __name__ == "__main__":
    main()