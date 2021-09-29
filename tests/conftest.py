"""
Author :  Raju Nekadi
Description: This file is written to define fixture function test cases.This function read the output file
and return line count and rows to test cases.

"""

import pytest
import csv
from collections import OrderedDict


@pytest.fixture()
def get_report():
    rows = []
    with open('output/report.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            line_count += 1
            rows.append(row)
    return line_count, rows
