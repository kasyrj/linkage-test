#!/usr/bin/python3

import sys
import os
import csv

class FileTools():
    
    @staticmethod
    def writeFile(filename, arrContents):
        '''Write an array to file.'''
        outfile = open(filename,'w')
        for line in arrContents:
            outfile.write(line)
        outfile.close()

class CsvParser():

    @staticmethod
    def readCsv(filename, as_dict=False, delimiter="\t", encoding="utf-8"):
        '''Read a CSV and returns a list version of the format CSV[line_number][field_number]'''
        out = []
        with open(filename, newline="", encoding=encoding) as f:
            reader = csv.reader(f, delimiter=delimiter, dialect="excel")
            for line in reader:
                out.append(line)
        if as_dict == True:
            out = CsvParser.parseCsvListAsDict(out)
        return out

    @staticmethod
    def parseCsvListAsDict(csv_list):
        '''Parse a CSV list as a dict with headers from the first row as keys. Headerless columns are omitted.'''
        out = {}
        headers = []
        for col_num in range(len(csv_list[0])):
            if csv_list[0][col_num] != "":
                headers.append(csv_list[0][col_num])
        if (len(set(headers)) != len(headers)):
            print("ERROR: column headers must be unique for dict conversion", file=sys.stderr)
            quit()
        for col_num in range(len(csv_list[0])):
            header = csv_list[0][col_num]
            out[header] = []
            for row_num in range(1,len(csv_list)):
                out[header].append(csv_list[row_num][col_num])
        return out
