import json
import pandas as pd
from pymongo import MongoClient


def loadData(path):
    df_data = pd.read_csv(path, sep='\t')
    json_data = json.loads(df_data.to_json(orient='records', indent=4))
    uri = "mongodb://root:example@localhost:27017/"
    client = MongoClient(uri)
    database = client["cars"]
    collection = database["updates"]
    if isinstance(json_data, list):
        collection.insert_many(json_data)
    else:
        collection.insert_one(json_data)
    print(collection.find_one())


if __name__ == '__main__':
    loadData('../Caso5.txt')
