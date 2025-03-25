from pyspark.sql import SparkSession

spark_obj = (SparkSession.builder.appName("Spark Introduction").master("local[2]").getOrCreate())

spark_obj