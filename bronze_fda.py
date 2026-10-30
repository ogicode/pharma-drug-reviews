# Databricks notebook source
# Bronze: load all raw FDA JSON files from the volume into a table as is
# and add file metadata
from pyspark.sql.functions import explode

df = (spark.read.option("multiline", True).json("/Volumes/workspace/pharma/volume/fda_*.json")
      # one row per adverse event report, keep source file and its arrival time
      .select(explode("results").alias("r"), "_metadata.file_path", "_metadata.file_modification_time")
      .select("r.*", "file_path", col("file_modification_time").alias("ingested_at")))

# overwriteSchema: FDA JSON shape can change, so replace the table schema
df.write.mode("overwrite").option("overwriteSchema", True).saveAsTable("workspace.pharma.bronze_fda_events")