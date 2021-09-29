"""
Author :  Raju Nekadi
Description: This file is exposes a utility function called to get SparkSession to retun a valid spark session
"""


from pyspark.sql import SparkSession
from src.logging.logger import *


def get_spark_session():
    try:
        logger=get_session()
        spark=SparkSession.builder.appName('helloFresh-assesment').getOrCreate()
        logger.info("sparkSession.py  ->  Completed Successfully")
        return spark
    except Exception as e:
        logger.info(" Unable to Create Spark Session !!!")
        logger.exception("Error in get_spark_session function " + str(e))