# Import packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# set seaborn style
sns.set_style("whitegrid")


# Import relevant data
wide_data = pd.read_csv('Data/imdb_final_wide.csv', index_col=False)
all_genres = pd.read_csv('Data/all_genres.csv', index_col=False)
all_genres = all_genres['Genres']
genre_decades = pd.read_csv('Data/Analysis_Data/Genre_Decades.csv')
genre_decades_meta = pd.read_csv('Data/Analysis_Data/Genre_Decades_Metascore.csv')
genre_percentages_decade = pd.read_csv('Data/Analysis_Data/Genre_Percentages_Decade.csv')
overall_genre_stats = pd.read_csv('Data/Overall_Genre_Stats.csv')
################## GRAPHING/ANALYSIS ##################

### Overall quantities ###
# Year quantities
fig, ax = plt.subplots(1,2, sharey=True)
ax0, ax1= ax.flatten()
ax0.hist(x='Year', data=wide_data, bins=40)
ax1.hist(x='Year', data=wide_data[wide_data['Metascore (*)']>0], bins=40)
ax0.set_title('Number of movies with an IMDB score')
ax1.set_title('Number of movies with a Metascore')
ax0.set_ylabel('Quantity')
ax0.set_xlabel('Decade')
ax1.set_xlabel('Decade')
#ax.set_xlabel('Year')
plt.savefig('Graphs/yearly_movie_quantities.png')
plt.show()

# Genre quantities
fig, ax = plt.subplots()
plt.bar(all_genres, [wide_data[genre].sum() for genre in all_genres])
plt.xticks(rotation=90)
plt.savefig('Graphs/Overall/Quantities/overall_genre_quantities.png')
plt.show()

# Runtime quantities
fig, ax = plt.subplots()
ax.hist(x='Runtime', data=wide_data, bins=100)
ax.set_title='Frequency of different Runtimes (binned)'
ax.set_xlabel='Runtime (minutes)'
ax.set_ylabel = 'Number of occurences'
plt.savefig('Graphs/Overall/Quantities/overall_runtime_quantities.png')
plt.show()


# MPAA/TV_Rating quantities
fig, ax = plt.subplots()
sns.countplot(x='MPAA/TV_Rating', data=wide_data, hue='Decade')
ax.set_title='Number of each rated movie'
ax.set_xlabel='Maturity rating'
ax.set_ylabel = 'Number of occurences'
plt.savefig('Graphs/Overall/Quantities/overall_maturity_quantities.png')
plt.show()
# Given the obvious results/interpretation of this graph, we dont need to normalize it


### Quantity changes over time ###
# Genre quantities --> Time
def decade_genre_quantities(df, y_label):
    add = [0,5,10,15]
    for num in add:
        fig, ax = plt.subplots(1, 5, sharey=True, sharex=True, figsize=(16, 7))
        for i in range(5):
            sns.barplot(x='Decade', y=all_genres[i+num], data=df, ax=ax[i])
            ax[i].set_title(all_genres[i+num])
            ax[i].set_ylabel('')
            ax[i].set_xlabel('')
        fig.text(0.001, 0.5, y_label, rotation='vertical')
        fig.text(0.5, 0.001, 'Decades')
        plt.setp(ax, ylim=(0, 0.6))
        plt.show()
#not sure how to save

decade_genre_quantities(genre_percentages_decade, 'Percentage of Total Movies')

# Runtime quantities --> Time
fig, ax = plt.subplots()
sns.countplot(x=((wide_data['Runtime']/10).round())*10, data=wide_data, hue='Decade')
ax.set_title='Frequency of different Runtimes (binned)'
ax.set_xlabel='Runtime (minutes)'
ax.set_ylabel = 'Number of occurences'
plt.show()

# MPAA-TV Rating quantities --> Time - already done above



### Overall Ratings ###

# Genre Ratings
fig, ax = plt.subplots()
graph = sns.barplot(data=overall_genre_stats, x='Genre', y='Avg_Rating')
graph.set_xticklabels(ax.get_xticklabels(), rotation=65)
plt.savefig('Graphs/Overall/Ratings/overall_genre_ratings.png')
plt.show()
    #Genre runtimes (Maybe not necessary
fig, ax = plt.subplots()
graph = sns.barplot(data=overall_genre_stats, x='Genre', y='Avg_Runtime')
graph.set_xticklabels(ax.get_xticklabels(), rotation=65)
plt.show()

# Runtime Ratings

# Maturity Ratings
fig, ax = plt.subplots()
graph = sns.barplot(data=wide_data, x='MPAA/TV_Rating', y='IMDB_Rating')
graph.set_xticklabels(ax.get_xticklabels(), rotation=65)
plt.show()

# Time Ratings
    # Year Ratings

    # Decade Ratings

    # Month Ratings


### Ratings Over_Time ###

# Genre Ratings --> Decade

def decade_genre_changes(df, y_label):
    add = [0,5,10,15]
    for num in add:
        fig, ax = plt.subplots(1, 5, sharey=True, sharex=True, figsize=(16, 7))
        for i in range(5):
            sns.barplot(x='Decade', y=all_genres[i+num], data=df, ax=ax[i])
            ax[i].set_title(all_genres[i+num])
            ax[i].set_ylabel('')
            ax[i].set_xlabel('')
        fig.text(0.001, 0.5, y_label, rotation='vertical')
        fig.text(0.5, 0.001, 'Decades')
        plt.show()

decade_genre_changes(genre_decades, y_label='Avg IMDB Rating')
decade_genre_changes(genre_decades_meta, y_label='Avg Metascore')

#Boxplots of genre ratings over time
#imdb
for genre in all_genres: #this works though
    df = wide_data[wide_data[genre]==True]
    fig, ax = plt.subplots()
    sns.boxplot(x='Decade', y='IMDB_Rating', data=df)
    ax.set_title(genre)
    plt.show()


#metascore
for genre in all_genres: #this works though
    df = wide_data[wide_data[genre]==True]
    fig, ax = plt.subplots()
    sns.boxplot(x='Decade', y='Metascore (*)', data=df)
    ax.set_title(genre)
    plt.show()


# Runtime Ratings --> Decade
fig, ax = plt.subplots()
sns.scatterplot(data=wide_data[wide_data['Runtime']>0], x='Runtime', y='IMDB_Rating', hue='Decade', alpha=.75)
ax.set_xlabel('Runtime (minutes)')
ax.set_title('Overall Ratings for different Runtimes')
plt.savefig('Graphs/Over_Time/Ratings/runtime_ratings_over_time.png')
plt.show()



# Maturity Ratings --> Decade
maturity = (wide_data['MPAA/TV_Rating'].dropna().unique().tolist())


for rating in maturity:
    fig, ax = plt.subplots()
    sns.boxplot(x='Decade', y='IMDB_Rating', data=wide_data[wide_data['MPAA/TV_Rating']==rating])
    ax.set_title(rating)
    plt.show()


# repeat looking at months instead of decades?


fig, ax = plt.subplots()
for genres in all_genres:
    sns.lineplot(x='Year', y='IMDB_Rating', data = wide_data[wide_data[genres]==True], ci=None)
plt.savefig('Graphs/Over_Time/Ratings/genre_ratings_over_time.png')
plt.show()