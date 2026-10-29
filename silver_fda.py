# Databricks notebook source
# Silver: clean and type the bronze data.
# Good rows go to silver, bad rows go to quarantine.
from pyspark.sql.functions import col, to_date, explode_outer

df = spark.table("workspace.pharma.bronze_fda_events").select(
    col("safetyreportid").alias("report_id"),
    # FDA dates come as yyyyMMdd strings
    to_date("receivedate", "yyyyMMdd").alias("received_date"),
    # 1 = serious, 2 = not serious
    col("serious").cast("int").alias("serious"),
    # 0 = unknown, 1 = male, 2 = female
    col("patient.patientsex").cast("int").alias("patient_sex"),
    # one row per report and drug, keeps reports with no drugs as null
    explode_outer("patient.drug.medicinalproduct").alias("drug_name"),
).dropDuplicates(["report_id", "drug_name"])

# a row is bad if any key field is missing
bad = col("report_id").isNull() | col("received_date").isNull() | col("drug_name").isNull()

df.filter(bad).write.mode("overwrite").saveAsTable("workspace.pharma.quarantine_fda_events")
df.filter(~bad).write.mode("overwrite").saveAsTable("workspace.pharma.silver_fda_events")