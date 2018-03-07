# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 18:00:23 2017

@author: Atul
"""

#from os import chdir
#chdir("D:/Projects/guardian")
import pandas as pd
from elasticsearch import Elasticsearch
import dataPrep
from gensim.models import word2vec
from gensim import corpora
import numpy as np
from sklearn.manifold import TSNE
import logging
from bokeh.plotting import figure, output_file , show
from bokeh.models import HoverTool, ColumnDataSource
from collections import OrderedDict

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
    level=logging.INFO)

es = Elasticsearch(['localhost'],port=9200) #,http_auth=('elastic','theguardian'))



search_res = es.search(index = 'guardian', size=5100,
                       #timeout=30,
                       body={"query": { "bool":{
                               "must":{
                               "match": {"sectionName": "Football"}}}
                        }
                        })
#search_res['hits']['hits'][0]['_source']['fields']['bodyText']

articles = pd.DataFrame(columns=['articles'])
articles.articles = [hit['_source']['fields']['bodyText'] for hit in search_res['hits']['hits']]
#del search_res

articles = dataPrep.clean_text(articles, col='articles', remove_unusual=False,
                                    remove_stopwords=True,
                                    remove_numbers=True, stem_words=False,
                                    lemmatize=True, nGram=True)


# Set values for various parameters
num_features = 100    # Word vector dimensionality                      
min_word_count = 20   # Minimum word count                        
num_workers = 4       # Number of threads to run in parallel
context = 10          # Context window size                                                                                    
downsampling = 1e-3   # Downsample setting for frequent words

# Initialize and train the model (this will take some time)
model = word2vec.Word2Vec(articles.articles, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)

model.init_sims(replace=True)

fname = "wv_guardian_football"
#model.save(fname)
#model = word2vec.Word2Vec.load(fname)


# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(list(articles.articles))
dictionary.filter_extremes(no_below=20, no_above=0.5)
dictionary.compactify()
fname = "dict_guardian_football"
dictionary.save(fname)
#dictionary = corpora.Dictionary.load(fname)

keys = [x.replace('_',' ') for x in dictionary.token2id]

def getVal(model,k,dim=100):
    """ here model is a word2vec model and 
    dim is the number of dimensions of each word """
    try:
        return model[k]
    except: KeyError
    return np.zeros(dim)


X = np.vstack([getVal(model,k) for k in keys])
X = [a for a in X if any(a)!=0]

#a = X.sum(axis=1)
#sum([1 for x in a if x==0])
#len(a)

RS = 20180108
tsne = TSNE(n_components=2, perplexity=30.0, random_state=RS)
words_proj = tsne.fit_transform(X)


words = pd.DataFrame()
# Select the 0th feature: x
words['x'] = words_proj[:,0]
# Select the 1th feature: y
words['y'] = words_proj[:,1]
words['labels'] = [k for k in keys if any(getVal(model,k))!=0]
#words.set_index('labels',inplace=True,drop=True)


TOOLS="pan,wheel_zoom,box_zoom,reset,hover,previewsave"
p = figure(title="The Guardian - Words",plot_width=900, plot_height=900,tools=TOOLS)
source = ColumnDataSource(words)

p.circle('x', 'y',source=source, fill_alpha=0.2, size=10)

hover =p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ("(xx,yy)", "(@x, @y)"),
    ("label", "@labels"),
])

output_file("theguardianfootballwords.html", title="The Guardian - Football")
show(p)
