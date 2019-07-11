from functools import reduce

default_cell_alignment = 'l'
vertical_border_char = '|'
minor_horizontal_border_char = '-'
major_horizontal_border_char = '='


def get_alignment_char(friendly_char):
    """
    Converts a friendly alignment char, i.e. 'l', 'r', 'm', to
    internal python string.format alignment char, i.e. '^', '<', '>'.
    Defaults to left alignment, i.e. '<'.
    """
    char_map = {'l': '<', 'r': '>', 'm': '^'}
    return char_map[friendly_char] if friendly_char in char_map else char_map[default_cell_alignment]


def create_cell_format(column_config):
    """
    Creates a python string format for a table cell, i.e. '{:30}|'. If
    left or right aligned, applies appropriate padding of 1 space char.

    Args:
        column_config: length-2 tuple, [0] is *proper* alignment char, i.e '^',
                       [1] is column chracter width, i.e. 20
    """
    a = column_config[0]
    w = column_config[1]

    w = w-1 if a in {'l', 'r'} else w
    left_padding = ' ' if a == 'l' else ''
    right_padding = ' ' if a == 'r' else ''

    return left_padding + '{:' + get_alignment_char(a) + str(w-1) + '}|' + right_padding


def create_row_format(col_widths, col_alignments=None):
    vertical_border_char = '|'
    _col_alignments = col_alignments \
        if col_alignments is not None \
        else ['l']*len(col_widths)
    # {(20, 'left'), (30, 'middle'), ...}
    column_config = zip(_col_alignments, col_widths)

    # '|{:<20}|{:^30}|...|'
    return reduce(lambda acc, c: (acc + create_cell_format(c)),
                  column_config,
                  vertical_border_char)


def create_horizontal_divider(char, col_widths):
    return reduce(lambda acc, w: acc + char*(w-1) + '+', col_widths, '+')


def print_rows(rows, row_format) -> list:
    # need to create row preserve since some lists in python are "consumed" upon use
    rows_preserve = []
    for row in rows:
        rows_preserve.append(row)
        print(row_format.format(*row))

    return rows_preserve


def tabulate(rows, headers, col_widths, col_alignments=None):
    """
    Pretty-prints a table for the given rows and headers (columns).
    Returns 

    Args:
        rows: A list of lists, i.e. the data rows of the table,
              i.e. {{'1', '2'}, {'3', '4'}, ...}.
        headers: A list of column header strings, i.e. {'id', 'name', 'age'}
        col_widths: A list of column character-width integers, i.e. {5, 60, 10}
        col_alignments: A list of column alignment strings, i.e. {'l', 'r', 'm'}.

    Returns:
        A copy of the "rows" value the function recieved (in-case it was a
        iterable that is consumed like maps).
    """
    header_row_seperator = create_horizontal_divider(
        major_horizontal_border_char, col_widths)
    data_row_seperator = create_horizontal_divider(
        minor_horizontal_border_char, col_widths)

    header_row_format = create_row_format(
        col_widths, col_alignments=['m']*len(col_widths))
    data_row_format = create_row_format(
        col_widths, col_alignments=col_alignments)

    print(data_row_seperator)
    print(header_row_format.format(*headers))
    print(header_row_seperator)
    rows_preserve = print_rows(rows, data_row_format)
    print(data_row_seperator)

    return rows_preserve
