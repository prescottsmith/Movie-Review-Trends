import pandas


class CL:

    def genres(self):
        cleaned_genres = []
        for index in range(len(self['Genre'])):
            list = self[['Genre'][index].split(sep=',')
            row = []
            for item in list:
                new = item.replace(' ', '')
                row.append(new)
            cleaned_genres.append(row)
        self['Genre'] = cleaned_genres
        return self


    def rated(self):
        cleaned_rating = []
        for index in range(len(self['Rated'])):

        self['Rated'] = cleaned_rating
        return self

    def runtime(self):
        cleaned_runtime = []
        for index in range(len(self['Runtime'])):

        self['Runtim'] = cleaned_runtime
        return self

    def release(self):
        cleaned_release = []
        for index in range(len(self['Release Date'])):

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

def main(file)
    #import csv file
    #run clean
    #export back to csv

if __name__ == '__main__':
    main()


###

cleaned_genres = []
for index in range(len(df_mc['Genre'])):
    list = df_mc['Genre'][index].split(sep=',')
    row = []
    for item in list:
        new = item.replace(' ','')
        row.append(new)
    cleaned_genres.append(row)

df_mc['Genre'] = cleaned_genres