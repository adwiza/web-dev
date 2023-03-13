#!/usr/bin/env python
# coding: utf-8

# In[1]:


import joblib
import re
import string

import numpy as np
import pandas as pd

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, classification_report
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.naive_bayes import MultinomialNB

# In[2]:


# categories = [
#     "alt.atheism",
#     "misc.forsale",
#     "sci.space",
#     "soc.religion.christian",
#     "talk.politics.guns",
# ]

categories = [
    "hasBadWords.True",
    "hasBadWords.False",
]

news_group_data = pd.read_json('datasets/dataset.json')  # dataset.json
news_group_data['target'] = news_group_data.hasBadWords.apply(
    lambda x: "hasBadWords.True" if x is True else "hasBadWords.False")
# news_group_data.drop(['violation'], axis=1, inplace=True)
news_group_data.shape

# news_group_data = fetch_20newsgroups(
#     subset="all", remove=("headers", "footers", "quotes"), categories=categories
# )

# df = pd.DataFrame(
#     dict(
#         text=news_group_data["text"],
#         target=news_group_data["target"]
#     )
# )
# df["target"] = df.target.map(lambda x: categories[x])


# In[3]:


df = pd.DataFrame(
    dict(
        text=news_group_data["text"],
        target=news_group_data["target"]
    )
)

df.head()


def process_text(text):
    text = str(text).lower()
    text = re.sub(
        f"[{re.escape(string.punctuation)}]", " ", text
    )
    text = " ".join(text.split())
    return text


df["clean_text"] = df.text.map(process_text)


df.head()


df_train, df_test = train_test_split(df, test_size=0.20, stratify=df.target, shuffle=True)


vec = CountVectorizer(
    ngram_range=(1, 3),
    stop_words="english",
)

X_train = vec.fit_transform(df_train.clean_text)
X_test = vec.transform(df_test.clean_text)

y_train = df_train.target
y_test = df_test.target


nb = MultinomialNB()
nb.fit(X_train, y_train)

preds = nb.predict(X_test)
print(classification_report(y_test, preds))

joblib.dump(nb, "nb.joblib")
joblib.dump(vec, "vec.joblib")

nb_saved = joblib.load("nb.joblib")
vec_saved = joblib.load("vec.joblib")

# sample_text = ["Space, Stars, Planets and Astronomy!"]
sample_text = [
    "SISSY TRAINING, STRAPON SUCKING,BLOWJOB TRAINING, ANAL, TRANSGENDER EDUCATION, HUMILIATION SMOKING, MAKEUP"]
clean_sample_text = process_text(sample_text)
sample_vec = vec_saved.transform(sample_text)
nb_saved.predict(sample_vec)
