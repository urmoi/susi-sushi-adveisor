import sys

pins: list[tuple[str, int, bool]] = [
    ("3v3 Power", 1, False),    ("5v Power", 2, False),
    ("I2C SDA", 3, False),      ("5v Power", 4, False),
    ("I2C SCL", 5, False),      ("Ground", 6, False),
    ("GPIO4", 7, 4),            ("GPIO14", 8, 14),
    ("Ground", 9, False),       ("GPIO15", 10, 15),
    ("GPIO17", 11, 17),         ("GPIO18", 12, 18),
    ("GPIO27", 13, 27),         ("Ground", 14, False),
    ("GPIO22", 15, 22),         ("GPIO23", 16, 23),
    ("3v3 Power", 17, False),   ("GPIO24", 18, 24),
    ("GPIO10", 19, 10),         ("Ground", 20, False),
    ("GPIO9", 21, 9),           ("GPIO25", 22, 25),
    ("GPIO11", 23, 11),         ("GPIO8", 24, 8),
    ("Ground", 25, False),      ("GPIO7", 26, 7),
    ("ID_SD", 27, False),       ("ID_SC", 28, False),
    ("GPIO5", 29, 5),           ("Ground", 30, False),
    ("GPIO6", 31, 6),           ("GPIO12", 32, 12),
    ("GPIO13", 33, 13),         ("Ground", 34, False),
    ("GPIO19", 35, 19),         ("GPIO16", 36, 16),
    ("GPIO26", 37, 26),         ("GPIO20", 38, 20),
    ("Ground", 39, False),      ("GPIO21", 40, 21),
]


sushi_machine_ascii_art: list[str] = [
    "     ________________________ ",
    " ^  |              |      |  |",
    " |  |               \/\/\/   |",
    "    |            ©   SUSI    |",
    "    |   ________             |",
    " Y  |##===0==0=============##|",
    "    |##                    ##|",
    "    |##                    ##|",
    " |  |##____________________##|",
    " v        ''            ''    ",
    "   <-- left  X-axis  right -->"
]

raspberry_pi_ascii_art: list[str] = [
    "------UUUU-----",
    "|©    UUUU   ©|",
    "|           ::|",
    "|           ::|",
    "|   ######  ::|",
    "|   ######  ::|",
    "|   ######  ::|",
    "|   ######  ::|",
    "|           ::|",
    "|B          ::|",
    "|           ::|",
    "|B          ::|",
    "|©           ©|",
    "---------------",
]

servo_hat_ascii_art: list[str] = [
    "------UUU -----",
    "|© °  UUU    ©|",
    "|           ::|",
    "|:::        ::|",
    "|:::        ::|",
    "|:::        ::|",
    "|::: #####  ::|",
    "|::: #####  ::|",
    "|:::        ::|",
    "|:::        ::|",
    "|:::    ==  ::|",
    "|       ==  ::|",
    "|©      ==   ©|",
    "---------------",
]


def print_title(title: str) -> None:
    terminal_length: int = 60
    title_length: int = len(title)
    spacer_left: int = int((terminal_length-title_length)/2)
    spacer_right: int = terminal_length-title_length-spacer_left
    spacer: list[str] = [f"{(spacer_left-2)*'#'}  ", f"  {(spacer_right-2)*'#'}"]
    reset_terminal()
    print()
    print(f"{spacer[0]}{title}{spacer[1]}")
    print()

def print_subtitle(subtitle: str) -> None:
    terminal_length: int = 60
    subtitle_length: int = len(subtitle)
    spacer_left: int = int((terminal_length-subtitle_length)/2)
    print()
    print(f"{spacer_left*' '}{subtitle}")
    print()

def print_centered(context: str) -> None:
    terminal_length: int = 60
    context_length: int = len(context)
    spacer_left: int = int((terminal_length-context_length)/2)
    print(f"{spacer_left*' '}{context}")

def print_context_update(context: str) -> None:
    terminal_length: int = 60
    subtitle_length: int = len(context)
    spacer_left: int = int((terminal_length-subtitle_length)/2)
    print(f"{(spacer_left)*' '}{context}{(spacer_left)*' '}", end="\r")

def print_options(options: list[tuple[str, str]], prompt: str="  Select option: ") -> str:
    terminal_length: int = 60
    print(f"\n  {(terminal_length-4)*'-'}  \n")
    print(f" {prompt}")
    print()
    for option in options:
        if option:
            print(f"   > {option[0].capitalize()} : {option[1]}")
        else:
            print()

    return get_valid_input(options=options, prompt="   ? ")


def get_valid_input(options: list[dict[str, str]], prompt: str) -> str:
    option = None  
    print()
    while True:
        if option is not None:
            print(f"Invalid input {option}, try again.")
            clear_terminal_line()
        option = input(prompt).lower()

        clear_terminal_line()
        move_terminal_cursor_up()
        move_terminal_cursor_up()

        if option in [valid_option[0] for valid_option in options if valid_option]:
            return option


def exit_terminal_menu(prompt: str=None) -> None:
    terminal_length: int = 60
    prompt_length: int = len(prompt)
    spacer_left: int = int((terminal_length-prompt_length)/2)
    reset_terminal()
    print("\n")
    if prompt is not None:
        print(f"{spacer_left*' '}{prompt}")
        print("\n")
    print(f"{int((terminal_length-4)/2)*' '}Bye!")
    print("\n")
    exit(0)


def print_ascii_art(ascii_art: list[str], spaces: int=0) -> None:
    for line in ascii_art:
        print(f"{spaces*' '}{line}")


def reset_terminal() -> None:
    print("\033c", end="")


def move_terminal_cursor_up(lines: int=1) -> None:
    sys.stdout.write("\033[F"*lines)


def clear_terminal_line() -> None:
    sys.stdout.write("\033[K")