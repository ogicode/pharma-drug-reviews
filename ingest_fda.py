# Databricks notebook source
import requests
from datetime import date

r = requests.get("https://api.fda.gov/drug/event.json?limit=10")
path = f"/Volumes/workspace/pharma/volume/fda_{date.today()}.json"

with open(path, "w") as f:
    f.write(r.text)

dbutils.notebook.exit(path)