import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

sns.set_style("whitegrid")

wide_data = pd.read_csv('Data/imdb_final_wide.csv', index_col=False)
all_genres = pd.read_csv('Data/all_genres.csv', index_col=False)
all_genres = all_genres['Genres'].tolist()
genre_decades = pd.read_csv('Data/Analysis_Data/Genre_Decades.csv')
genre_decades_meta = pd.read_csv('Data/Analysis_Data/Genre_Decades_Metascore.csv')

#wide_data = wide_data[wide_data['Number_of_votes']>5000]

# Total quantities
year=[]
for rdate in wide_data['Release_Date']:
    annum = pd.to_datetime(rdate).year
    year.append(annum)
wide_data['Year'] = year

fig, ax = plt.subplots()
plt.hist(x='Year', data=wide_data, bins=40)
plt.show()



# How time affects genre ratings

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

def decade_genre_changes_box(df, y_label):
    add = [0,5,10,15]
    for num in add:
        fig, ax = plt.subplots(1, 5, sharey=True, sharex=True, figsize=(16, 7))
        for i in range(5):
            sns.boxplot(x='Decade', y='IMDB_Rating', data=df, ax=ax[i])
            ax[i].set_title(all_genres[i+num])
            ax[i].set_ylabel('')
            ax[i].set_xlabel('')
        fig.text(0.001, 0.5, y_label, rotation='vertical')
        fig.text(0.5, 0.001, 'Decades')
        plt.show() #doesnt work yet


#Boxplots of genre ratings over time
for genre in all_genres: #this works though
    df = wide_data[wide_data[genre]==True]
    fig, ax = plt.subplots()
    sns.boxplot(x='Decade', y='IMDB_Rating', data=df)
    ax.set_title(genre)
    plt.show()


decade_genre_changes_box(genre_decades, y_label='Avg IMDB Rating')
decade_genre_changes(genre_decades_meta, y_label='Avg Metascore')

# Genre quantities
for genre in all_genres: #this works though
    df = wide_data[wide_data[genre]==True]
    fig, ax = plt.subplots()
    sns.barplot(x='Decade', y= , data=wide_data)
    ax.set_title(genre)
    plt.show()

# Genre graphing
list_of_frames = []

Action = pd.read_csv('Data/Genre_Subsets/Action.csv')
list_of_frames.append(Action)

Adventure = pd.read_csv('Data/Genre_Subsets/Adventure.csv')
list_of_frames.append(Adventure)

Animation = pd.read_csv('Data/Genre_Subsets/Animation.csv')
list_of_frames.append(Animation)

Biography = pd.read_csv('Data/Genre_Subsets/Biography.csv')
list_of_frames.append(Biography)

Comedy = pd.read_csv('Data/Genre_Subsets/Comedy.csv')
list_of_frames.append(Comedy)

Crime = pd.read_csv('Data/Genre_Subsets/Crime.csv')
list_of_frames.append(Crimes)

Drama = pd.read_csv('Data/Genre_Subsets/Drama.csv')
list_of_frames.append(Drama)

Family = pd.read_csv('Data/Genre_Subsets/Family.csv')
list_of_frames.append(Family)

Fantasy = pd.read_csv('Data/Genre_Subsets/Fantasy.csv')
list_of_frames.append(Fantasy)

History = pd.read_csv('Data/Genre_Subsets/History.csv')
list_of_frames.append(History)

Horror = pd.read_csv('Data/Genre_Subsets/Horror.csv')
list_of_frames.append(Horror)

Music = pd.read_csv('Data/Genre_Subsets/Music.csv')
list_of_frames.append(Music)

Mystery = pd.read_csv('Data/Genre_Subsets/Mystery.csv')
list_of_frames.append(Mystery)

Romance = pd.read_csv('Data/Genre_Subsets/Romance.csv')
list_of_frames.append(Romance)

Sci_Fi = pd.read_csv('Data/Genre_Subsets/Sci_Fi.csv')
list_of_frames.append(Sci_Fi)

Sport = pd.read_csv('Data/Genre_Subsets/Sport.csv')
list_of_frames.append(Sport)

Thriller = pd.read_csv('Data/Genre_Subsets/Thriller.csv')
list_of_frames.append(Thriller)

War = pd.read_csv('Data/Genre_Subsets/War.csv')
list_of_frames.append(War)

Western = pd.read_csv('Data/Genre_Subsets/Western.csv')
list_of_frames.append(Western)



# Genres quantity
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
graph = sns.barplot(data=wide_data, x=wide_data['Decade'], y=wide_data.groupby('Decade')['IMDB_Rating'].mean())
graph.set_xticklabels(ax.get_xticklabels(), rotation=65)
plt.show()

g = sns.catplot(x="Decade", y="IMDB_Rating",
                data=wide_data, saturation=.5,
                kind="bar", ci=None, aspect=.6)

(g.set_axis_labels("Decade", "Average Rating"))
plt.show()

#Try making a boxplot for decades

#Genres over time
f, axes = plt.subplots(1,2)
sns.catplot(x="Decade", y="IMDB_Rating", data=Action, kind="bar", ax=axes[0])
#axes[0,0].set_titles('Action')

sns.catplot(x="Decade", y="IMDB_Rating", data=Adventure, kind="bar", ax=axes[1])
#axes[0, 1].set_titles('Adventure')

#sns.catplot(x="Decade", y="IMDB_Rating", data=Animation, kind="bar", ax=axes[0, 2])
#axes[0, 2].set_titles('Animation')

#sns.catplot(x="Decade", y="IMDB_Rating", data=Biography, kind="bar", ax=axes[1, 0])
#xes[1, 0].set_titles('Biography')

#sns.catplot(x="Decade", y="IMDB_Rating", data=Comedy, kind="bar", ax=axes[1, 1])
#axes[1, 1].set_titles('Comedy')

#sns.catplot(x="Decade", y="IMDB_Rating", data=Crime, kind="bar", ax=axes[1, 2])
#axes[1, 2].set_titles('Crime')

plt.close(2)
plt.close(3)
f.tight_layout()

plt.show()


#Take 2
fig, ax = plt.subplots(1,2, sharey=True)

sns.barplot(x='Decade', y='Action', data=genre_decades, ax=ax[0])
ax[0].set_title('Action')
ax[0].set_ylabel('Average IMDB Rating')

sns.barplot(x='Decade', y='Adventure', data=genre_decades, ax=ax[1])
ax[1].set_title('Adventure')

plt.show()




# Runtime Ratings
runtime_data = wide_data[wide_data['Runtime']>0]

    #IMDB
graph = sns.scatterplot(data=runtime_data, x='Runtime', y='IMDB_Rating', )
plt.show()
    #Metascore
graph = sns.scatterplot(data=runtime_data[runtime_data['Metascore (*)']>0], x='Runtime', y='Metascore (*)')
plt.show()



longest_movie = wide_data[wide_data['Runtime']==wide_data['Runtime'].max()]
print(longest_movie['Title'] + ' ' + str(longest_movie['Runtime']) + 'mins')
