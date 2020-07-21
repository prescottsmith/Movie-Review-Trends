import pandas
from pytimeparse.timeparse import timeparse
import dateutil.parser as dparser
import re

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
        return self

    def genres(self):
        cleaned_genres = []
        for genres in self['Genre']:
            list = re.split(r'[,&]', genres)
            row = []
            for item in list:
                if item==' Suspense':
                    continue
                new = item.replace(' ', '')
                row.append(new)
            cleaned_genres.append(row)
        self['Genre'] = cleaned_genres
        return self


    def rated(self):
        cleaned_rating = []
        for row in self['Rated']:
            row = ' ' + row + ' '
            new_rating = ''.join([rating for rating in ratings_list if rating in row]).strip()
            new_rating = CL.ratings_update(new_rating)
            cleaned_rating.append(new_rating)
        self['Rated'] = cleaned_rating
        return self

    def runtime(self):
        cleaned_runtime = []
        for row in self['Runtime']:
            row = row.replace(' ', '')
            row = row.replace('minutes', 'm')
            row = row.replace('min', 'm')
            try:
                minutes = timeparse(row)/60
            except:
                minutes = 0
            cleaned_runtime.append(minutes)
        self['Runtime'] = cleaned_runtime
        return self

    def release(self):
        cleaned_release = []
        for row in self['Release Date']:
            scrub = row.replace('Release Date', '')
            date = dparser.parse(scrub, fuzzy=True).date()
            cleaned_release.append(date)
        self['Release Date'] = cleaned_release
        return self

    #def save_items(self):
        #"""Saves dataframe to csv file in directory"""
        #self.to_csv(r'cleaned_chart.csv', index=False, header=True)


def clean(movie_data):
    g_cleaned = CL.genres(movie_data)
    rate_cleaned = CL.rated(g_cleaned)
    run_cleaned = CL.runtime(rate_cleaned)
    release_cleaned = CL.release(run_cleaned)

    cleaned = release_cleaned
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
