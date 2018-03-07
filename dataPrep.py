# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 13:29:37 2017

@author: 584815
"""
import pandas as pd
#import email
import re
from nltk.corpus import stopwords
from nltk.corpus import words as wordList
from nltk.corpus import names
#from sys import path
#path.append('D:\Python\smart_open-master')
#path.append('D:\Python\gensim-develop')
from gensim.parsing.preprocessing import STOPWORDS as sw
from gensim.models import phrases 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import PorterStemmer
from nltk.tokenize import word_tokenize

""" data cleaning """
# Find number of unique values in each columns 
# and drop the ones with too few values
def drop_cols(df,cutOff=10):
    counter = 0
    toDrop = []
    for col in df.columns:
        print(counter,col, df[col].nunique())
        if df[col].nunique()<cutOff :
            toDrop.append(counter)
        counter+=1
    print(toDrop)
    # dropping columns with too few values
    df.drop(df.columns[toDrop],axis=1,inplace=True)
    return df

# Returns a set of stopwords from nltk and gensim
def stopWords():
    return set(stopwords.words('english') + [w for w in sw])

def usualWords():
    return set(w.lower() for w in wordList.words()+names.words('male.txt')+names.words('female.txt'))

def tokenize(review, remove_numbers=False):
    if remove_numbers :
        step1 = re.sub("[^a-zA-Z\'_]"," ",review)
    else:
        step1 = re.sub("[^a-zA-Z0-9\'_]"," ",review)
    step2 = step1.lower()
    # dealing with contractions
    step2 = re.sub("\'s","",step2)
    step2 = re.sub("n\'t"," not",step2)
    step2 = re.sub("\'ve"," have",step2)
    step2 = re.sub("\'ll"," will",step2)
    step2 = re.sub("\'re"," are",step2)
    step2 = re.sub("\'d"," would",step2)
    step2 = re.sub("\'","",step2)
    #to_words = re.split(r'\W+',step2)
    to_words = word_tokenize(step2)
    return to_words

# Define a function to clean mails so it may be repeatedly used 
def text_to_words(text,remove_numbers=True,stem_words=False,lemmatize=True):
    to_words = tokenize(text,remove_numbers)
    while('' in to_words):
        to_words.remove('')
    if lemmatize:
        # Lemmatize all words in documents.
        lemmatizer = WordNetLemmatizer()
        to_words = [lemmatizer.lemmatize(w) for w in to_words]
    if stem_words:
        porter = PorterStemmer()
        to_words = [porter.stem(w) for w in to_words]
    return to_words

def remove_words(text,remove_unusual=False,remove_stopwords=False,stop_words=stopWords(),usualWords=[]):
    if remove_stopwords :
        # removes stopwords and words with only 1 unique letter
        text = [w for w in text if not w in stop_words if not (len(set(w))<=2) if len(w)>=3]
    if remove_unusual:
        # remove words not in nltk
        text = [w for w in text if w in usualWords]
    return text


def clean_text(df_input,col='content',remove_unusual=False,remove_stopwords=False,toRemove=[],remove_numbers=False,stem_words=False,lemmatize=False,nGram=False):
    # Clean mails
    if remove_stopwords:
        toRemove.extend(stopWords())
    usual_words = []
    if remove_unusual:
        usual_words = usualWords()
    ## Clean content of mails
    # tokenization and lemmatization/stemming
    df_input[col] = df_input[col].map(lambda x: text_to_words(x,remove_numbers,stem_words,lemmatize))
    # removing stopwords and unusual words
    df_input[col] = df_input[col].map(lambda x: remove_words(x,remove_unusual,remove_stopwords,toRemove,usual_words))
    # bigrams and trigrams
    if nGram:
        phrase = phrases.Phrases(df_input[col],min_count=30, threshold=300)
        bigram = phrases.Phraser(phrase)
        trigram = phrases.Phrases(bigram[df_input[col]])
        df_input[col] = [trigram[bigram[sent]] for sent in df_input[col]]

    print("data cleaned")
    return df_input


""" To Do:
        Add functionality to get Cc and Bcc from emails
"""