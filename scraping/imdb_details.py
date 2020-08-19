import requests
from bs4 import BeautifulSoup
import pandas as pd
from cleaning import movie_cleaning

raw_df = pd.read_csv('Data/imdb_giant_raw.csv', encoding = "ISO-8859-1").copy()
base_df = raw_df[raw_df['IMDB_Rating']!=' ~data not found~ ']
base_df = movie_cleaning.clean(base_df.copy())
base_df = base_df[base_df['Number_of_votes']>1000]
base_df = base_df.reset_index(drop=True)
base_df.to_csv(r'Data/imdb_giant_trimmed.csv', index=False, header=True)
country = []
lang = []
rdate = []
class IMDBdetails:
    """IMDBdetails extracts extra movie information from www.imdb.com"""

    def __init__():
        country = []
        lang = []
        rdate = []

    def prep():
        raw_df = pd.read_csv('Data/imdb_giant_raw.csv', encoding="ISO-8859-1").copy()
        base_df = raw_df[raw_df['IMDB_Rating'] != ' ~data not found~ ']
        base_df = movie_cleaning.clean(base_df.copy())
        base_df = base_df[base_df['Number_of_votes'] > 1000]
        base_df.to_csv(r'Data/imdb_giant_trimmed.csv', index=False, header=True)
        base_df = base_df.reset_index(drop=True)
        return base_df


    def add_info(self):
        details = []
        a = 0
        for link in self['URL']:
            r_movie = requests.get(link)
            soup = BeautifulSoup(r_movie.text, 'html.parser')
            blocks = soup.find_all('div', class_='txt-block')
            print('sourcing info from ' + link)
            title = soup.find('h1').get_text()
            for divs in blocks:

                try:
                    if divs.find('h1').get_text() == 'Country:':
                        country = divs.get_text()
                        break

                except:
                    country = ' ~data not found~ '

                try:
                    if divs.find('h4').get_text() == 'Country:':
                        country = divs.get_text()
                        break

                except:
                    country = ' ~data not found~ '


            for divs in blocks:
                try:
                    if divs.find('h4').get_text() == 'Language:':
                        lang = divs.get_text()
                        break
                except:
                    lang = ' ~data not found~ '

            for divs in blocks:
                try:
                    if divs.find('h4').get_text() == 'Release Date:':
                        rdate = divs.get_text()
                        break
                except:
                    rdate = ' ~data not found~ '

            print(title)
            info = {'Title (w/ year)':title, 'Country':country, 'Language':lang, 'Release_Date':rdate}
            details.append(info)
            #print(details)
            IMDBdetails.save_items(details)
            a = a+1
            print('Movie details added: ' + str(a))
        details = pd.DataFrame(details)
        full_frame = self.join(details)
        return full_frame


    def save_items(self, path=r'Data/imdb_giant_details_raw.csv'):
        dataframe = pd.DataFrame(self)
        dataframe.to_csv(path, index=False, header=True)




########

def main():
    prepped = IMDBdetails.prep()
    df = IMDBdetails.add_info(prepped)
    IMDBdetails.save_items(df, path=r'Data/imdb_complete_raw.csv')
    print('movie details added')


if __name__ == '__main__':
    main()



