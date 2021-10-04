# HelloFresh University Missouri Hackathon Excercise Spring 2021 

Thank you for your interest in joining HelloFresh UMKC Hackathon Challenge !

Please submit your answers in a different branch and create a pull request. Please do not merge your own pull request.


# HelloFresh
At HelloFresh, our mission is to change the way people eat - forever. From our 2011 founding in Europe’s vibrant tech hub Berlin, we’ve become the global market leader in the meal kit sector and inspire millions of energized home cooks across the globe every week.
We offer our meal kit boxes full of exciting recipes and thoughtfully sourced, fresh ingredients in more than 13 countries, operating from offices in Berlin, New York City, Sydney, Toronto, London, Amsterdam and Copenhagen and shipped out more than 250 Million meals in 2019.
Data Engineering Team at HelloFresh
We ingest events from our Kafka Stream and store them in our DataLake on s3.
Events are sorted by arriving date. For example `events/recipe_changes/2019/11/29`.
During events processing we heavily rely on execution day to make sure we pick proper chunk of data and keep historical results.
We use Apache Spark to work with data and store it on s3 in parquet format. Our primary programming language is Python.

# Exercise
## Overview
At HelloFresh we have a big recipes archive that was created over the last 8 years.
It is constantly being updated either by adding new recipes or by making changes to existing ones.
We have a service that can dump archive in JSON format to selected s3 location.
We are interested in tracking changes to see available recipes, their cooking time and difficulty level.

## Task 1
Using Apache Spark and Python, read and pre-process rows to ensure further optimal structure and performance
for further processing.
Use the dataset on S3 as the input (https://s3-eu-west-1.amazonaws.com/dwh-test-resources/recipes.json). It's fine to download it locally.

## Task 2
Using Apache Spark and Python read processed dataset from step 1 and:
1. extract only recipes that have `beef` as one of the ingredients
2. calculate average cooking time duration per difficulty level

Total cooking time duration can be calculated by formula:
```bash
total_cook_time = cookTime + prepTime
```  

Criteria for levels based on total cook time duration:
- easy - less than 30 mins
- medium - between 30 and 60 mins
- hard - more than 60 mins.

## Deliverables
- A deployable Spark Application written in Python
- a README file with brief explanation of approach, data exploration and assumptions/considerations.
You can use this file by adding new section or create a new one.
- a CSV file with average cooking time per difficulty level. Please add it to an `output` folder.
File should have 2 columns: `difficulty,avg_total_cooking_time` and named as `report.csv`

## Requirements
- Well structured, object-oriented, documented and maintainable code
- Unit tests to test the different components
- Errors handling
- Documentation
- Solution is deployable and we can run it

## Bonus points
- Config handling
- Logging and alerting
- Consider scaling of your application
- CI/CD explained
- Performance tuning explained
- We love clean and maintainable code
- We appreciate good combination of Software and Data Engineering

Good Luck!

# Solution

## Approach to identify the average cook time for each difficulty level.

 - Input file and Schema
 
 First of downlaoded the file from s3 to local inside project resource folder. The recipes schema for input json defined.
 
 
  ```python
recipe_schema = StructType([
    StructField("name", StringType(),True),
    StructField("ingredients", StringType(),True),
    StructField("url", StringType(),True),
    StructField("image", StringType(), True),
    StructField("cookTime", StringType(), True),
    StructField("recipeYield", StringType(), True),
    StructField("datePublished", StringType(), True),
    StructField("prepTime", StringType(), True),
    StructField("description", StringType(), True)
  ])
``` 
 
 
 ## Recipe Class
 For performing extract , transform and load of output csv report defined the recipe class.The recipe class consists of 
 different functions
 
 - Extract This method extract the input file and and creates the recipe dataframe for transform.
 
 
 ```python
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
``` 

- Tranform: This method take the recipe dataframe and and identify the average cook time for each difficulty.
In transform step I first filter out all the records which ingredients contains beef. Then we used the custom udf to 
get the given cook and prep time to seconds and calculate  total cook time for recipe.
Next identified the difficulty as per given criteria.
In the final step group the difficulty to aggregate average total cook time.




```python
  
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
``` 

Load : This method load the compuated average cook time for each difficulty into csv file in output folder.

 
```python
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
``` 


 ## Executor Class
 
The executor class is setup to perform the tasks which will provide provide input and output locations to task.

```python
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

```


## Main Module

app.py main module is setup to perform etl using the executors and recipe class.The main called by 
passing the task name as argument.

```python
if __name__=="__main__":
	"""Main  ETL module script definition.
	:return: None
	"""
	try:
		logger.info("Recipe ETL Process has been Started !!!")
		arg.parser.add_argument('task', type=str, help='Name of the task need to perform')
		args, _ = arg.parser.parse_known_args()
		task_name = args.task
		etl = Executor(task_name)
		etl.run()
	except Exception as e:
		logger.info("Failed to load input args!!!")
		logger.exception("Error in main function " + str(e))

```

Running main module

```python

python app.py --task avgCookTime

```

## Test Cases

Set up the test case to test the various components using pytest module.


- Fixture


```python
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
```

 - Cases
 
 1.Test case to assert number of row in output report.
 
 ```python
def test_report_size(get_report):
    record_count, records = get_report
    assert record_count == 3
```

 2. Test to assert the average cook time for easy diffucltiy recipe 
 
  ```python
 def test_easy_difficulty(get_report):
    record_count, records = get_report
    for record in records:
        if record['difficulty'] == 'EASY':
            assert float(record['avgCookTime']) == 1177.5
  ```           
 
 3. Test to assert the average cook time for easy diffucltiy recipe 
 
 ```python
def test_easy_difficulty(get_report):
    record_count, records = get_report
    for record in records:
        if record['difficulty'] == 'EASY':
            assert float(record['avgCookTime']) == 1177.5
 ```
            
 4. Test to assert the average cook time for easy diffucltiy recipe 
 
 ```python
 def test_hard_difficulty(get_report):
    record_count, records = get_report
    for record in records:
        if record['difficulty'] == 'HARD':
            assert float(record['avgCookTime']) == 10468.89
```

Running Test cases


 ```python
  pytest -v --cov
 ```
 
 
## Building the Solution using Wheel


- Build :

 ```python
python3 setup.py sdist bdist_wheel 
 ```
 
 - Deploy
 
```python
  pip install raju_umkc_hellofresh_2021-0.0.1-py3-none-any.whl
 ```
 
 

## Continous Integration

For automating the build and test process I have used  Circle CI to setup continous Integration process.

Added a CircleCI configuration file to the project. Created a folder named .circleci. 
In the .circleci folder, created a file named config.yml.


```yaml

# Python CircleCI 2.0 configuration file
version: 2
jobs:
  build_test:
    docker:
      - image: circleci/python:3.7
    steps:
      - checkout  # checkout source code to working directory
      - run:
          name: create whl and install dependencies
          command: |  # create whl and use pipenv to install dependencies
            python setup.py sdist bdist_wheel
            sudo pip install pipenv
            pipenv install dist/raju_data_engineering_test-0.0.1-py3-none-any.whl
            pipenv install pytest
      - run:
          name: run tests
          command: |  # Run test suite
            pipenv run pytest -v --cov

```

next step are to Integrating the the repo with to Circle CI.One environment variable and change log are setup 
build and test pipeline can be run when there is new update to source code. 

Please note due to github repo issues i was not able to Integrate this with Circle CI.

 







 


