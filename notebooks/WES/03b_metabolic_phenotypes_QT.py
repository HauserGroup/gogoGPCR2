# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import re
import subprocess

import dxdata
import dxpy
import pyspark

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession

from pathlib import Path
from src.phenotypes import get_age_sex, get_pheno_fields, concatenate, new_names

Path("../tmp").resolve().mkdir(parents=True, exist_ok=True)

trait = "metabolic"

# %%
conf = SparkConf()
# conf.set("autoBroadcastJoinThreshold", -1) # TODO: Check or remove

sc = pyspark.SparkContext()
spark = SparkSession(sc)

dispensed_database_name = dxpy.find_one_data_object(
    classname="database", name="app*", folder="/", name_mode="glob", describe=True
)["describe"]["name"]
dispensed_dataset_id = dxpy.find_one_data_object(
    typename="Dataset", name="app*.dataset", folder="/", name_mode="glob"
)["id"]

spark.sql("USE " + dispensed_database_name)

dataset = dxdata.load_dataset(id=dispensed_dataset_id)  # type: ignore
participant = dataset["participant"]

# %%
age_sex_fields = get_age_sex(participant, fields=["31", "21022"])

metabolic_fields = get_pheno_fields(
    participant,
    fields=[
        "21002",
        "50",
        "48",
        "21001",
        "23099",
        "23127",
        "102",
        "4080",
        "4079",
    ],
)

field_names = concatenate(["eid"], age_sex_fields, metabolic_fields)

df = participant.retrieve_fields(names=field_names, engine=dxdata.connect())  # type: ignore

# %%
# drop arrays
to_drop = [x for x in df.columns if "a1" in x]
df = df.drop(*to_drop)
colnames = [re.sub("_a\d", "", x) for x in df.columns]
colnames = ["xeid"] + [new_names(s) for s in colnames[1:]]
print(colnames[:10])

# %%
df = df.toDF(*colnames)

# %%
df.write.csv("/tmp/phenos.tsv", sep="\t", header=True, emptyValue="NA")

# %%
subprocess.run(
    ["hadoop", "fs", "-rm", "/tmp/phenos.tsv/_SUCCESS"], check=True, shell=False
)
subprocess.run(
    ["hadoop", "fs", "-get", "/tmp/phenos.tsv", "../tmp/phenos.tsv"],
    check=True,
    shell=False,
)

# %%
# !sed -e '3,${/^xeid/d' -e '}' ../tmp/phenos.tsv/part* > ../tmp/metabolic.QT.raw.tsv

# %%
# Upload to project

subprocess.run(
    ["dx", "upload", "../tmp/metabolic.QT.raw.tsv", "--path", "Data/phenotypes/"],
    check=True,
    shell=False,
)

# %%
