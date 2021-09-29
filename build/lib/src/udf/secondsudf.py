"""
Author :  Raju Nekadi
Description: This file is written to define UDF for converting the time to seconds using isodate libraryc function.
"""

import isodate

from pyspark.sql.functions import *


def get_seconds(col):
    if col:
        duration = isodate.parse_duration(col)
        return duration.total_seconds()
    else:
        return 0


secondsDF = udf(lambda z: get_seconds(z))