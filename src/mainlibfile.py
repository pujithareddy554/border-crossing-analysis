# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 02:19:50 2020

@author: pujit
"""

from datetime import datetime
from itertools import chain
import math
from operator import itemgetter
import pathlib
import errno
import os
import csv

def final_resultset(total_list, result_key, measure_key, measure_values):

    if not total_list:
        raise IndexError("Error! The list of cumulative average is empty.")

    new_total_list = []
    i = 0
    for key in measure_values.keys():

        # If the list has 1 value!
        if len(list(chain(*total_list))) == 2 and total_list[0][0] in measure_values.values():

            # saves in this order: <Border>, <Date>, <Measure>, <Value>, <Average>
            return [result_key, key, measure_key, total_list[0][0], total_list[0][1]]

        # if the list has more than 1 value
        elif len(list(chain(*total_list))) > 2:
            if total_list[i][0] in measure_values.values() and i < len(list(chain(*total_list))):
                new_total_list.append([result_key, key, measure_key, total_list[i][0], total_list[i][1]])
                i += 1

        else:
            raise ValueError("Error: total_list does not has less than one pair of values.")

    return new_total_list
def c_average(values_list):
    """" Gathers the cumulative average for each measure.
         So if the values list has more than one value,
         then there will be two numbers, the total sum at
         that step as well as the cumulative average.
    Args:
        values_list: list of values of the specific measure
    Return:
        list: if there are not multiple values, then return
              the singular value and 0, otherwise return
              the value at each step of the cumulative average.
    """

    if len(values_list) == 1:
        for value in values_list:
            return [tuple((value, 0))]

    new_list = [0] * len(values_list)

    new_p, counter = 0, 0
    for i in range(len(values_list)-1, -1, -1):
        new_list[i] = new_p
        new_p += values_list[i]

        if counter >= 1:
            new_list[i] = math.floor(new_list[i]/counter) if (new_list[i]/counter) - math.floor(new_list[i]/counter) < 0.5 else math.floor(new_list[i]/counter)+1

        counter += 1

    return list(zip(values_list, new_list))
def sum_values(date_value):
    """Sums all the measure values
    Args:
        measure_value: Dictionary which holds the Date and Time as a key,
                       and the value the current number of crossings and 0
    Returns:
        the sum of all the measure values for that dictionary
    """
    for key, value in date_value.items():
        date_value[key] += value

    return date_value
def find_average(border):
    data_process_list = []

    for border_key, measure_value in border.items():
        for measure_key, date_value in measure_value.items():
            date_values = sum_values(date_value)

            updated_list = [v for v in (date_values.values())]
            cumulative_list = c_average(updated_list)

            key_id = final_resultset(cumulative_list, border_key, measure_key, date_values)

            if len(key_id) == 5:
                data_process_list.append(key_id)
            else:
                data_process_list += key_id

    # Sort the list by Date, Value, Measure, Border with the most recent dates
    sorted_list = sorted(data_process_list, key=itemgetter(3, 2, 0),
                                                 reverse=True)
    final_list = sorted(sorted_list,
                               key=lambda x: datetime.strptime(x[1],
                                                               '%d/%m/%Y %H:%M:%S %p'),
                               reverse=True)

    return final_list
def write_to_csv(name_of_output_file, final_list):
    """ Writes the file out to csv file row by row.
    Args:
        name_of_output_file: name of the output file
        final_list: the list which holds all the border data information
    Raises:
        OSError: If the file does in fact exist
        FileNotFoundError: If the file is not found
    """

    try:
        filepath = name_of_output_file
    except OSError:
        if pathlib.Path(name_of_output_file).resolve(strict=True):
            pass
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    name_of_output_file)

    # Write out to the output csv file
    with open(filepath, mode='w') as csv_outfile:
        outfile_writer = csv.writer(csv_outfile, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_NONE)

        # Column headers--Don't quote them
        outfile_writer.writerow(['Border', 'Date', 'Measure', 'Value', 'Average'])

        outfile_writer = csv.writer(csv_outfile, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)

        # for each row in the final list, remove the list of list
        # and create one list
        for row in final_list:
            outfile_writer.writerow(row)
