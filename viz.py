"""
Helper functions for visualization and debugging.
"""

def table_position(table):
    """
    This function prints the position of the table.
    """

    ### Example ###
    #       -----*-----                         = 110 mm
    #       =  42.5 mm
    #
    #            0 1 2 3 4 5 6 7 8 9 º          = 200 mm / 100 %
    #
    #   0       |                     |
    #   2       |                     |
    #   4       |                     |
    #   6       |                     |
    #   8       |                     |
    #   º       |                     |
    #
    #       = 132 mm / 100 %

    print_rows = 5
    print_cols = 20

    table_wings = 5                                             # wing size of the table

    schema = []
    for i in range(print_rows + 1):
        schema.append(table_wings*" " + "|" + (print_cols+1)*" " + "|" + table_wings*" ")

    ud_pos = round(table[0] * print_rows)
    lr_pos = round(table[1] * print_cols)

    start_index = table_wings + 1                               # start index in h direction

    row = schema[ud_pos]
    schema[ud_pos] = row[:lr_pos+start_index-table_wings]        # cuts everything after table
    schema[ud_pos] += table_wings*"-" + "*" + table_wings*"-"    # prints table with wings
    schema[ud_pos] += row[lr_pos+start_index+table_wings+1:]     # cuts everything before table   


    print()
    print(f"     "+(table_wings+1)*" "+"0 1 2 3 4 5 6 7 8 9 º")
    print()
    print(f"0    {schema[0]}")
    print(f"2    {schema[1]}")
    print(f"4    {schema[2]}")
    print(f"6    {schema[3]}")
    print(f"8    {schema[4]}")
    print(f"º    {schema[5]}")
    print()
    print(table)