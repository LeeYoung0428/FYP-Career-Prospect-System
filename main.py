from mysql_manager import MySQLManager
import pandas as pd
from scipy import spatial
import pickle
from matplotlib.backends.backend_agg  import FigureCanvasAgg as FigureCanvas
import seaborn as sns

id = 1
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
    # print(df_combined.dtypes)
    #############################################################################
    # concat the dataframes of the top publications in 1 dataframe
    # then sort them depening on similarity from the highest to the lowest
    publications_2018 = publications_arrange(data_2018, vector)
    publications_2019 = publications_arrange(data_2019, vector)
    publications_2020 = publications_arrange(data_2020, vector)
    publications_2021 = publications_arrange(data_2021, vector)
    publications = pd.concat([publications_2018, publications_2019, publications_2020, publications_2021],
                            ignore_index= True)
    publications = publications.sort_values(by=["author", "similarity"], ascending=[True, False])
    print(publications.dtypes)
    print(publications.head())
    return df_combined.copy(), publications.copy()
   ##########################################################################################

def find(data, vector):
    df_lst = []
    for item in data:
        sim = similarity(vector, item["vector"])
        df_lst.append((item["photo"], item["author"], item["university"], sim))
    df = pd.DataFrame(df_lst, columns=["photo", "author", "university", "similarity"]) 
    df['docs']   = df.groupby('author')['author'].transform('count')
    
    # the method 'query' used as a boolean index, it just select the rows with similarity bigger than 0.5 for each author
    # then i used transform('count') to count how many have been selected
    df["related"] =  df.query("similarity >= 0.55").groupby('author')['author'].transform('count')

    # i just copy the value i got from the previous code and past it in other empty cells for each cell
    # that helps each author has his own related value in all his rows
    # which helps for grouping the rows by "photo", "author", "university", "docs", "related"
    df["related"] =  df['related'].fillna(df.groupby('author')['related'].transform('count'))
    df["related"].astype(int)
    df_agg = df.groupby(by=["photo", "author", "university", "docs", "related"]).similarity.agg(["mean", "std", "var"])
    df_agg.reset_index(inplace=True)
    df_agg.fillna(0, inplace=True)
    df_sorted = df_agg.sort_values(by=["mean", "std"], ascending=[False, True])
    return df_sorted.to_dict("records")

# arrange the publication and sort them starting by the highest avg sim of each author
# that helps to get the highest top 3 publications of each by picking just the first 3 publications
def publications_arrange(data, vector):
    df_lst = []
    global id
    for item in data:
        sim = similarity(vector, item["vector"])
        item["id"] = id
        id += 1
        df_lst.append((item["id"], item["author"], item["title"],item["abstract"],item["link"], sim))
    df = pd.DataFrame(df_lst, columns=["id", "author", "title","abstract", "link", "similarity"]) 
    df.fillna(0, inplace=True)
    df_sorted = df.sort_values(by=["author", "similarity"], ascending=[True, False])
    return df_sorted

def similarity(a, b):
    return 1 - spatial.distance.cosine(a, b)


