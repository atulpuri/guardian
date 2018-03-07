# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 19:23:11 2017

@author: Atul


retrieves date of most recent update

returns date from then to yesterday
"""

from os import listdir, remove
from datetime import datetime, date, timedelta
import json

def get_last_updated():
    articles = [datetime.strptime(x.split(".")[0], "%Y-%m-%d") for x in listdir('articles') if x.endswith(".json")]
    articles.sort(reverse=True)
    
    last = articles[0]
    return date(last.year, last.month, last.day)

def get_settings(d=True):
    if d:
        with open("settings/settings.json","r") as f:
            settings = json.load(f)
    else:
        with open("settings/settings_u.json","r") as f:
            settings = json.load(f)
    
    # get start date and coerce to date
    if settings["from"] == "last updated":
        start_date = get_last_updated()
    elif isinstance(settings["from"], dict):
        start_date = date(settings['from']['year'], settings['from']['month'], settings['from']['day'])

    # get end date and coerce to date    
    if settings["to"] == "yesterday":
        yest = datetime.now() - timedelta(days=1)
        end_date = date(yest.year, yest.month, yest.day)
    elif isinstance(settings["to"], dict):
        end_date = date(settings['to']['year'], settings['to']['month'], settings['to']['day'])
    
    if d:
        date2dict = lambda x: {'year':x.year, 'month':x.month, 'day':x.day}
        with open("settings/settings_u.json","w") as f:
            f.write(json.dumps({"from": date2dict(start_date), "to":date2dict(end_date)}, indent=2))
    else:
        remove("settings/settings_u.json")
    return start_date, end_date