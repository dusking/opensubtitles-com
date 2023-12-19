"""
This file is part of Opensubtitles API wrapper.

Opensubtitles API is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published by the Massachusetts
Institute of Technology.

For full details, please see the LICENSE file located in the root
directory of this project.
"""
from operator import itemgetter
from collections import OrderedDict

from prettytable import PrettyTable


def dicts_to_pt(data, sort=None, align=None):
    """Convert a list of dictionaries to a PrettyTable.

    Parameters:
    - data (list): A list of dictionaries to be converted (must have same keys).
    - sort (str, optional): The key to sort the data. Defaults to None.
    - align (str, optional): The alignment of columns. Defaults to None.

    Returns:
    PrettyTable: A PrettyTable containing the converted data.
    """
    data = sorted(data, key=itemgetter(sort), reverse=False) if sort else data
    all_keys = sum([list(x.keys()) for x in data], [])  # get a list of all keys
    columns = list(OrderedDict.fromkeys(all_keys))  # remove duplicates, uses OrderedDict to keep the order of columns
    columns, data = add_numbers_column(columns, data)
    return generate_table(columns, data=data, align=align)


def dict_to_pt(data, align=None):
    """Convert a dict to a PrettyTable.

    Parameters:
    - data (list): The dictionary be convert.
    - align (str, optional): The alignment of columns. Defaults to None.

    Returns:
    PrettyTable: A PrettyTable containing the converted data.
    """
    list_of_dicts = [{"key": k, "value": v} for k, v in data.items()]
    return dicts_to_pt(list_of_dicts, None, align)


def add_numbers_column(columns, items):
    """Add a column with line numbers to the list of columns and items.

    Parameters:
    - columns (list): The list of column names.
    - items (list): The list of items (dictionaries) to be numbered.

    Returns:
    tuple: A tuple containing the modified columns and items.
    """
    columns.insert(0, "#")
    line_number = 1
    for item in items:
        item["#"] = line_number
        line_number += 1
    return columns, items


def generate_table(cols, data, align=None):
    """Generate a PrettyTable from a list of columns and data.

    Parameters:
    - cols (list): The list of column names.
    - data (list): The list of dictionaries representing rows.
    - align (str, optional): The alignment of columns. Defaults to None.

    Returns:
    PrettyTable: A PrettyTable containing the specified columns and data.
    """
    pt = PrettyTable(cols)

    for row_data in data:
        pt.add_row([row_data[column] for column in cols])

    pt.align = align if align else pt.align
    return pt
