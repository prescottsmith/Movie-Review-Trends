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
for rdate in data['Release_Date']:
    year = pd.to_datetime(rdate).year
    dec = (year//10)*10
    decade.append(dec)

data['Decade'] = decade

#fix Genres into list
new_genres = []
for genres in data['Genre']:
    genres = genres.replace("'",'')
    genres = genres.replace("[", '')
    genres = genres.replace("]", '')
    genres = genres.replace(" ", '')
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

wide_data.to_csv(r'Data/imdb_final_wide.csv')

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
