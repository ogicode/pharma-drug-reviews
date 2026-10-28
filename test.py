# list rows
from databricks.connect import DatabricksSession
spark = DatabricksSession.builder.profile("ogicode").serverless().getOrCreate()
spark.sql("SELECT * FROM samples.bakehouse.sales_transactions LIMIT 10").show()