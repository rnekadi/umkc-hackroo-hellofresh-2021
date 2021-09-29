"""
Author :  Raju Nekadi
Description: This file is written to define recipe class to extract,transform input record from json.

"""

from src.config.sparksession import *
import pyspark.sql.functions as F
from src.schema.recipeschema import *
from src.udf.secondsudf import *

# Initiate logger
logger = get_session()

# Initiate Spark Session
spark = get_spark_session()

# Initialize Spark Context
sc = spark.sparkContext


class Recipe:
    def extract_input_file(self, input_path):
        """Load data from json file format.
        :param spark: input_path.
        :return: Spark DataFrame.
        """
        try:
            logger.info("Reading Input Json File ...!!!")
            recipe_df = spark.read.schema(recipe_schema).json(input_path)
            logger.info("Input File Read Successfully")
            return recipe_df
        except Exception as e:
            logger.info("Failed to Read Input File!!!")
            logger.exception("Error in extract input file function " + str(e))

    def transform_dataframe(self, recipe_df):
        """Transform original dataset.
        :param df: Input DataFrame.
        :return: Transformed DataFrame.
        """
        try:
            logger.info("Performing the Transformation on the input file ...")
            avg_cooktime_df = recipe_df.filter(F.lower(F.col('ingredients')).contains('beef')) \
                .withColumn("totalCookTime", secondsDF(F.col('prepTime')) + secondsDF(F.col('cookTime'))) \
                .withColumn('difficulty', when((F.col("totalCookTime") >= 3600), F.lit("HARD"))
                            .otherwise(F.when((F.col("totalCookTime") >= 1800), F.lit("MEDIUM"))
                                       .otherwise(F.when((F.col("totalCookTime") <= 1800), F.lit("EASY")).otherwise(F.lit("UNKNOWN"))))) \
                .groupBy('difficulty').agg(round(F.avg('totalCookTime'), 2).alias('avgCookTime'))
            return avg_cooktime_df
            logger.info("Successfully Calculated Average Cook Time")
        except Exception as e:
            logger.info("Failed to transform Input File!!!")
            logger.exception("Error in transform_dataframe function " + str(e))

    def write_report(self, dataframe, path):
        """Write the dataframe to CSV file.
               :param df: Input DataFrame.
               :return: report csv file
        """
        try:
            dataframe.toPandas().to_csv(path, index=False)
            logger.info("Successfully write report csv file")
        except Exception as e:
            logger.info("Failed to Write Report File!!!")
            logger.exception("Error in write_report function " + str(e))

    def read_ouput(self, path):
        """Read  the csv file and return dataframe
            :param df: Path of the report file.
            :return: dataframe object
        """
        try:
            output_df = spark.read.csv(path)
            return output_df
        except Exception as e:
            logger.exception("Error in read_ouput function " + str(e))
