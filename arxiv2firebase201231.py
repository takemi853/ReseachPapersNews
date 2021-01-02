#firebaseのインポート部分
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# from firebase_admin import db

cred = credentials.Certificate('./composite-sun-297508-firebase-adminsdk-bcgyh-21f2ee2ae2.json')

firebase_admin.initialize_app(cred)
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://composite-sun-297508-default-rtdb.firebaseio.com/',
#     'databaseAuthVariableOverride': {
#         'uid': 'my-service-worker'
#     }
# })
######################
#転送# (翻訳+原文)
#####################
import pprint
import arxiv
import pandas as pd
import numpy as np
from tqdm import tqdm
 
from datetime import datetime
import re
import requests
from googletrans import Translator
from time import sleep
 
import arxiv

# category = ["AI","CL","CC","CE","CG","GT","CV","CY","CR","DS",
#             "DB","DL","DM","DC","ET","FL","GL","GR","AR","HC",
#             "IR","IT","LO","LG","MA","MS","MM","NI","NE","NA",
#             "OS","OH","PF","PL","RO","SI","SE","SD","SC","SY"]
QUERY = "cs.AI"
# QUERY = "cs.AI OR cs.CV"
# for i in category:
#     QUERY += "OR cs.{}".format(i)

dt = datetime.now().strftime("%Y%m%d")
# dt = str(int(dt)-1)
dt=str(20201228) #デバック用(ここは2020というように4桁表示)
print(str(int(dt)))
tr = Translator(service_urls=['translate.googleapis.com'])
result_list = arxiv.query(query = 'cat:{} AND submittedDate:[{}000001 TO {}235959]'.format(QUERY,dt,dt),max_results=50,sort_by='submittedDate')


#databaseに初期データを追加する(firebase)
arxiv_ref = db.reference('arxiv-test')

def translate(text):
    tr = Translator(service_urls=['translate.googleapis.com'])
    while True:
        try:
            text_ja = tr.translate(text,src="en", dest="ja").text
            return text_ja
            break
        except Exception as e:
            tr = Translator(service_urls=['translate.googleapis.com'])

def translate_post(df):
    title_jpn = translate(title)
    abst_jpn = translate(abst)
    print("-------"+str(count)+"ページ目-------")
    print("author:{}".format(author))
    print(url)
    print("title:{}".format(title_jpn))
    print("date:{}".format(date))
    print("Abstract:{}".format(abst_jpn))
    print("Category:{}".format(cat))
    print(df.iloc[1,1])

    arxiv_ref.child(title).set({
    "title_jpn":title_jpn,
    "author":author,
    "cat":cat,
    "url":url,
    "abst_jpn":abst_jpn,
    "abst":abst,
    "date":date,
    "hotword":{
        "1":{
            "keyword":df.iloc[8,1],
            "value":df.iloc[8,2]
        },
        "2":{
            "keyword":df.iloc[9,1],
            "value":df.iloc[9,2]
        },
        "3":{
            "keyword":df.iloc[10,1],
            "value":df.iloc[10,2]
        },
        "4":{
            "keyword":df.iloc[11,1],
            "value":df.iloc[11,2]
        },
        "5":{
            "keyword":df.iloc[12,1],
            "value":df.iloc[12,2]
        },
        "6":{
            "keyword":df.iloc[13,1],
            "value":df.iloc[13,2]
        },
        "7":{
            "keyword":df.iloc[14,1],
            "value":df.iloc[14,2]
        },
        "8":{
            "keyword":df.iloc[15,1],
            "value":df.iloc[15,2]
        },
        "9":{
            "keyword":df.iloc[16,1],
            "value":df.iloc[16,2]
        },
        "10":{
            "keyword":df.iloc[17,1],
            "value":df.iloc[17,2]
        }
      }
    })
    sleep(20)

count = 1

def pickupHotword(doc):
    docs = []
    docs.append(doc)
    df = pd.DataFrame(columns=['category_id', 'name', 'tf-idf'])
    #参考　https://tex2e.github.io/blog/python/tf-idf　より
    #参考：TF-IDFを用いた「Kaggle流行語大賞2020」https://upura.hatenablog.com/entry/2020/12/08/234045
    from sklearn.feature_extraction.text import TfidfVectorizer
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords


    stopWords = stopwords.words("english")
    stopWordsAdd = ['data', 'devices','device','accuracy', 'ai','model','framework',
                    'without','due','also','base','based'
                    'simple', 'ashrae', 'ieee',
                    'using', 'prediction', 'ml', 'classification', 'regression',
                    'machine', 'learning', 'exercise', 'detection', 'kernel', 'dataset']

    for sw in stopWordsAdd:
        stopWords.append(sw)

    vectorizer = TfidfVectorizer(stop_words=stopWords)
    # vectorizer = TfidfVectorizer(max_df=0.9,ngram_range=(1,5)) # tf-idfの計算
    #                            ^ 文書全体の90%以上で出現する単語は無視する
    X = vectorizer.fit_transform(docs)
    # print('feature_names:', vectorizer.get_feature_names())

    words = vectorizer.get_feature_names()
    for doc_id, vec in zip(range(len(docs)), X.toarray()):
        print('doc_id:', doc_id)
        for w_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True):
            lemma = words[w_id]
            df = df.append({'category_id': doc_id, 'name': lemma, 'tf-idf': round(tfidf,3)}, ignore_index=True)
            # print('\t{0:s}: {1:f}'.format(lemma, tfidf))
    return df



for result in result_list:
    author = result.author
    url = result.pdf_url
    title = result.title
    date = result.published[0:10]
    abst = result.summary
    cat = result.category
 
    abst = abst.replace("\n","")
    df = pickupHotword(abst)
    translate_post(df) 
    count += 1     
print("Done")
