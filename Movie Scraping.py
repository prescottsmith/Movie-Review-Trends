import imdb_collect
import rt_collect
import mc_collect

import pandas as pd


#Scrape IMDB
df_imdb = imdb_collect.scrape()

#Scrape Rotten Tomatoes
df_rt = rt_collect.scrape()

#Scrape Metacritic
df_mc = mc_collect.scrape()



