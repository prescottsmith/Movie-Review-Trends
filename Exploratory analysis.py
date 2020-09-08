import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math
import numpy as np

sns.set_style("whitegrid")

wide_data = pd.read_csv('Data/movies_final_wide.csv', index_col=False)
all_genres = pd.read_csv('Data/all_genres.csv', index_col=False)
all_genres = all_genres['Genres'].tolist()
genre_decades = pd.read_csv('Data/Analysis_Data/Genre_Decades.csv')
genre_decades_meta = pd.read_csv('Data/Analysis_Data/Genre_Decades_Metascore.csv')
comparison_data = pd.read_csv('Data/Analysis_Data/movies_comparison_wide.csv')
comparison_data = comparison_data[comparison_data['Decade']!=2020]
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



#Correlation plot
new_data = wide_data[wide_data['Number_of_votes']>10000]
corr_data = new_data.drop(['Title', 'URL', 'Genre', 'MPAA/TV_Rating', 'Release_Date', 'Month', 'Language', 'Decade', 'Country'], axis =1)

correlation = corr_data.corr()


# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(100, 90))

# Generate a custom diverging colormap
#cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(correlation, square=True, annot=True, linewidths=.5, cbar_kws={"shrink": .5})

plt.show()



#Comparing the websites

#website ratings
fig, ax = plt.subplots()
sns.boxplot(x='Source', y='Rating', data=comparison_data)
plt.show()

#website ratings over time
fig, ax = plt.subplots()
sns.boxplot(x='Source', y='Rating', data=comparison_data, hue='Decade')
plt.show()

#genre ratings
for genre in all_genres: #this works though
    df = comparison_data[comparison_data[genre]==True]
    fig, ax = plt.subplots()
    sns.boxplot(x='Source', y='Rating', data=df)
    ax.set_title(genre)
    plt.show()

#genre ratings over time
for genre in all_genres: #this works though
    df = comparison_data[comparison_data[genre]==True]
    fig, ax = plt.subplots()
    sns.boxplot(x='Source', y='Rating', data=df, hue='Decade')
    ax.set_title(genre)
    plt.show()

#Runtime ratings

fig, ax = plt.subplots()
sns.scatterplot(x='Runtime', y='Rating', data=comparison_data, hue='Source')
plt.show()

fig, ax = plt.subplots()
sns.barplot(x='MPAA/TV_Rating', y='Rating', data=comparison_data, hue='Source')
ax.set_xticklabels(ax.get_xticklabels(), rotation=65)
plt.show()

fig, ax = plt.subplots()
sns.barplot(x='Decade', y='Rating', data=comparison_data, hue='Source')
ax.set_xticklabels(ax.get_xticklabels(), rotation=65)
plt.show()

fig, ax = plt.subplots()
sns.boxplot(x='Source', y='Rating', data=comparison_data)
plt.savefig('Graphs/Overall/Ratings/ratings_per_site.png', bbox_inches = "tight")
plt.show()

fig, ax = plt.subplots()
sns.lineplot(x='Year', y='Rating', data=comparison_data, hue='Source')
plt.savefig('Graphs/Over_Time/Ratings/yearly_ratings_per_site.png', bbox_inches = "tight")
plt.show()

fig, ax = plt.subplots()
sns.lineplot(x='Decade', y='Rating', data=comparison_data, hue='Source')
plt.savefig('Graphs/Over_Time/Ratings/decade_ratings_per_site.png', bbox_inches = "tight")
plt.show()


#primary genre ratings over time
for genre in all_genres:
    path = str('Graphs/Over_Time/Ratings/Primary_Genres/decade_ratings_per_site_' + str(genre) + '.png')
    fig, ax = plt.subplots()
    sns.lineplot(x='Decade', y='Rating', data=comparison_data[comparison_data['Primary_Genre']==genre], hue='Source')
    ax.set_title(str('Primarily ' + genre + ' Movies - Ratings over time'))
    plt.savefig(path, bbox_inches="tight")
    plt.show()


for genre in all_genres:
    booler = []
    for movie in comparison_data['Genre']:
        if genre in movie:
            booler.append(True)
        else:
            booler.append(False)
    comparison_data[genre]=booler

#all genre ratings over time
for genre in all_genres:
    path = str('Graphs/Over_Time/Ratings/All_Genre_Tags/decade_ratings_per_site_' + genre + '.png')
    fig, ax = plt.subplots()
    sns.lineplot(x='Decade', y='Rating', data=comparison_data[comparison_data[genre]==1], hue='Source')
    ax.set_title(str('Tagged ' +genre + ' Movies - Ratings over time'))
    ax.set_ylim([0, 100])
    #plt.savefig(path, bbox_inches="tight")
    plt.show()


for genre in all_genres:
    path = str('Graphs/Over_Time/Ratings/Primary_Genres/decade_ratings_per_site_' + str(genre) + '.png')
    fig, ax = plt.subplots(1,2, sharey=True, figsize=(16,7))
    sns.lineplot(x='Decade', y='Rating', data=comparison_data[comparison_data['Primary_Genre']==genre], hue='Source', ax=ax[0])
    sns.lineplot(x='Decade', y='Rating', data=comparison_data[comparison_data[genre] == 1], hue='Source', ax=ax[1])
    ax[0].set_title(str('Primarily ' + genre + ' Movies - Ratings over time'))
    ax[1].set_title(str('Tagged ' + genre + ' Movies - Ratings over time'))
    ax[0].set_ylim([0, 100])
    ax[1].set_ylim([0, 100])
    #plt.savefig(path, bbox_inches="tight")
    plt.show()



fig, ax = plt.subplots()
sns.barplot(x='Month', y='Rating', data=comparison_data[comparison_data['Source']=='RT Critics'], ci=False)
ax.set_ylim([50, 70])
ax.set_title('RT Critics - Average Monthly Ratings')
plt.show()

fig, ax = plt.subplots()
sns.barplot(x='Month', y='Rating', data=comparison_data[comparison_data['Source']=='Metascore'], ci=False)
ax.set_ylim([50, 70])
ax.set_title('Metacritic - Average Monthly Ratings')
plt.show()

fig, ax = plt.subplots()
sns.barplot(x='Month', y='Rating', data=comparison_data[comparison_data['Source']=='IMDB'], ci=False)
ax.set_ylim([50, 70])
ax.set_title('IMDB - Average Monthly Ratings')
plt.show()

fig, ax = plt.subplots()
sns.barplot(x='Month', y='Rating', data=comparison_data[comparison_data['Source']=='RT Audience'], ci=False)
ax.set_ylim([50, 70])
ax.set_title('RT Audience - Average Monthly Ratings')
plt.show()

fig, ax = plt.subplots()
sns.countplot(x='Month', data=wide_data)
ax.set_title('Monthly release quantities')
plt.show()

fig, ax = plt.subplots()
sns.countplot(x='Month', data=wide_data[wide_data['Year']>=2000])
ax.set_title('Monthly release quantities - last 20 years')
plt.show()



for genre in all_genres:
    data = wide_data[wide_data[genre]==True]
    fig, ax = plt.subplots()
    sns.barplot(x='Month', y='RT_critic', data=data[data['Year']>=2000], ci=False)
    ax.set_ylim([0, 100])
    ax.set_ylabel('Rating')
    ax.set_title('RT Critics - Average Monthly ' + str(genre) + ' Ratings')
    plt.savefig('Graphs/Over_Time/Ratings/Monthly/Genres/RT_critic_monthly_ratings_' + str(genre) + '.png', bbox_inches = "tight")
    plt.show()

for genre in all_genres:
    data = wide_data[wide_data[genre]==True]
    fig, ax = plt.subplots()
    sns.countplot(x='Month', data=data[data['Year']>=2000])
    ax.set_title('Quantity of ' + str(genre) + ' Genre releases per month since 2000')
    #plt.savefig('Graphs/Over_Time/Ratings/Monthly/RT_critic_monthly_ratings.png', bbox_inches = "tight")
    plt.show()

#just RT critic 10 year country ratings
country_list = ['USA', 'UK', 'France', 'Canada', 'Germany', 'Australia', 'Japan', 'Spain', 'China']
for country in country_list:
    fig, ax = plt.subplots(figsize=(20,9))
    ax.set_ylim([0, 100])
    country_data = wide_data[wide_data['Country']==country]
    sns.barplot(x='Year', y='RT_critic', data=country_data[country_data['Year']>2009])
    ax.set_title(str(country) + ' movie ratings last 5 years')
    ax.set_ylabel('Average RT Critic Rating')
    ax.set_xlabel('Year')

    #plt.savefig('Graphs/Overall/Ratings/top10_country_Ratings_meta.png', bbox_inches = "tight")
    plt.show()


#switch to show different website ratings
country_list = ['USA', 'UK', 'France', 'Canada', 'Germany', 'Australia', 'Japan', 'Spain', 'China']
for country in country_list:
    fig, ax = plt.subplots(figsize=(20,9))
    ax.set_ylim([0, 100])
    country_data = comparison_data[comparison_data['Country']==country]
    sns.barplot(x='Year', y='Rating', data=country_data[country_data['Year']>2009], hue='Source')
    ax.set_title(str(country) + ' movie ratings last 10 years')
    ax.set_ylabel('Average RT Critic Rating')
    ax.set_xlabel('Year')
    #plt.savefig('Graphs/Overall/Ratings/top10_country_Ratings_meta.png', bbox_inches = "tight")
    plt.show()


fig, ax = plt.subplots(figsize=(20,9))
sns.barplot(x='Country', y='Rating', data=comparison_data[comparison_data['Year']>2009], hue='Source', order = comparison_data.Country.value_counts().iloc[:10].index)
ax.set_title('Top 10 movie-producing countries - Average ratings (last decade)', fontsize=23)
ax.set_ylabel('Average Movie Rating', fontsize=20)
ax.set_xlabel('Country', fontsize=20)
ax.tick_params(labelsize=18)
ax.legend(fontsize='x-large', title_fontsize='40')
plt.savefig('Graphs/Overall/Ratings/top10_country_Ratings.png', bbox_inches = "tight")
plt.show()


#Runtime ratings last 20 years
wide_data['Runtime_rounded']=round(wide_data['Runtime']/5)*5



fig, ax = plt.subplots()
sns.barplot(x='Runtime_rounded', y='RT_critic', data=wide_data[wide_data['Year']>=2000])
ax.set_ylim([0, 100])
ax.set_ylabel('RT Critic Rating', fontsize=12)
ax.set_xlabel('Rounded Runtimes (nearest 5 minutes)', fontsize=12)
ax.tick_params(labelsize=10, rotation=90)
ax.set_title("Runtimes - Average Ratings from RT Critics (last 20 years)", fontsize=14)
#plt.savefig('Graphs/Overall/Ratings/Runtime_ratings_20_year_RT_critics.png', bbox_inches = "tight")
plt.show()

#Runtime ratings across genres
last20 = wide_data[wide_data['Year']>=2000]

for genre in all_genres:
    fig, ax = plt.subplots()
    sns.barplot(x='Runtime_rounded', y='RT_critic', data=last20[last20[genre]==True])
    ax.set_ylim([0, 100])
    ax.set_ylabel('RT Critic Rating', fontsize=12)
    ax.set_xlabel('Rounded Runtimes (nearest 5 minutes)', fontsize=12)
    ax.tick_params(labelsize=10, rotation=90)
    ax.set_title("'"+ str(genre) + "' Runtimes - Average Ratings from RT Critics (last 20 years)", fontsize=14)
    plt.savefig('Graphs/Overall/Ratings/Genres/Runtimes/' + str(genre) + '_ratings_20_year_RT_critics.png', bbox_inches = "tight")
    plt.show()

#Monthly runtime ratings
months = [1,2,3,4,5,6,7,8,9,10,11,12]
for month in months:
    fig, ax = plt.subplots()
    sns.barplot(x='Runtime_rounded', y='RT_critic', data=last20[last20['Month']==month])
    ax.set_ylim([0, 100])
    ax.set_ylabel('RT Critic Rating', fontsize=12)
    ax.set_xlabel('Rounded Runtimes (nearest 5 minutes)', fontsize=12)
    ax.tick_params(labelsize=10, rotation=90)
    ax.set_title(str(month) + "st month Runtime Average Ratings from RT Critics (last 20 years)", fontsize=14)
    #plt.savefig('Graphs/Overall/Ratings/Genres/Runtimes/' + str(genre) + '_ratings_20_year_RT_critics.png', bbox_inches = "tight")
    plt.show()

#maturity ratings
fig, ax = plt.subplots()
sns.barplot(x='MPAA/TV_Rating', y='Rating', data=comparison_data[comparison_data['Year']>=2000], hue='Source')
ax.set_ylim([0, 100])
ax.set_ylabel('Rating', fontsize=12)
ax.set_xlabel('Maturity Rating', fontsize=12)
ax.tick_params(labelsize=10, rotation=90)
ax.set_title("Average Reviews for different maturity ratings (last 20 years)", fontsize=14)
plt.savefig('Graphs/Overall/Ratings/reviews_maturity_ratings_20year.png', bbox_inches = "tight")
plt.show()

#maturity ratings monthly
maturities = ['Not Rated', 'PG-13', 'R', 'PG', 'G', 'TV-14', 'TV-PG']

for rating in maturities:
    data = wide_data[wide_data['MPAA/TV_Rating']==rating]
    fig, ax = plt.subplots()
    sns.barplot(x='Month', y='RT_critic', data=data[data['Year']>=2000])
    ax.set_ylim([0, 100])
    ax.set_ylabel('Rating', fontsize=11)
    ax.set_ylabel('Month', fontsize=11)
    ax.tick_params(labelsize=10)
    ax.set_title("'" + str(rating) + "' rated movies - Average monthly RT critic reviews (last 20 years)", fontsize=13)
    plt.savefig('Graphs/Overall/Ratings/Monthly/Maturities/RT_critic_monthly_ratings_' + str(rating) + '_movies.png', bbox_inches = "tight")
    plt.show()

#Monthly maturity ratings
months = [1,2,3,4,5,6,7,8,9,10,11,12]
for month in months:
    fig, ax = plt.subplots()
    sns.barplot(x='Runtime_rounded', y='RT_critic', data=last20[last20['Month']==month])
    ax.set_ylim([0, 100])
    ax.set_ylabel('RT Critic Rating', fontsize=12)
    ax.set_xlabel('Rounded Runtimes (nearest 5 minutes)', fontsize=12)
    ax.tick_params(labelsize=10, rotation=90)
    ax.set_title(str(month) + "st month Runtime Average Ratings from RT Critics (last 20 years)", fontsize=14)
    #plt.savefig('Graphs/Overall/Ratings/Genres/Runtimes/' + str(genre) + '_ratings_20_year_RT_critics.png', bbox_inches = "tight")
    plt.show()


for genre in all_genres:
    fig, ax = plt.subplots()
    sns.barplot(x='MPAA/TV_Rating', y='RT_critic', data=last20[last20[genre]==True])
    ax.set_ylim([0, 100])
    ax.set_ylabel('RT Critic Rating', fontsize=12)
    ax.set_xlabel('Maturity Rating', fontsize=12)
    ax.tick_params(labelsize=10, rotation=90)
    ax.set_title("'"+ str(genre) + "' movies' maturities - Average RT Critic Ratings (last 20 years)", fontsize=14)
    #plt.savefig('Graphs/Overall/Ratings/Genres/Runtimes/' + str(genre) + '_ratings_20_year_RT_critics.png', bbox_inches = "tight")
    plt.show()