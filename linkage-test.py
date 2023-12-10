#!/usr/bin/python3

import sys
import os.path
import argparse
from pathlib import Path
from filetools import FileTools, CsvParser
from csv_binary import CSVBinaryDataset
from linkage import LinkageTest

PARSER_DESC = "Perform linkage test for multistate data from Syrjänen et al. (2016)."

DEFAULT_MISSING = '-'
DEFAULT_ABSENT = '0'
DEFAULT_PRESENT = '1'
DEFAULT_DATAPOINT_ID = 'DP'


parser = argparse.ArgumentParser(description=PARSER_DESC)

parser.add_argument("-i","--input-file",
                    dest="input_file",
                    help="Input file (CSV).",
                    default=None,
                    metavar="INPUT_FILE",
                    type=str)

parser.add_argument("-o","--output-file",
                    dest="output_file",
                    help="Output file (CSV).",
                    default=None,
                    metavar="OUTPUT_FILE",
                    type=str)

parser.add_argument("-m","--missing",
                    dest="missing",
                    help="String designating a missing character. Default: '" + DEFAULT_MISSING + "'",
                    default=DEFAULT_MISSING,
                    metavar="MISSING_STRING",
                    type=str)

parser.add_argument("-a","--absent",
                    dest="absent",
                    help="String designating a meaningfully absent character. Default: '" + DEFAULT_ABSENT + "'",
                    default=DEFAULT_ABSENT,
                    metavar="ABSENT_STRING",
                    type=str)

parser.add_argument("-p","--present",
                    dest="present",
                    help="String designating a present character. Default: '" + DEFAULT_PRESENT + "'",
                    default=DEFAULT_PRESENT,
                    metavar="PRESENT_STRING",
                    type=str)

parser.add_argument("-d","--datapoint-id",
                    dest="datapoint_id",
                    help="Field for datapoint ID. Default: '" + DEFAULT_DATAPOINT_ID + "'",
                    default=DEFAULT_DATAPOINT_ID,
                    metavar="UNIQUE_ID_COLUMN",
                    type=str)

args = parser.parse_args()

if args.input_file == None:
    print("Please specify an input file.", file=sys.stderr)
    quit()

if (os.path.isfile(args.input_file) == False):
    print("Please specify an input file.", file=sys.stderr)
    quit()

dataset_params = {
    "datapoint_id_column": args.datapoint_id,
    "missing_char": args.missing,
    "meaningfully_empty_char": args.absent,
    "present_char": args.present,
}

dataset = CSVBinaryDataset(CsvParser.readCsv(args.input_file, delimiter=",",as_dict=True), dataset_params)

if args.output_file != None:
    output_file = Path(args.output_file)
    if output_file.is_file():
        print("output file already exists. Please rename or delete the existing file and rerun.", file=sys.stderr)
        quit()

linkageTest = LinkageTest()
results = linkageTest.run(dataset)
if args.output_file != None:
    FileTools.writeFile(args.output_file, results)
    quit()


else:
    output = ''
    for row in results:
        output += row
    print(output)
    quit()   
