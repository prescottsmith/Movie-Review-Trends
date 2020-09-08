# Import packages
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# set seaborn style
sns.set_style("whitegrid")


# Import relevant data
wide_data = pd.read_csv('Data/movies_final_wide.csv', index_col=False)
all_genres = pd.read_csv('Data/all_genres.csv', index_col=False)
all_genres = all_genres['Genres']
genre_decades = pd.read_csv('Data/Analysis_Data/Genre_Decades.csv')
genre_decades_meta = pd.read_csv('Data/Analysis_Data/Genre_Decades_Metascore.csv')
genre_percentages_decade = pd.read_csv('Data/Analysis_Data/Genre_Percentages_Decade.csv')
overall_genre_stats = pd.read_csv('Data/Overall_Genre_Stats.csv')
comparison_data = pd.read_csv('Data/Analysis_Data/movies_comparison_wide.csv')
critics_data = pd.read_csv('Data/Analysis_Data/movies_critics_wide.csv')
audience_data = pd.read_csv('Data/Analysis_Data/movies_audience_wide.csv')


################## GRAPHING/ANALYSIS ##################

### Overall quantities ###
# Year quantities
fig, ax = plt.subplots()
ax.hist(x='Year', data=wide_data, bins=70)
ax.set_title('Number of movies in dataset')
ax.set_ylabel('Quantity')
ax.set_xlabel('Year')
plt.savefig('Graphs/yearly_movie_quantities.png')
plt.show()

#Month quantities
fig, ax = plt.subplots()
sns.countplot(x='Month', data=wide_data)
ax.set_title('Movies released by month')
ax.set_ylabel('Quantity')
ax.set_xlabel('Month')
plt.savefig('Graphs/monthly_movie_quantities.png')
plt.show()

# Genre quantities
fig, ax = plt.subplots()
plt.bar(all_genres, [wide_data[genre].sum() for genre in all_genres])
ax.xaxis.grid(False)
plt.xticks(rotation=90)
ax.set_title('Total quantity of Movie Genre Occurrences')
plt.savefig('Graphs/Overall/Quantities/overall_genre_quantities.png', bbox_inches = "tight")
plt.show()

#Primary Genre Quantities
fig, ax = plt.subplots()
sns.countplot(x='Primary_Genre', data=wide_data.sort_values(by=['Primary_Genre']), color='blue')
plt.xticks(rotation=90)
ax.set_title('Primary Movie Genre Quantities')
ax.set_ylabel('Quantity')
ax.set_xlabel('')
plt.savefig('Graphs/Overall/Quantities/overall_primary_genre_quantities.png', bbox_inches = "tight")
plt.show()

# Runtime quantities
fig, ax = plt.subplots()
plt.hist(x='Runtime', data=wide_data, bins=100)
plt.axvline(wide_data['Runtime'].mean(), color='k', linestyle='dashed', linewidth=1)
ax.set_title('Frequency of different Runtimes (binned)')
ax.set_xlabel('Runtime (minutes)')
ax.set_ylabel('Number of occurences')
plt.savefig('Graphs/Overall/Quantities/overall_runtime_quantities.png')
plt.show()


# MPAA/TV_Rating quantities - NOPE
fig, ax = plt.subplots()
sns.countplot(x='MPAA/TV_Rating', data=wide_data)
ax.set_title('Number of Movies with different maturity ratings')
ax.set_xlabel('Maturity rating')
plt.xticks(rotation=90)
plt.savefig('Graphs/Overall/Quantities/overall_maturity_quantities.png', bbox_inches = "tight")
plt.show()
# Given the obvious results/interpretation of this graph, we dont need to normalize it

#Country Quantities

fig, ax = plt.subplots()
sns.countplot(x='Country', data=wide_data, color='blue', order=wide_data.Country.value_counts().iloc[:10].index)
plt.xticks(rotation=90)
ax.set_title('Top 10 Movie-producing Countries')
ax.set_ylabel('Quantity of Movies')
ax.set_xlabel('Country')
plt.savefig('Graphs/Overall/Quantities/top10_country_quantities.png', bbox_inches = "tight")
plt.show()

#Monthly Quantities
fig, ax = plt.subplots()
sns.countplot(x='Month', data=wide_data)
ax.set_title('Monthly release quantities')
plt.savefig('Graphs/Overall/Quantities/monthly_release_quantities.png', bbox_inches = "tight")
plt.show()

fig, ax = plt.subplots()
sns.countplot(x='Month', data=wide_data[wide_data['Year']>=2000])
ax.set_title('Monthly release quantities - last 20 years')
plt.savefig('Graphs/Overall/Quantities/monthly_release_quantities_20years.png', bbox_inches = "tight")
plt.show()


#RATINGS
#ratings per site
fig, ax = plt.subplots()
sns.boxplot(x='Source', y='Rating', data=comparison_data)
plt.savefig('Graphs/Overall/Ratings/ratings_per_site.png', bbox_inches = "tight")
plt.show()

#Ratings per site yearly
fig, ax = plt.subplots()
sns.lineplot(x='Year', y='Rating', data=comparison_data, hue='Source')
ax.set_ylim([0, 100])
plt.savefig('Graphs/Over_Time/Ratings/yearly_ratings_per_site.png', bbox_inches = "tight")
plt.show()

#Ratings per site (decades)
fig, ax = plt.subplots()
sns.lineplot(x='Decade', y='Rating', data=comparison_data, hue='Source')
ax.set_ylim([0, 100])
plt.savefig('Graphs/Over_Time/Ratings/decade_ratings_per_site.png', bbox_inches = "tight")
plt.show()



#Monthly Ratings
fig, ax = plt.subplots()
sns.barplot(x='Month', y='Rating', data=comparison_data[comparison_data['Source']=='RT Critics'], ci=False)
ax.set_ylim([50, 70])
ax.set_title('RT Critics - Average Monthly Ratings')
plt.savefig('Graphs/Over_Time/Ratings/Monthly/RT_critic_monthly_ratings.png', bbox_inches = "tight")
plt.show()

fig, ax = plt.subplots()
sns.barplot(x='Month', y='Rating', data=comparison_data[comparison_data['Source']=='Metascore'], ci=False)
ax.set_ylim([50, 70])
ax.set_title('Metacritic - Average Monthly Ratings')
plt.savefig('Graphs/Over_Time/Ratings/Monthly/Metacritic_monthly_ratings.png', bbox_inches = "tight")
plt.show()

fig, ax = plt.subplots()
sns.barplot(x='Month', y='Rating', data=comparison_data[comparison_data['Source']=='IMDB'], ci=False)
ax.set_ylim([50, 70])
ax.set_title('IMDB - Average Monthly Ratings')
plt.savefig('Graphs/Over_Time/Ratings/Monthly/IMDB_monthly_ratings.png', bbox_inches = "tight")
plt.show()

fig, ax = plt.subplots()
sns.barplot(x='Month', y='Rating', data=comparison_data[comparison_data['Source']=='RT Audience'], ci=False)
ax.set_ylim([50, 70])
ax.set_title('RT Audience - Average Monthly Ratings')
plt.savefig('Graphs/Over_Time/Ratings/Monthly/RT_audience_monthly_ratings.png', bbox_inches = "tight")
plt.show()


# Genre critic ratings by month (20 years)
for genre in all_genres:
    data = wide_data[wide_data[genre]==True]
    fig, ax = plt.subplots()
    sns.barplot(x='Month', y='RT_critic', data=data[data['Year']>=2000], ci=False)
    ax.set_ylim([0, 100])
    ax.set_ylabel('Rating', fontsize=12)
    ax.set_xlabel('Month', fontsize=12)
    ax.tick_params(labelsize=10)
    ax.set_title("RT Critics - Average Monthly '" + str(genre) + "' Ratings", fontsize=14)
    plt.savefig('Graphs/Over_Time/Ratings/Monthly/Genres/RT_critic_monthly_ratings_' + str(genre) + '.png', bbox_inches = "tight")
    plt.show()

# quantity reference for genre monthly releases
for genre in all_genres:
    data = wide_data[wide_data[genre]==True]
    fig, ax = plt.subplots()
    sns.countplot(x='Month', data=data[data['Year']>=2000])
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Number of movies', fontsize=12)
    ax.set_title('Monthly release quantities of ' + str(genre) + ' movies - last 20 years', fontsize=14)
    plt.savefig('Graphs/Over_Time/Quantities/Monthly/Genres/monthly_release_quantities_20years_' + str(genre) + '.png', bbox_inches = "tight")
    plt.show()

#order=critics_data.groupby('Country')['Rating'].mean().sort_values(ascending=False).iloc[:10].index

fig, ax = plt.subplots(figsize=(20,9))
sns.barplot(x='Country', y='Rating', data=comparison_data[comparison_data['Year']>2009], hue='Source', order = comparison_data.Country.value_counts().iloc[:10].index)
ax.set_title('Top 10 movie-producing countries - Average ratings (last decade)', fontsize=23)
ax.set_ylabel('Average Movie Rating', fontsize=20)
ax.set_xlabel('Country', fontsize=20)
ax.tick_params(labelsize=18)
ax.legend(fontsize='x-large', title_fontsize='40')
plt.savefig('Graphs/Overall/Ratings/top10_country_Ratings.png', bbox_inches = "tight")
plt.show()

top5_countries= critics_data.Country.value_counts().iloc[:5]

top5_country_ratings_c = critics_data.loc[(critics_data['Country']=='Japan') | (critics_data['Country']=='Italy') | (critics_data['Country']=='France') | (critics_data['Country']=='Canada') | (critics_data['Country']=='Germany')]

#Country ratings over time
fig, ax = plt.subplots()
sns.lineplot(x='Decade', y='Rating', data=top5_country_ratings_c, hue='Country')
#plt.savefig('Graphs/Over_Time/Ratings/top5_country_ratings_critics.png', bbox_inches = "tight")
plt.show()




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
sns.countplot(x=((wide_data['Runtime']/10).round())*10, data=wide_data, hue='Decade', normalize=)
ax.set_title('Frequency of different Runtimes (binned)')
ax.set_xlabel('Runtime (minutes)')
ax.set_ylabel('Number of occurences')
plt.show()

# MPAA-TV Rating quantities --> Time - already done above



### Overall Ratings ###

# Genre Ratings
fig, ax = plt.subplots()
graph = sns.barplot(data=overall_genre_stats, x='Genre', y='Avg_Rating')
graph.set_xticklabels(ax.get_xticklabels(), rotation=65)
ax.set_title('Overall Average Genre Ratings')
ax.set_ylabel('Average Rating')
plt.savefig('Graphs/Overall/Ratings/overall_genre_ratings.png')
plt.show()

fig, ax = plt.subplots(1,2, figsize=(20, 7), sharey=True)
plt.xticks(rotation=90)
sns.boxplot(data=critics_data, x='Primary_Genre', y='Rating', hue='Source', ax=ax[0])
sns.boxplot(data=audience_data, x='Primary_Genre', y='Rating', hue='Source', ax=ax[1])
plt.show()

    #Genre runtimes (Maybe not necessary
fig, ax = plt.subplots()
graph = sns.barplot(data=overall_genre_stats, x='Genre', y='Avg_Runtime')
ax.set_title('Overall Average Genre Runtimes')
ax.set_ylabel('Average Runtime')
graph.set_xticklabels(ax.get_xticklabels(), rotation=65)
plt.show()

# Runtime Ratings

# Maturity Ratings
fig, ax = plt.subplots()
graph = sns.barplot(data=wide_data, x='MPAA/TV_Rating', y='IMDB_Rating')
ax.set_title('Average Rating movies with different Maturity levels')
ax.set_ylabel('Average Rating')
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
        fig, ax = plt.subplots(2, 5, sharey=True, sharex=True, figsize=(16, 7))
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




#Country Ratings
country_list = ['USA', 'UK', 'France', 'Canada', 'Germany', 'Australia', 'Japan', 'Spain', 'China']
for country in country_list:
    fig, ax = plt.subplots(figsize=(20,9))
    ax.set_ylim([0, 100])
    country_data = comparison_data[comparison_data['Country']==country]
    sns.barplot(x='Year', y='Rating', data=country_data[country_data['Year']>2009], hue='Source')
    ax.set_title(str(country) + ' movie ratings last 10 years', fontsize=29)
    ax.set_ylabel('Average RT Critic Rating', fontsize=21)
    ax.set_xlabel('Year', fontsize=21)
    ax.tick_params(labelsize=20)
    ax.legend(fontsize=18)
    plt.savefig('Graphs/Over_Time/Ratings/' + str(country) + '_Ratings_10_year.png', bbox_inches = "tight")
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
plt.savefig('Graphs/Overall/Ratings/Runtime_ratings_20_year_RT_critics.png', bbox_inches = "tight")
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