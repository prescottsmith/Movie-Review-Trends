from cleaning import movie_cleaning
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from plotnine import *

wide_data = pd.read_csv('Data/imdb_final_wide.csv')

##### Genre graphing

#Genres quantity
decades = [1980, 1990, 2000, 2010]
genre_values = []
for genre in all_genres:
    genre_values.append(wide_data[genre].sum())

g_av_ratings = []
for genre in all_genres:
    frame = wide_data[wide_data[genre]==True]
    g_avg = frame['IMDB_Rating'].mean()
    g_av_ratings.append(g_avg)

# Making Genre DF
genres_dict={'Genre':all_genres, 'Quantity':genre_values, 'Avg_Rating':g_av_ratings}

genre_df=pd.DataFrame(genres_dict)

# Genre histogram
fig, ax = plt.subplots()
plt.bar(all_genres, genre_values)
plt.xticks(rotation=90)
plt.show()

# Genre ratings
fig, ax = plt.subplots()
graph = sns.barplot(data=genre_df, x='Genre', y='Avg_Rating')
graph.set_xticklabels(ax.get_xticklabels(), rotation=65)
plt.show()


# Decade averages - doesnt work
fig, ax = plt.subplots()
graph = sns.barplot(data=wide_data, x='Decade', y=data['IMDB_Rating'].mean())
graph.set_xticklabels(ax.get_xticklabels(), rotation=65)
plt.show()


#Runtime Ratings
runtime_data = wide_data[wide_data['Runtime']>0]

    #IMDB
graph = sns.scatterplot(data=runtime_data, x='Runtime', y='IMDB_Rating')
plt.show()
    #Metascore
graph = sns.scatterplot(data=runtime_data[runtime_data['Metascore (*)']>0], x='Runtime', y='Metascore (*)')
plt.show()



longest_movie = data[data['Runtime']==data['Runtime'].max()]
print(longest_movie['Title'] + ' ' + str(longest_movie['Runtime']) + 'mins')