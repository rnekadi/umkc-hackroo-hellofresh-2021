"""
Author :  Raju Nekadi
Description: This file is written to define all the unit test cases.

"""


def test_report_size(get_report):
    record_count, records = get_report
    assert record_count == 3


def test_easy_difficulty(get_report):
    record_count, records = get_report
    for record in records:
        if record['difficulty'] == 'EASY':
            assert float(record['avgCookTime']) == 1177.5


def test_medium_difficulty(get_report):
    record_count, records = get_report
    for record in records:
        if record['difficulty'] == 'MEDIUM':
            assert float(record['avgCookTime']) == 2400.0


def test_hard_difficulty(get_report):
    record_count, records = get_report
    for record in records:
        if record['difficulty'] == 'HARD':
            assert float(record['avgCookTime']) == 10468.89






