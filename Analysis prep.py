from cleaning import movie_cleaning
import pandas as pd
import numpy as np


#imdb = pd.read_csv('Data/imdb_full_raw.csv', encoding = "ISO-8859-1").copy()
#imdb_clean = movie_cleaning.clean(imdb_filtered.copy())
#base_df.replace(' ~data not found~ ', np.NaN)

imdb_base = pd.read_csv('Data/imdb_trimmed.csv', encoding = "ISO-8859-1").copy()
imdb_details = pd.read_csv('Data/imdb_details_raw.csv', encoding = "ISO-8859-1").copy()
imdb_full_raw = imdb_base.join(imdb_details)
imdb_full_clean = movie_cleaning.clean(imdb_full_raw.drop(columns='Title (w/ year)'))
imdb_full_clean = imdb_full_clean.replace(' ~data not found~ ', np.NaN)
imdb_full_clean = imdb_full_clean.replace('~data not found~', np.NaN)

new_meta = []
for row in imdb_full_clean['Metascore (*)']:
    row = float(row)
    new_meta.append(row)
imdb_full_clean['Metascore (*)'] = new_meta

imdb_full_clean['Metascore (*)'] = imdb_full_clean['Metascore (*)']/10
imdb_full_clean.to_csv(r'Data/imdb_final.csv')

data = imdb_full_clean.copy()


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

wide_data = data.copy()
data_genres = genre_list(data)


all_genres = sorted(list(set(data_genres)))

for genre in all_genres:
    booler = []
    for movie in wide_data['Genre']:
        if genre in movie:
            booler.append(True)
        else:
            booler.append(False)
    wide_data[genre]=booler

wide_data.to_csv('Data/imdb_final_wide.csv', index = False)

def genre_list(df):
    list = []
    for index in range(len(df)):
        genres = df['Genre'][index]
        for items in genres:
            if items in list:
                continue
            list.append(items)
    return list

data_genres = genre_list(wide_data)
all_genres = sorted(list(set(data_genres)))


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
genre_time_df = pd.DataFrame(time_genre)
genre_time_df.to_csv('Data/Analysis_Data/Genre_Decades_IMDB.csv', index=False)

time_genre = {'Decade':(1980,1990,2000,2010,2020)}
for genre in all_genres:
    series = wide_data[wide_data[genre]==True].groupby('Decade')['Metascore (*)'].mean()
    vals = series.values
    time_genre.update({genre:vals})

time_genre['Western']= np.append(time_genre['Western'], 0)
genre_time_df_meta = pd.DataFrame(time_genre)
genre_time_df_meta.to_csv('Data/Analysis_Data/Genre_Decades_Metascore.csv', index=False)




genre_percentages_decade = {'Decade':(1980,1990,2000,2010,2020)}
for genre in all_genres:
    series = wide_data[wide_data[genre]==True].groupby('Decade')['Title'].count()/wide_data.groupby('Decade')['Title'].count()
    vals = series.values
    genre_percentages_decade.update({genre:vals})
genre_percentages_decade = pd.DataFrame(genre_percentages_decade)
genre_percentages_decade.to_csv('Data/Analysis_Data/Genre_Percentages_Decade.csv', index=False)






#This won't work because of mismatched lengths (some years might not have a genre represented)
genre_percentages_year = {'Year':(range(1980,2020))}
for genre in all_genres:
    series = wide_data[wide_data[genre]==True].groupby('Year')['Title'].count()/wide_data.groupby('Year')['Title'].count()
    vals = series.values
    genre_percentages_year.update({genre:vals})
genre_percentages_year = pd.DataFrame(genre_percentages_year)
genre_percentages_year.to_csv('Data/Analysis_Data/Genre_Percentages_Year.csv', index=False)



