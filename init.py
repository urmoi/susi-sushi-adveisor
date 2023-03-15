# Global variables

# Dimensions
dim = {                                     # dimensions of movement in mm, measured with tof sensor
    "ud": {"min": 10, "max": 130},          # ud = up-down / vertical min and max reachable position
    "lr": {"min": 50, "max": 250}           # lr = left-right / horizontal min and max reachable position
}

# Display
display = None                              # Display object

# Contacts
roller_contact = None                       # True if roller is in machine
fillings_contact = None                     # True if fillings are in machine
template_contact = None                     # True if template is in machine
table_contact = None                        # True if table is in machine
door_contact = None                         # True if door is closed

# Sensors
ud_tof = 0.0                                # vertical ToF sensor
lr_tof = 0.0                                # horizontal ToF sensor
tof = (ud_tof, lr_tof)                      # tuple of ToF sensor data

f1_button = None                            # filling 1 button
f2_button = None                            # filling 2 button
f3_button = None                            # filling 3 button

start_button = None                         # start button

# Motors
v_step = None                               # vertical stepper motor
h_step= None                                # horizontal stepper motor

f1_servo = None                             # filling 1 servo motor
f2_servo = None                             # filling 2 servo motor
f3_servo = None                             # filling 3 servo motor

temp_servo = None                           # template servo motor

# Positions
table = (0.0, 0.0)                          # tuple percentage % position of the table

# States
template = False                            # True if template is down
fillings = (False, False, False)            # True if filling selected


def tof2pos(tof:tuple) -> tuple:
    """
    Convert ToF sensor value to percentage position [ud, lr].

        min          max
    max 0.0 -- lr -- 1.0
         |
        ud
         |
    min 1.0

    """
    return (
        (tof[0]-dim["ud"]["max"])/(dim["ud"]["min"]-dim["ud"]["max"]),  # ud = up-down / vertical
        (tof[1]-dim["lr"]["min"])/(dim["lr"]["max"]-dim["lr"]["min"])   # lr = left-right / horizontal
    )