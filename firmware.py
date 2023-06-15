# # : Comment                       prints comment (or  seperated with ; after command, which not prints)

# A
# B : Button Ingredients    #       [0=off, 1=on] Ingredient buttons
# C : Calibrate             #       [0=always, 1=once], calibrate Y axis with offset
# D
# E : End                           marks end of recipe, resets 
# F : Fold                  #       [0=neutral, 1=active]
# G
# H
# I : Ingredients           #       [0=neutral, 1=active (only selected)]
# J
# K
# L : LED                   #   #   [light -> 0=off, 1=orange, 2=green] [blink -> 0=noBlink, #=Blink]
# M : Move                  #   #   [X] [Y], position in mm, [0 0] is top left, NaN=NoMovement)
# N
# O
# P
# Q
# R : Reset Button          #       [mode -> 0=None, 1=reset, -1=error]
# S : Start Button          #       [mode -> 0=None, 1=start, 2=wait for ingredients, -1=error]
# T : Template              #       [0=neutral, 1=active]
# U
# V
# W : Wait                  #       [time in miliseconds]
# X
# Y
# Z


import threading
import time


from init import (
    DIMENSIONS,
    MOVE_X, MOVE_Y, POS_X, POS_Y, 
    MOVE_FOLD, MOVE_INGREDIENTS, MOVE_TEMPLATE,
    BUTTON_INGREDIENTS, BUTTON_START, BUTTON_RESET,
    LEDS, LED_ORANGE, LED_GREEN
)


YPOSITION: int = None # y position in mm

RESTART: bool = False # restart flag


def load_instruction(filename: str) -> str:
    extension = ".scode"
    try:
        with open(f"./{filename}{extension}") as file:
            instruction: str = file.read()
    except FileNotFoundError:
        print(f"No instructions file found: {filename}{extension}.")
        exit(1)
    return instruction


def perform_instruction(filename: str='instructions', verbose: int=1) -> bool:
    global RESTART

    # cylce loop
    while True:
        if not verbose: print(f"running {filename}...")
        if verbose: print(f"## START CYCLE {(len(filename)-7)*'.'} ##")
        if verbose: print(f"## FILE {filename.upper()} ##")

        # reset restart flag
        RESTART = False

        # load instruction
        instruction: str = load_instruction(filename=filename)

        # read instruction line by line
        for line in instruction.splitlines():

            # check for restart, break out of for loop
            if RESTART:
                break

            # check for comment
            if verbose == 2 and line[0] == '#':
                print(f" {line}")
                print(" > Comment")
                continue
                
            if verbose == 2: print()

            if verbose: print(f"   {line.split(';')[0].strip()}")
            
            # remove comments, split by space, isolate parameters, convert to int (or None)
            command = parameter(line.split(';')[0].strip().split(' '))

            try:
                # check command
                if command[0] == 'B':
                    command_button(active=command[1], verbose=verbose)
                elif command[0] == 'C':
                    command_calibrate(mode=command[1], verbose=verbose)
                elif command[0] == 'E':
                    command_end(verbose=verbose)
                elif command[0] == 'F':
                    command_fold(active=command[1], verbose=verbose)
                elif command[0] == 'I':
                    command_ingredients(active=command[1], verbose=verbose)
                elif command[0] == 'L':
                    command_led(color=command[1], blink=command[2], verbose=verbose)
                elif command[0] == 'M':
                    command_move(x=command[1], y=command[2], verbose=verbose)
                elif command[0] == 'R':
                    command_reset(mode=command[1], verbose=verbose)
                elif command[0] == 'S':
                    command_start(mode=command[1], verbose=verbose)
                elif command[0] == 'T':
                    command_template(active=command[1], verbose=verbose)
                elif command[0] == 'W':
                    command_wait(invervall=command[1], verbose=verbose)
                else:
                    if verbose == 2: print(" > Unknown command")

            except IndexError:
                if verbose == 2: print(" > Invalid command parameters")
                pass

        print(f"END CYCLE")
        
        # check for restart, restart cycle loop
        if RESTART:
            reset()
            continue
        


def command_button(active: int, verbose: int=0) -> None:
    # active: 0=off, 1=on
    if verbose == 2: print(f" > Ingredient Buttons: {'on for selection' if active else 'off and all deselected'}")
    for button in BUTTON_INGREDIENTS:
        if bool(active):  
            # toggle ingredient on button press, blink depending on status
            button.set_callback(callback=lambda: led_switch(state=button.status())) 
        else:
            # reset ingredient button status
            button.deselect()
            button.set_callback(callback=None)
    return


def command_calibrate(mode: int=0, verbose: int=0) -> None:
    # mode: 0=always, 1=once
    if mode == 0 or YPOSITION is None:
        if verbose == 2: print(" > Calibrating...")
        calibrate()
        if verbose == 2: print(" > Calibration finished")
    else:
        if verbose == 2: print(" > Calibrating skipped")
    return


def command_end(verbose: int=0) -> None:
    if verbose == 2: print(" > Ending...")
    command_fold(active=0)
    command_move(x=0, y=0)
    command_template(active=0)
    command_ingredients(active=0)
    command_button(active=0)
    led_ready()
    return


def command_fold(active: int, verbose: int=0) -> None:
    # active: 0=neutral, 1=active
    if verbose == 2: print(f" > Fold moved: {'active' if active else 'neutral'}")
    position: str = 'active' if active else 'neutral'
    MOVE_FOLD.set_position(position=position)
    return


def command_ingredients(active: int, verbose: int=0) -> None:
    # active: 0=neutral, 1=active (only selected)
    if verbose == 2: print(f" > Ingredient Movement: ", end='')
    if verbose == 2 and  not active: print("all to neutral")
    for ingredient in MOVE_INGREDIENTS:
        if bool(active):
            selected: bool = BUTTON_INGREDIENTS[MOVE_INGREDIENTS.index(ingredient)].status()
            if verbose == 2: print(f"[{ingredient.name}: ", end='')
            if selected:
                if verbose == 2: print(" on] ", end='')
                ingredient.set_position(position='active')
            else:
                if verbose == 2: print("off] ", end='')
                ingredient.set_position(position='neutral')
            if verbose == 2: print()
        else:
            ingredient.set_position(position='neutral')
    return


def command_led(color: int, blink: int, verbose: int=0) -> None:
    # color: 0=off, 1=orange, 2=green
    # blink: 0=off, #=n times
    if verbose == 2: print(f" > LED: {'orange' if color == 1 else 'green' if color == 2 else 'off'} {'(blinking ' + str(blink) + ' times)' if blink else ''}")

    if color == 0:
        led_off()
        return
    if color == 1:
        led_on = LED_ORANGE
        led_off = LED_GREEN
    elif color == 2:
        led_on = LED_GREEN
        led_off = LED_ORANGE
    else:
        if verbose == 2: print(" > Unknown LED color")
        return

    led_off.off()
    if blink == 0:
        led_on.on()
    else:
        led_on.blink(on_time=0.5, off_time=0.5, n=blink)
    return


def command_move(x: int, y: int, verbose: int=0) -> None:
    # Move to position, None = no movement

    # Cap the position to the size of the machine
    x = cap_position(pos=x, min_pos=0, max_pos=DIMENSIONS['size']['x'])
    y = cap_position(pos=y, min_pos=-DIMENSIONS['size']['y'], max_pos=0)

    if verbose == 2: print(f" > Moving to position: [X {x if x is not None else '---'} | Y {y if y is not None else '---'}] mm", end="\r")

    # Move both axes
    if x is not None and y is not None:
        # Create threads to move both axis at the same time
        move_x_thread = threading.Thread(target=move_x, kwargs={'x': x})
        ret0 = move_y_thread = threading.Thread(target=move_y, kwargs={'y': y})

        # Start the threads
        move_x_thread.start()
        ret1 = move_y_thread.start()

        # Wait for both threads to complete
        move_x_thread.join()
        ret2 = move_y_thread.join()

        print(YPOSITION, y)
    
    # Move only x axis
    elif x is not None:
        move_x(x=x)
        return

    # Move only y axis
    elif y is not None:
        move_y(y=y)
        return

    # No movement
    else:
        if verbose == 2: print(f"{50 * ' '}", end="\r")
        if verbose == 2: print(f" > No movement")
        return
    
    if verbose == 2: print(f"{50 * ' '}", end="\r")
    if verbose == 2: print(f" > Moved to position: [X {x if x else '---'} | [Y {y if y else '---'}] mm")
    return

    
def command_reset(mode: int, verbose: int=0) -> None:
    # mode: 0=None, 1=reset, -1=error
    if verbose == 2: print(f" > Reset Button: {'off' if mode == 0 else 'reset on press' if mode == 1 else 'reset template on press' if mode == 2 else 'error light on press'}")
    if mode == 0:
        # disable button
        BUTTON_RESET.set_callback(None)
    elif mode == 1:
        # reset and led reset color
        BUTTON_RESET.set_callback([lambda: restart(), lambda: led_reset()])
    elif mode == -1:
        # error when pressed (blink)
        BUTTON_START.set_callback(led_error)
    return


def command_start(mode: int, verbose: int=0) -> None:
    # mode: 0=None, 1=start, -1=error
    if verbose == 2: print(f" > Start Button: {'off' if mode == 0 else 'wait for press to continue' if mode == 1 else 'error light on press'}")
    if mode == 0:
        # disable button
        BUTTON_START.set_callback(None)
    elif mode == 1:
        # block until ingredient is selected, then continue
        while True:
            # no ingredient selected, blink red
            if not any([ingredient.status() for ingredient in BUTTON_INGREDIENTS]):
                # show error light
                BUTTON_START.set_callback(led_error)
                # reset start button selection
                BUTTON_START.deselect()
                continue
            BUTTON_START.set_callback(None)
            # ingredient selected
            if BUTTON_START.status():
                # start pressed, continue
                break
        BUTTON_START.set_callback(None)
    elif mode == -1:
        # error when pressed (blink red)
        BUTTON_START.set_callback(callback=led_error)
    return


def command_template(active: int, verbose: int=0) -> None:
    # active: 0=neutral, 1=active
    if verbose == 2: print(f" > Template moved: {'active' if active else 'neutral'}")
    position: str = 'active' if active else 'neutral'
    MOVE_TEMPLATE.set_position(position=position)
    return


def command_wait(invervall: int, verbose: int=0) -> None:
    # invervall: #=ms
    if verbose == 2: print(f" > Waiting for {invervall} ms")
    time.sleep(invervall / 1000)
    return


def move_x(x: int, distance: int=None) -> bool:
    # No info given
    if x is None and distance is None:
        return False
    
    # Get current position if none given
    if x is None:
        x = POS_X.read_distance(DIMENSIONS['offset']['x'])
    
    # Add distance
    if distance is not None:
        x += distance

    offset = DIMENSIONS['offset']['x']

    # Move until position is reached
    while True:
        pos = POS_X.read_distance(offset=offset)
        if pos < x:
            MOVE_X.move_right()
        elif pos > x:
            MOVE_X.move_left()
        else:
            MOVE_X.stop()
            break
        time.sleep(0.2)
    
    return True


def move_y(y: int, distance: int=None) -> bool:
    global YPOSITION

    # No info given
    if y is None and distance is None:
        return False
    
    # Can not calculate distance without position
    if y is not None and YPOSITION is None:
        return False
    
    delta = 0

    # Move to position
    if y is not None and YPOSITION is not None:
        delta = y - YPOSITION

    # Move by distance
    if distance is not None:
        delta += distance

    # Calculate steps
    distance_per_step = DIMENSIONS['thread'] / MOVE_Y.steps
    steps = int(abs(delta) / distance_per_step)

    if delta > 0:
        MOVE_Y.move_up(steps=steps)
    elif delta < 0:
        MOVE_Y.move_down(steps=steps)
    MOVE_Y.stop()

    # Update YPOSITION
    if YPOSITION is not None:
        YPOSITION += delta
    return True


def calibrate() -> bool:
    global YPOSITION
    command_fold(active=False)
    if POS_Y.sense_magnet():
        while POS_Y.sense_magnet():
            MOVE_Y.move_up()
        move_y(y=None, distance=5)
    while not POS_Y.sense_magnet():
        MOVE_Y.move_down()
    YPOSITION = -DIMENSIONS['size']['y']-DIMENSIONS['offset']['y']
    return True

def reset() -> bool:
    print("## RESETTING...", end="\r")
    MOVE_FOLD.move_neutral()
    move_y(y=-DIMENSIONS['size']['y'])
    move_x(x=0)
    move_y(y=0)
    MOVE_TEMPLATE.move_neutral()
    command_ingredients(active=0)
    command_button(active=0)
    return True


def restart() -> bool:
    global RESTART
    RESTART = True
    print("## RESTARTING...", end="\r")




def cap_position(pos: int, min_pos: int=None, max_pos: int=None) -> int:
    if pos is None:
        return None
    if min_pos is not None and pos < min_pos:
        return min_pos
    elif max_pos is not None and pos > max_pos:
        return max_pos
    else:
        return pos
 
def led_off() -> bool:
    # light off
    LED_ORANGE.off()
    LED_GREEN.off()
    return True

def led_error(blink: int=3) -> bool:
    # light orange
    LED_ORANGE.blink(on_time=0.25, off_time=0.25, n=blink)
    LED_ORANGE.off()
    return True

def led_busy(blink: int=1) -> bool:
    # light orange
    LED_ORANGE.on()
    return True

def led_ready(blink: int=3) -> bool:
    # blink 3times green, then stay on
    LED_GREEN.blink(n=blink)
    LED_GREEN.on()
    return True

def led_reset(blink: int=3) -> bool:
    # blink 3times orange, then stay on
    LED_ORANGE.blink(n=blink)
    LED_ORANGE.on()
    return True

def led_switch(state: bool, blink: int=1) -> bool:
    if state:
        # blink green
        LED_GREEN.blink(on_time=0.25, off_time=0.25, n=blink)
        LED_GREEN.on()
    else:
        # blink orange
        LED_ORANGE.blink(on_time=0.25, off_time=0.25, n=blink)
    return True


def parameter(command: list[str]) -> list[str]:
    # convert parameters to int (or None)
    for i in range(1, len(command)):
        command[i] = command[i].strip()
        try:
            command[i] = int(command[i])
        except ValueError:
            command[i] = None
    return command


def main() -> None:
    perform_instruction()


if __name__ == "__main__":
    main()