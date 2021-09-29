
"""
Author :  Raju Nekadi
Description: This file is written to define executor class to extract,transform input record from json.

"""

from src.modules.recipe import *


class Executor(Recipe):
    def __init__(self, tasks=[]):
        self.tasks = tasks

    def run(self):
        logger.info(" Starting the ETL Process")
        logger.info(self.tasks)

        input_file_path = "./resource/recipe.json"
        output_file_path = "./output/report.csv"

        if self.tasks == "avgCookTime":
            recipe_df = Recipe.extract_input_file(self, input_file_path)
            avg_cooktime_df = Recipe.transform_dataframe(self, recipe_df)
            Recipe.write_report(self, avg_cooktime_df, output_file_path)
        else:
            logger.info('Not a valid task')

        # log the success and terminate Spark application
        logger.info('app job is finished')
        spark.stop()
