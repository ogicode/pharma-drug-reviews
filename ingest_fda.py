# Databricks notebook source
# Ingest: each run saves the next FDA report as one JSON file in the volume.
import os
import requests

folder = "/Volumes/workspace/pharma/volume"

# number of reports already loaded = how many to skip
n = len([f for f in os.listdir(folder) if f.startswith("fda_")])

# sorted by date so the order stays the same between runs
r = requests.get(f"https://api.fda.gov/drug/event.json?sort=receivedate:asc&skip={n}&limit=1")
path = f"{folder}/fda_{n + 1:05d}.json"

with open(path, "w") as f:
    f.write(r.text)

dbutils.notebook.exit(path)