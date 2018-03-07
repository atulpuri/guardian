# guardian

## Overview

This repository contains my experiments with news articles from The Guardian...

## Contents
* Data Collection 
* Topic Modelling 
* Word2Vec Experiment
* Utilities

### Data Collection

The articles were collected using the The Guardian's API whose reference can be found at: 
http://open-platform.theguardian.com/documentation/

Files | Requires
---- | ----
guardian_download.py | utils.py
guardian_upload.py | settings/guardian_creds.json
NA | settings/settings.json


### Topic Modelling

Files | Requires | Outputs
---- | ---- | ----
guardian_topic_modelling.py | dataprep.py | football_lda40.html
NA | NA | world_lda40.html

### Word2Vec Experiment

Files | Requires | Outputs
---- | ---- | ----
guardian_wv.py | dataprep.py | theguardianfootballwords.html
