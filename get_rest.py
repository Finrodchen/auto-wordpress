import json 
from requests import Request, Session
import pandas as pd

url = "https://data.tycg.gov.tw/opendata/datalist/datasetMeta/download?id=8dc035f1-0770-4522-8c98-96d98bb0530e&rid=9f126a52-5bea-41ff-a769-96b0f1df0f51"
session = Session()

response = session.get(url)
results = json.loads(response.text)

df = pd.DataFrame.from_dict(results["infos"])

df.to_csv(f"./data/rest_list.csv", encoding = "utf_8_sig")

