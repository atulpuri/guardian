from os import path
from elasticsearch import Elasticsearch
import json
import time
from datetime import timedelta
import utils

es = Elasticsearch(['localhost'],port=9200)

meta = { "index" : { "_index" : "guardian", "_type" : "articles" } }
res = []
success = []
unsuccess = []
file_names = []

## to upload recently downloaded files
start_date, end_date = utils.get_settings(False)

dayrange = range((end_date - start_date).days + 1)
for daycount in dayrange:
    dt = start_date + timedelta(days=daycount)
    datestr = dt.strftime('%Y-%m-%d')
    file_names.append(datestr + '.json')
    #print(datestr)
    
    
for file_name in file_names:
    if file_name.endswith(".json"):
        try:
            with open(path.join("articles",file_name)) as day:
                temp = sum([[meta,x] for x in json.load(day)],[])
                #print("checkpoint 1")
                res.append(
                    es.bulk(index = 'guardian', body = temp, refresh = True)
                )
                #print("checkpoint 2")
            print("{}".format(file_name.split(".")[0]))
            success.append(file_name)
        except:
            print("{} unsuccessful".format(file_name.split(".")[0]))
            unsuccess.append(file_name)
    time.sleep(2.5)
