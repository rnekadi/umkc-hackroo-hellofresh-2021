from pyspark.sql.types import *

# Define custom schema

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
