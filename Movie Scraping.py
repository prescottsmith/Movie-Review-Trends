import imdb_collect
import rt_collect
import mc_collect
import movie_cleaning
import matplotlib as plt
import seaborn as sns
import pandas as pd

df_imdb = (pd.read_csv('imdb_chart.csv').copy())
df_rt = (pd.read_csv('rt_chart.csv').copy())
df_mc = (pd.read_csv('mc_chart.csv').copy())

#Scrape IMDB
#df_imdb = imdb_collect.scrape()

#Scrape Rotten Tomatoes
#df_rt = rt_collect.scrape()

#Scrape Metacritic
#df_mc = mc_collect.scrape()

df_imdb_clean = movie_cleaning.clean(df_imdb.copy())
df_rt_clean = movie_cleaning.clean(df_rt.copy())
df_mc_clean = movie_cleaning.clean(df_mc.copy())

df_mc_clean['Source'] = 'Metacritic'
df_rt_clean['Source'] = 'Rotten Tomatoes'
df_imdb_clean['Source'] = 'IMDB'

#Columns need units

megaframe = df_imdb_clean.append(df_rt_clean.append(df_mc_clean))

