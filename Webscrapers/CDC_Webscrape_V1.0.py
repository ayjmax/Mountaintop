import requests
import json
import pandas as pd
import csv
from pathlib import Path
from os import chdir, getcwd
from sodapy import Socrata

#Socrata API hosts various government data
Socrata_url = "https://api.us.socrata.com/api/catalog/v1?names={}&domains=chronicdata.cdc.gov"
formats = {"Census": "Ce", "County": "Co", "ZTCA": "ZTCA"}
categories = ["CASTHMA", "RISKBEH", "PREVENT"]
years = [2021, 2020] #add more when necessary

#Change work directory as necessary
work_dir = "C:/Mountaintop" #Change if needed
if (getcwd() != work_dir):
    chdir(work_dir)

def getData(ID, form, year):
    #Check if file dir exists; if not, create new dir
    base_dir = f"{work_dir}/Raw_Data/API_PLACES_Files/{year}/{form}"
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    
    client = Socrata("chronicdata.cdc.gov", None)
    results_casthma = client.get(ID, stateabbr="PA", measureid="CASTHMA", limit=10000)
    results_riskbeh = client.get(ID, stateabbr="PA", categoryid="RISKBEH", limit=10000)
    results_prevent = client.get(ID, stateabbr="PA", categoryid="PREVENT", limit=10000)

    abbr = formats[form]
    df = pd.DataFrame.from_records(results_casthma)
    df.to_csv(f"{base_dir}/Raw_PLACES_{abbr}_CASTHMA_{year}.csv", index=False)

    df = pd.DataFrame.from_records(results_riskbeh)
    df.to_csv(f"{base_dir}/Raw_PLACES_{abbr}_RISKBEH_{year}.csv", index=False)

    df = pd.DataFrame.from_records(results_prevent)
    df.to_csv(f"{base_dir}/Raw_PLACES_{abbr}_PREVENT_{year}.csv", index=False)


for form in formats:
    for year in years:
        title = f"PLACES: Local Data for Better Health, Census Tract Data {year} release"
        response = requests.get(Socrata_url.format(title))

        if (response.status_code == 200):
            print('API responded')
            data = response.text
            parsed_json = json.loads(data)
            ID = parsed_json['results'][0]['resource']['id']
            getData(ID, form, str(year))
        else:
            print('ERROR')
            exit(1)