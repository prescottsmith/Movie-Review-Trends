import pandas
from pytimeparse.timeparse import timeparse
import dateutil.parser as dparser
import re
import numpy as np

ratings_list = [' R ',
               ' M ',#this is now PG
               ' MA ',
               ' PG-13 ',
               ' TV-14 ',
               ' TV-G ',
               ' TV-PG ',
               ' TV-R ',
               ' GP ',#this is PG
               ' PG ',
               ' M/PG ',
               ' G ',
               ' Approved ',
               ' Passed ',
               ' Not Rated ',
               ' NR ',
               ' Unrated ']

class CL:


    def ratings_update(self):
        self = self.replace(' M ', ' PG ')
        self = self.replace(' GP ', ' PG ')
        self = self.replace(' TV-G ', ' G ')
        self = self.replace(' TV-PG ', ' PG ')
        self = self.replace(' TV-14 ', ' PG-13 ') #Closest approximation
        self = self.replace(' NR ', ' Not Rated ')
        self = self.replace('Unrated', 'Not Rated')
        return self

    def genres(self):
        cleaned_genres = []
        for genres in self['Genre']:
            if genres.startswith('\n'):
                genres = genres.replace('\n','')
                listy = re.split(r'[,&]', genres)
                row = []
                for item in listy:
                    if item==' Suspense':
                        continue
                    new = item.replace(' ', '')
                    row.append(new)
                cleaned_genres.append(row)
            else:
                cleaned_genres.append(genres)
        self['Genre'] = cleaned_genres
        return self


    def rated(self):
        cleaned_rating = []
        #for row in self['Rated']:
        for row in self['MPAA/TV_Rating']:
            try:
                row = ' ' + row + ' '
                new_rating = ''.join([rating for rating in ratings_list if rating in row]).strip()
                new_rating = CL.ratings_update(new_rating)
                cleaned_rating.append(new_rating)
            except:
                cleaned_rating.append(row)
        self['MPAA/TV_Rating'] = cleaned_rating
        return self

    def runtime(self):
        cleaned_runtime = []
        for row in self['Runtime']:
            try:
                row = row.replace(' ', '')
                row = row.replace('minutes', 'm')
                row = row.replace('min', 'm')
                try:
                    minutes = timeparse(row)/60
                except:
                    minutes = 0
            except:
                minutes = row
            cleaned_runtime.append(minutes)
        self['Runtime'] = cleaned_runtime
        return self


    def release(self):
        cleaned_release = []
        for row in self['Release_Date']:
            row = row.replace('Release Date: ', '').split('\n')
            try:
                row = row[1].split('(')[0].strip()
                date = dparser.parse(row, fuzzy=True).date()
                cleaned_release.append(date)
            except:
                cleaned_release.append(np.NaN)
        self['Release_Date'] = cleaned_release
        return self

    def vote_cleaned(self):
        cleaned_votes = []
        for row in self['Number_of_votes']:
            if type(row) is int:
                cleaned_votes.append(row)
            else:
                clean = row.split('\n')[0]
                clean = clean.replace(',', '').strip()
                clean = clean.replace('~data not found~', '0')
                cleaned_votes.append(int(clean))
        self['Number_of_votes'] = cleaned_votes
        return self

    def country_cleaned(self):
        country = []
        for row in self['Country']:
            row = row.replace('\nCountry:', '')
            row = row.replace('\n|', '').split('\n')
            try:
                country.append(row[1:-1])
            except:
                country.append(row)
        self['Country'] = country
        return self

    def lang_cleaned(self):
        lang = []
        for row in self['Language']:
            row1 = row.replace('\nLanguage:', '')
            row1 = row1.replace('\n|', '').split('\n')
            if row != ' ~data not found~ ':
                lang.append(row1[1:-1])
            else:
                lang.append(row)
        self['Language'] = lang
        return self



    #def save_items(self):
        #"""Saves dataframe to csv file in directory"""
        #self.to_csv(r'cleaned_chart.csv', index=False, header=True)


def clean(movie_data):
    #movie_data = movie_data.replace(' ~data not found~ ', np.NaN)
    g_cleaned = CL.genres(movie_data)
    rate_cleaned = CL.rated(g_cleaned)
    run_cleaned = CL.runtime(rate_cleaned)
    votes_cleaned = CL.vote_cleaned(run_cleaned)
    date_cleaned = CL.release(votes_cleaned)
    country_cleaned = CL.country_cleaned(date_cleaned)
    lang_cleaned = CL.lang_cleaned(country_cleaned)

    #release_cleaned = CL.release(run_cleaned)

    #cleaned = release_cleaned
    cleaned = lang_cleaned
    return cleaned

#def main(file)
    #import csv file
    #run clean
    #export back to csv

if __name__ == '__main__':
    main()

else: print(" Apply clean() to the dataframe to return a cleaned version "
            "\n e.g. df_clean = movie_cleaning.clean(df) ")
###
