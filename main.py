import sys

import controller
import init


def main() -> None:

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


if __name__ == "__main__":
    main()