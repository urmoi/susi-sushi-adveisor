import init
import viz
from check import homing


# Example Code
def main():

    table = init.tof2pos((20, 100))

    viz.table_position(table)

    # table, template, fillings = homing(table, template, fillings)

    # vis.table_position(table)


if __name__ == "__main__":
    main()



    
