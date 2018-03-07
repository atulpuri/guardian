# guardian

## Overview

This repository contains my experiments with news articles from The Guardian...

## Contents
* Data Collection 
* Topic Modelling 
* Word2Vec Experiment
* Utilities

### Data Collection

The articles were collected using the The Guardian's API whose reference can be found at: http://open-platform.theguardian.com/documentation/

Files: 
1. guardian_download.py
2. guardian_upload.py

Requires: 
1. utils.py
2. settings/guardian_creds.json
3. settings/settings.json

### Topic Modelling

Files:
1. guardian_topic_modelling.py

Requires:
1. dataprep.py

Outputs:
1. football_lda40.html
2. world_lda40.py

### Word2Vec Experiment

Files:
1. guardian_wv.py

Requires:
1. dataprep.py

Output:
1. theguardianfootballwords.html
