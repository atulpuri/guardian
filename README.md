# guardian

## Overview

This repository contains my experiments with news articles from The Guardian...

I've been looking for a dataset to explore for a while now and this one seemed perfectly suitable to my needs and areas of interest.
That being said, my exploration deals primarily with the articles from the _World_ and _Football_ sections. The articles span from 1/1/2015 to my latest update (which is usually once in a week).

In my experiments, I've tried to identify the major themes governing the published articles in these sections using Topic Modelling.
Future work includes identification of Named Entities and relations between them.

## Contents
* Data Collection 
* Topic Modelling 
* Word2Vec Experiment
* Utilities

### Data Collection

| File | Requires |
| ---- | ---- |
| guardian_download.py | utils.py |
| guardian_upload.py | settings/guardian_creds.json |
|   | settings/settings.json |

The articles were collected using the The Guardian's API whose reference can be found at: 
http://open-platform.theguardian.com/documentation/

The script guardian_download.py downloads all articles for all dates within the given date range.
Input should be given in the form of a json:
{
  'from' : {
    'year' : x,
    'month' : x,
    'day' : x
    },
  'to' : {...}
}
Keywords such as 'last updated' and 'yesterday' can also be used.

Initially stored as JSON files (folder named _articles_), they were then indexed and uploaded to Elasticsearch in order to analyze them using Kibana.

### Word2Vec Experiment

| File | Requires | 
| ---- | ---- |
| guardian_wv.py | dataprep.py | 

| Output | Section |
| ---- | ---- |
| theguardianfootballwords.html | Football |

...

### Topic Modelling

| File | Requires |
| ---- | ---- |
| guardian_topic_modelling.py | dataprep.py |
|   |   |

| Output | Comments | Section |
| ---- | ---- | ---- |
| football_lda40.html | football_lda40.csv (TBD) | Football |
| world_lda40.html | world_lda40.csv (TBD) | World |

I used Topic Modelling to attempt to identify the underlying themes of the articles of the two sections. To do so, I extracted 40 topics from each section and they can be seen their respective pyLDAvis visualizations. 
For each of the sections, most topics seemed quite satisfactory, as in they were clearly distinguishable and my comments on each of the topics can be found in their respective csv files.
The overlap amongst topics was also an interesting phenomenon to observe as it added a perspective of similarity between the topics.

### Utilities

| File | Purpose |
| ---- | ----|
| dataprep.py | Text cleaning and preprocessing |
| utils.py | Utility functions required during data download/upload |
| settings.json | Preset settings of dates for dowload |
| guardian_creds.json | Stores API key |
| settings_u.json | Temp file storing settings of dates for upload |
