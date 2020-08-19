from cleaning import movie_cleaning
import pandas as pd
import numpy as np
import math


#imdb = pd.read_csv('Data/imdb_full_raw.csv', encoding = "ISO-8859-1").copy()
#imdb_clean = movie_cleaning.clean(imdb_filtered.copy())
#base_df.replace(' ~data not found~ ', np.NaN)

#imdb_base = pd.read_csv('Data/imdb_giant_trimmed.csv', encoding = "ISO-8859-1").copy()
#imdb_details = pd.read_csv('Data/imdb_giant_details_raw.csv', encoding = "ISO-8859-1").copy()
#imdb_full_raw = imdb_base.join(imdb_details)
full_raw = pd.read_csv('Data/movies_complete_raw.csv', encoding = "ISO-8859-1").copy()
full_clean = movie_cleaning.clean(full_raw.drop(columns=['Title (w/ year)','Title_(RT)','Source']))
#full_clean = full_clean.replace(' ~data not found~ ', np.NaN)
#full_clean = full_clean.replace('~data not found~', np.NaN)
full_clean = full_clean.replace(' ~data not found~ ', 'data unavailable')
full_clean = full_clean.replace('~data not found~', 'data unavailable')
full_clean = full_clean[full_clean['Year']!=2020].reset_index()


new_country=[]
for country in full_clean['Country']:
    if country != 'data unavailable':
        country = country.split(',')[0]
        country = country[2:-1]
        country = country.replace("'", "")
        new_country.append(country)
    else:
        new_country.append(country)
full_clean["Country"] = new_country



new_meta = []
for row in full_clean['Metascore (*)']:
    if row == 'data unavailable':
        row = np.NaN
        new_meta.append(row)
    else:
        row = float(row)
        new_meta.append(row)
full_clean['Metascore (*)'] = new_meta

full_clean['IMDB_Rating'] = full_clean['IMDB_Rating']*10


RT_data = []
for row in range(len(full_clean)):
        if math.isnan(full_clean['RT_critic'][row]):
            if math.isnan(full_clean['RT_audience'][row]):
                RT_data.append(0)
            else:
                RT_data.append(1)
        else:
            RT_data.append(1)
RT_dict = {'RT_Data':RT_data}
RT_data = pd.DataFrame(RT_dict)
full_clean = full_clean.join(RT_data)

full_clean = full_clean[full_clean['RT_Data']==1].drop(columns=['RT_Data'])
full_clean = full_clean[pd.notna(full_clean['Metascore (*)'])]
full_clean = full_clean.reset_index(drop=True)
full_clean.to_csv(r'Data/movies_final.csv')

data = full_clean.copy()


decade=[]
year=[]
month = []
for rdate in data['Release_Date']:
    annum = pd.to_datetime(rdate).year
    mon = pd.to_datetime(rdate).month
    dec = (annum//10)*10
    year.append(annum)
    decade.append(dec)
    month.append(mon)


data['Month'] = (month)
data['Year'] = year
data['Decade'] = decade

#fix Genres into list
new_genres = []
for genres in data['Genre']:
    genres = genres.replace("'",'')
    genres = genres.replace("[", '')
    genres = genres.replace("]", '')
    genres = genres.replace(" ", '')
    genres = genres.replace("-", '_')
    genres = genres.split(',')

    new_genres.append(genres)
data['Genre']=new_genres

def genre_list(df):
    list = []
    for index in range(len(df)):
        genres = df['Genre'][index]
        for items in genres:
            if items in list:
                continue
            list.append(items)
    return list

def country_list(df):
    list = []
    for index in range(len(df)):
        country = df['Country'][index]
        if country in list:
            continue
        list.append(country)
    return list

def lang_list(df):
    list = []
    for index in range(len(df)):
        language = df['Language'][index]
        if language in list:
            continue
        list.append(language)
    return list

data_genres = genre_list(data)
data_countries = country_list(data)
data_languages = lang_list(data)

all_genres = sorted(list(set(data_genres)))

all_countries = sorted(list(set(data_countries)))
all_languages = sorted(list(set(data_languages)))

wide_data = data.copy()

booler = []
for movie in wide_data['Language']:
    if movie != 'English':
        booler.append(True)
    else:
        booler.append(False)
wide_data['Foreign Language']=booler

booler = []
for movie in wide_data['Country']:
    if movie == 'USA':
        booler.append(False)
    elif movie == 'UK':
        booler.append(False)
    else:
        booler.append(True)

wide_data['Foreign Production']=booler


for genre in all_genres:
    booler = []
    for movie in wide_data['Genre']:
        if genre in movie:
            booler.append(True)
        else:
            booler.append(False)
    wide_data[genre]=booler

new_genre=[]
for g in full_clean['Genre']:
    if g != 'data unavailable':
        g = g.split(',')[0]
        g = g[2:-1]
        g = g.replace("'", "")
        new_genre.append(g)
    else:
        new_genre.append(g)
full_clean["Genre"] = new_genre


for country in all_countries:
    booler = []
    for movie in wide_data['Country']:
        if country in movie:
            booler.append(True)
        else:
            booler.append(False)
    wide_data[country]=booler

prim_g = []
for movie in wide_data['Genre']:
        primary = movie[0]
        prim_g.append(primary)
wide_data ['Primary_Genre'] = prim_g

wide_data = wide_data[wide_data['Film_Noir']==False].drop(columns=['Film_Noir'])

wide_data = wide_data.rename(columns={'Metascore (*)':'Metascore'})
wide_data.to_csv('Data/movies_final_wide.csv', index = False)


all_genres.remove('Film_Noir')

genres_dict = {'Genres':all_genres}
genres_df = pd.DataFrame(genres_dict)

genres_df.to_csv('Data/all_genres.csv', index=False)

#Overall Genre data
genre_values = []
for genre in all_genres:
    genre_values.append(wide_data[genre].sum())

g_av_ratings = []
for genre in all_genres:
    frame = wide_data[wide_data[genre]==True]
    g_avg = frame['IMDB_Rating'].mean()
    g_av_ratings.append(g_avg)

g_run = []
for genre in all_genres:
    frame = wide_data[wide_data[genre]==True]
    time = frame['Runtime'].mean()
    g_run.append(time)

# Making Genre DF
overall_genre_stats={'Genre':all_genres, 'Quantity':genre_values, 'Avg_Rating':g_av_ratings, 'Avg_Runtime':g_run}

genre_stats_df=pd.DataFrame(overall_genre_stats)

genre_stats_df.to_csv('Data/Overall_Genre_Stats.csv', index=False)


Action = wide_data[wide_data['Action']==True]
Adventure = wide_data[wide_data['Adventure']==True]
Animation = wide_data[wide_data['Animation']==True]
Biography = wide_data[wide_data['Biography']==True]
Comedy = wide_data[wide_data['Comedy']==True]
Crime = wide_data[wide_data['Crime']==True]
Drama = wide_data[wide_data['Drama']==True]
Family = wide_data[wide_data['Family']==True]
Fantasy = wide_data[wide_data['Fantasy']==True]
History = wide_data[wide_data['History']==True]
Horror = wide_data[wide_data['Horror']==True]
Music = wide_data[wide_data['Music']==True]
Musical = wide_data[wide_data['Musical']==True]
Mystery = wide_data[wide_data['Mystery']==True]
Romance = wide_data[wide_data['Romance']==True]
Sci_Fi = wide_data[wide_data['Sci_Fi']==True]
Sport = wide_data[wide_data['Sport']==True]
Thriller = wide_data[wide_data['Thriller']==True]
War = wide_data[wide_data['War']==True]
Western = wide_data[wide_data['Western']==True]

Action.to_csv(r'Data/Genre_Subsets/Action.csv', index=False)
Adventure.to_csv(r'Data/Genre_Subsets/Adventure.csv', index=False)
Animation.to_csv(r'Data/Genre_Subsets/Animation.csv', index=False)
Biography.to_csv(r'Data/Genre_Subsets/Biography.csv', index=False)
Comedy.to_csv(r'Data/Genre_Subsets/Comedy.csv', index=False)
Crime.to_csv(r'Data/Genre_Subsets/Crime.csv', index=False)
Drama.to_csv(r'Data/Genre_Subsets/Drama.csv', index=False)
Family.to_csv(r'Data/Genre_Subsets/Family.csv', index=False)
Fantasy.to_csv(r'Data/Genre_Subsets/Fantasy.csv', index=False)
History.to_csv(r'Data/Genre_Subsets/History.csv', index=False)
Horror.to_csv(r'Data/Genre_Subsets/Horror.csv', index=False)
Music.to_csv(r'Data/Genre_Subsets/Music.csv', index=False)
Musical.to_csv(r'Data/Genre_Subsets/Musical.csv', index=False)
Mystery.to_csv(r'Data/Genre_Subsets/Mystery.csv', index=False)
Romance.to_csv(r'Data/Genre_Subsets/Romance.csv', index=False)
Sci_Fi.to_csv(r'Data/Genre_Subsets/Sci_Fi.csv', index=False)
Sport.to_csv(r'Data/Genre_Subsets/Sport.csv', index=False)
Thriller.to_csv(r'Data/Genre_Subsets/Thriller.csv', index=False)
War.to_csv(r'Data/Genre_Subsets/War.csv', index=False)
Western.to_csv(r'Data/Genre_Subsets/Western.csv', index=False)



time_genre = {'Decade':(1980,1990,2000,2010,2020)}
for genre in all_genres:
    series = wide_data[wide_data[genre]==True].groupby('Decade')['IMDB_Rating'].mean()
    vals = series.values
    time_genre.update({genre:vals})

time_genre['Western']= np.append(time_genre['Western'], 0)
#genre_time_df = pd.DataFrame(time_genre)
#genre_time_df.to_csv('Data/Analysis_Data/Genre_Decades_Movies.csv', index=False)


genre_percentages_decade = {'Decade':(1950, 1960, 1970, 1980,1990,2000,2010)}
for genre in all_genres:
    series = wide_data[wide_data[genre]==True].groupby('Decade')['Title'].count()/wide_data.groupby('Decade')['Title'].count()
    vals = series.values
    genre_percentages_decade.update({genre:vals})

genre_percentages_decade = pd.DataFrame(genre_percentages_decade)
genre_percentages_decade.to_csv('Data/Analysis_Data/Genre_Percentages_Decade.csv', index=False)




IMDB = wide_data[['Title','IMDB_Rating','Genre', 'Runtime', 'MPAA/TV_Rating', 'Release_Date','Month', 'Year', 'Decade', 'Primary_Genre']].copy()
Metascore = wide_data[['Title','Metascore','Genre', 'Runtime', 'MPAA/TV_Rating', 'Release_Date','Month', 'Year', 'Decade', 'Primary_Genre']].copy()
RT_Critic = wide_data[['Title','RT_critic','Genre', 'Runtime', 'MPAA/TV_Rating', 'Release_Date','Month', 'Year', 'Decade', 'Primary_Genre']].copy()
RT_Audience = wide_data[['Title','RT_audience','Genre', 'Runtime', 'MPAA/TV_Rating', 'Release_Date','Month', 'Year', 'Decade', 'Primary_Genre']].copy()

IMDB['Source'] = 'IMDB'
Metascore['Source'] = 'Metascore'
RT_Critic['Source'] = 'RT Critics'
RT_Audience['Source'] = 'RT Audience'


IMDB = IMDB.rename(columns = {'IMDB_Rating':'Rating'})
Metascore = Metascore.rename(columns = {'Metascore':'Rating'})
RT_Critic = RT_Critic.rename(columns = {'RT_critic':'Rating'})
RT_Audience = RT_Audience.rename(columns = {'RT_audience':'Rating'})


source_list = [IMDB, Metascore, RT_Critic, RT_Audience]


comparison_data = IMDB.append(Metascore.append(RT_Critic.append(RT_Audience)))

comparison_data = comparison_data[~np.isnan(comparison_data['Rating'])].reset_index(drop=True)

critics_data = Metascore.append(RT_Critic)
audience_data = IMDB.append(RT_Audience)

comparison_data.to_csv('Data/Analysis_Data/movies_comparison_wide.csv', index = False)
critics_data.to_csv('Data/Analysis_Data/movies_critics_wide.csv', index = False)
audience_data.to_csv('Data/Analysis_Data/movies_audience_wide.csv', index = False)



