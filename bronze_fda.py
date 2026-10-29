# Databricks notebook source
# Bronze: load all raw FDA JSON files from the volume into a table as is.
# No filtering, bad rows are kept. Bronze is the raw truth.
from pyspark.sql.functions import explode, current_timestamp

df = (spark.read.option("multiline", True).json("/Volumes/workspace/pharma/volume/fda_*.json")
      # one row per adverse event report, keep source file for lineage
      .select(explode("results").alias("r"), "_metadata.file_path")
      .select("r.*", "file_path")
      # when the row was loaded
      .withColumn("ingested_at", current_timestamp()))

df.write.mode("overwrite").saveAsTable("workspace.pharma.bronze_fda_events")