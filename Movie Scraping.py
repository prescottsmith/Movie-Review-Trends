import imdb_collect
import rt_collect
import mc_collect
import movie_cleaning
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from string import ascii_letters

sns.set(style="white")

df_imdb = (pd.read_csv('imdb_chart.csv').copy())
df_rt = (pd.read_csv('rt_chart.csv').copy())
df_mc = (pd.read_csv('mc_chart.csv').copy())

#Scrape IMDB
#df_imdb = imdb_collect.scrape()

#Scrape Rotten Tomatoes
#df_rt = rt_collect.scrape()

#Scrape Metacritic
#df_mc = mc_collect.scrape()

#cleaning and simplifying dataframes
df_imdb_clean = movie_cleaning.clean(df_imdb.copy())
df_rt_clean = movie_cleaning.clean(df_rt.copy())
df_mc_clean = movie_cleaning.clean(df_mc.copy())

df_mc_clean['Source'] = 'Metacritic'
df_rt_clean['Source'] = 'Rotten Tomatoes'
df_imdb_clean['Source'] = 'IMDB'

mc = df_mc_clean
rt = df_rt_clean
imdb = df_imdb_clean[0:100]

### widening the genres layout
def genre_list(df):
    list = []
    for index in range(len(df)):
        genres = df['Genre'][index]
        for items in genres:
            if items in list:
                continue
            list.append(items)
    return list

imdb_genres = genre_list(imdb)
rt_genres = genre_list(rt)
mc_genres = genre_list(mc)

all_genres = sorted(list(set(imdb_genres+rt_genres+mc_genres)))

top100 = imdb.append(rt.append(mc))

for genre in all_genres:
    booler = []
    for movie in top100['Genre']:
        if genre in movie:
            booler.append(True)
        else:
            booler.append(False)
    top100[genre]=booler
###

for genre in all_genres:
    print(genre + ': ' + str(top100[genre].sum()))





#Columns need units

#Exploratory Data Analysis

    #Genres
genre_values = []
for genre in all_genres:
    genre_values.append(top100[genre].sum())

fig, ax = plt.subplots()
plt.bar(all_genres, genre_values)
plt.xticks(rotation=90)
plt.show()


#
runtimes = megaframe.groupby(['Source'])['Runtime'].mean()

#Runtime distributions
fig, ax = plt.subplots()
ax.hist(imdb['Runtime'], color='y', alpha=0.5, bins=20)
ax.hist(rt['Runtime'], color='r', alpha=0.5, bins=20)
ax.hist(mc['Runtime'], color='b', alpha=0.5, bins=20)
ax.set_xlabel('Runtime (minutes)')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Runtimes')
plt.show()


sites = ['IMDB', 'Rotten Tomatoes', 'Metacritic']


sns.barplot(data=megaframe.groupby(['Source'])['Runtime'].mean())
plt.show()


#Correlation plot
corr_data = top100.drop(['Movie_Rank', 'Movie_Title', 'Genre', 'Rated', 'Release Date', 'Source'], axis =1)

top100_corr = corr_data.corr()
# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(top100_corr, dtype=np.bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(top100_corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

plt.show()