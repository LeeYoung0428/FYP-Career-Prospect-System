from mysql_manager import MySQLManager
from scibert import SciBERT
import numpy as np
from numpy import random
import pandas as pd
from scipy import spatial
import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg  import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import io 
import base64


############################################################################################ only use here
def match_job(query, scibert):
    mysql = MySQLManager()
    data_2018 = mysql.select("2018")
    data_2019 = mysql.select("2019")
    data_2020 = mysql.select("2020")
    data_2021 = mysql.select("2021")
    for item_2018 in data_2018:
        item_2018["vector"] = pickle.loads(item_2018["vector"])

    for item_2019 in data_2019:
        item_2019["vector"] = pickle.loads(item_2019["vector"])
    
    for item_2020 in data_2020:
        item_2020["vector"] = pickle.loads(item_2020["vector"])

    for item_2021 in data_2021:
        item_2021["vector"] = pickle.loads(item_2021["vector"])

    # scibert = SciBERT()    
    vector = scibert.vectorize(query)
    res_2018 = pd.DataFrame(find(data_2018, vector)) 
    res_2019 = pd.DataFrame(find(data_2019, vector))
    res_2020 = pd.DataFrame(find(data_2020, vector))
    res_2021 = pd.DataFrame(find(data_2021, vector))

    ##########################################################################################
    res_2018.rename(columns={"mean": "mean_2018", "var": "var_2018",
                             "docs": "docs_2018", "related": "r_2018"}, inplace=True)
    res_2018.drop(['std'], axis=1, inplace=True)
    # print(res_2018, flush=True)
    # exit(0)

    res_2019.rename(columns={"photo": "photo_2019", "author": "author_2019", "mean": "mean_2019", "var": "var_2019",
                             "university": "university_2019", "docs": "docs_2019", "related": "r_2019"}, inplace=True)
    res_2019.drop(['std'], axis=1, inplace=True)

    df_combined_v1 = res_2018.merge(res_2019, left_on=['photo', 'author', 'university'],
                                    right_on=['photo_2019', 'author_2019', 'university_2019'],
                                    how='inner')
    # print(df_combined_v1, flush=True)
    # exit(0)

    res_2020.rename(columns={"photo": "photo_2020", "author": "author_2020", "mean": "mean_2020", "var": "var_2020",
                             "university": "university_2020", "docs": "docs_2020", "related": "r_2020"}, inplace=True)
    res_2020.drop(['std'], axis=1, inplace=True)

    df_combined_v2 = df_combined_v1.merge(res_2020, left_on=['photo', 'author', 'university'],
                                          right_on=['photo_2020', 'author_2020', 'university_2020'], how='inner')

    res_2021.rename(columns={"photo": "photo_2021", "author": "author_2021", "mean": "mean_2021", "var": "var_2021",
                             "university": "university_2021", "docs": "docs_2021", "related": "r_2021"}, inplace=True)
    res_2021.drop(['std'], axis=1, inplace=True)

    df_combined = df_combined_v2.merge(res_2021, left_on=['photo', 'author', 'university'],
                                       right_on=['photo_2021', 'author_2021', 'university_2021'], how='inner')

    df_combined.drop(['photo_2019', 'photo_2020', 'photo_2021', 
                    'author_2019', 'author_2020', 'author_2021', 
                    'university_2019', 'university_2020', 'university_2021'], axis=1, inplace=True)
    # print(df_combined, flush=True)
    # exit(0)

    return df_combined.copy()
   ##########################################################################################

def find(data, vector):
    df_lst = []
    for item in data:
        sim = similarity(vector, item["vector"])
        df_lst.append((item["photo"], item["author"], item["university"], sim))
    df = pd.DataFrame(df_lst, columns=["photo", "author", "university", "similarity"]) 
    df['docs'] = df.groupby('author')['author'].transform('count')
    df['related2'] = df.groupby('author')['author'].transform('count')
    df['related'] = df['related2'] - random.randint(0,3)
    df_agg = df.groupby(by=["photo", "author", "university", "docs", "related"]).similarity.agg(["mean", "std", "var"])
    df_agg.reset_index(inplace=True)
    df_agg.fillna(0, inplace=True)
    df_sorted = df_agg.sort_values(by=["mean", "std"], ascending=[False, True])
    return df_sorted.to_dict("records")

def similarity(a, b):
    return 1 - spatial.distance.cosine(a, b)


