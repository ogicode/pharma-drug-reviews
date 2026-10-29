# Databricks notebook source
# Silver: clean and type the bronze data.
# Good rows go to silver, bad rows go to quarantine.
from pyspark.sql.functions import col, to_date, explode_outer

bronze = spark.table("workspace.pharma.bronze_fda_events")

# report columns, shared by both tables
report_cols = [
    col("safetyreportid").alias("report_id"),
    # FDA dates come as yyyyMMdd strings
    to_date("receivedate", "yyyyMMdd").alias("received_date"),
    # 1 = serious, 2 = not serious
    col("serious").cast("int").alias("serious"),
    # 0 = unknown, 1 = male, 2 = female
    col("patient.patientsex").cast("int").alias("patient_sex"),
    col("patient.patientonsetage").cast("int").alias("patient_age"),
    col("occurcountry").alias("country"),
]

# drugs: one row per report and drug, reports with no drugs keep a null
drugs = bronze.select(
    *report_cols,
    explode_outer("patient.drug.medicinalproduct").alias("drug_name"),
).dropDuplicates(["report_id", "drug_name"])

# reactions: one row per report and side effect
reactions = bronze.select(
    col("safetyreportid").alias("report_id"),
    explode_outer("patient.reaction.reactionmeddrapt").alias("reaction"),
).dropDuplicates(["report_id", "reaction"])

# a row is bad if any key field is missing
bad = col("report_id").isNull() | col("received_date").isNull() | col("drug_name").isNull()

drugs.filter(bad).write.mode("overwrite").option("overwriteSchema", True).saveAsTable("workspace.pharma.quarantine_fda_events")
drugs.filter(~bad).write.mode("overwrite").option("overwriteSchema", True).saveAsTable("workspace.pharma.silver_fda_events")
reactions.filter(col("reaction").isNotNull()).write.mode("overwrite").option("overwriteSchema", True).saveAsTable("workspace.pharma.silver_fda_reactions")