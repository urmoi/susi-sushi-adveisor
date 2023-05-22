import sys

import controller
import init

# import RPi.GPIO as GPIO



def main() -> None:

    # check if debug mode is enabled
    # exits when pin 37 | GPIO26 is connected to ground
    check_debug_mode()

    # check if calibration was done
    # exits when calibration is needed
    check_calibration()

    # default instruction file
    filename: str = 'instructions'

    # default verbosity, show nothing
    verbose: int = 0

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg[0] == '-':
                if arg == '-v':
                    # show only commands from instruction file
                    verbose = 1
                elif arg == '-V':
                    # show commands and explanations
                    verbose = 2
            else:
                filename = arg
            

    try:
        controller.perform_instruction(filename=filename, verbose=verbose)
    except (OSError, KeyboardInterrupt):
        init.MOVE_X.stop()
        init.MOVE_Y.stop()
        print(end="\r")
        print("  ", end="\r")
        print(f"\n")
        print(f"{15*' '}Susi stopped!")
        print(f"{20*' '}Bye!\n\n")
        exit(0)


def check_debug_mode() -> bool:
    # True is default, False is debug mode (connected to ground)
    if init.DEPUG_PIN.sense():
        return False
    
    print("\n\n")
    print(" Pin 37 | GPIO26 is connected to ground. Going in Debug Mode.")
    print(" To start in Auto Mode, disconnect Pin 37 | GPIO26 from ground.")
    print(" (Both Pins on the left Bottom, when the USBs are on the left)\n\n")
    print("#########################  DEBUG MODE  #########################\n")
    print("                     >  maybe run following scripts:\n")
    print("                        main.py <filename> [-v | -V]\n")
    print("                        _test_hall.py")
    print("                        _test_tof.py")
    print("                        _test_buttons.py")
    print("                        _test_motors.py")
    print("                        _calibrate_axes.py\n\n")
    print("                     >  exiting ...")
    print("\n\n")

    exit(0)


def check_calibration() -> bool:
    for dimension in init.DIMENSIONS.values():
        for axis in dimension.values():
            if axis is None:
                print("\n\n")
                print(" Axes Calibration is needed. Going in Debug Mode.\n\n")
                print("#########################  DEBUG MODE  #########################\n")
                print("                     >  maybe run following scripts:\n")
                print("                        _calibrate_axes.py\n\n")
                print("                     >  exiting ...")
                print("\n\n")

                exit(0)
    return True

if __name__ == "__main__":
    main()