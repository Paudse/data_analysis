from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("local-test") \
    .master("local[*]") \
    .getOrCreate()

print("Spark ready!")

data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
columns = ["name", "age"]

df = spark.createDataFrame(data, columns)
df.show()

df.filter(df.age > 30).show()
df.groupBy().avg("age").show()

df = spark.read.csv("data.csv", header=True, inferSchema=True)
df.printSchema()
df.show(5)

df.groupBy("city").count().show()

spark.stop()