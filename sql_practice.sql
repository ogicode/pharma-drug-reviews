-- www.sql-practice.com
-- select columns, from table, filter, limit
-- patients who live in Hamilton
select first_name, city
from patients
where city = 'Hamilton'
limit 10;

-- show patients and diagnosis
select p.first_name, a.diagnosis
from patients p join admissions a 
on p.patient_id = a.patient_id
where diagnosis = "Asthma Exacerbation"
-- WHERE first_name LIKE 'C%';
-- where city in ("Hamilton", "Dundas")

# pandas
# Hamilton patients
patients.loc[patients["city"] == "Hamilton", ["first_name", "city"]].head(10)

# patients + diagnosis
df = patients.merge(admissions, on="patient_id")   # how="inner" default
df.loc[df["diagnosis"] == "Asthma Exacerbation", ["first_name", "diagnosis"]]

# LIKE 'C%'
patients[patients["first_name"].str.startswith("C")]

# IN (...)
patients[patients["city"].isin(["Hamilton", "Dundas"])]

#pyspark
from pyspark.sql import functions as F

# Hamilton patients
patients.filter(F.col("city") == "Hamilton").select("first_name", "city").limit(10)

# patients + diagnosis
(patients.alias("p")
    .join(admissions.alias("a"), "patient_id")      # how="inner" default
    .filter(F.col("a.diagnosis") == "Asthma Exacerbation")
    .select("p.first_name", "a.diagnosis"))

# LIKE 'C%'
patients.filter(F.col("first_name").like("C%"))

# IN (...)
patients.filter(F.col("city").isin("Hamilton", "Dundas"))