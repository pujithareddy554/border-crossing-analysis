# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
from mainlibfile import find_average, write_to_csv
def main():
    data_dict = {} # Data Storage, Data is stored in a nested dictonary.
    with open("Border_Crossing_Entry_Data.csv", 'r') as data_file: # Data Preparation Stars
        data = csv.DictReader(data_file, delimiter=",")
        for row in data:
            md =  data_dict.get(row["Border"], dict()) 
            item = md.get(row["Measure"], dict())
            if(row["Date"]) in item:
                item[row["Date"]] += int(row["Value"])
            else:
                item[row["Date"]] = int(row["Value"])
            md[row["Measure"]] = item
            data_dict[row["Border"]] = md  # Data is processed and prepared to fit the model.
    dataToWrite=find_average(data_dict) # Calculating the averages
    write_to_csv("results.csv", dataToWrite) # writing the data in to results file
if __name__ == '__main__':
    main()