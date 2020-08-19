import requests
from bs4 import BeautifulSoup
import pandas as pd
from cleaning import movie_cleaning
import numpy as np
import math


imdb_full_raw = pd.read_csv('Data/imdb_complete_raw.csv', encoding = "ISO-8859-1").copy()




class RT:
    """RT extracts extra movie rating information from www.rottentomatoes.com"""

    def setup():
        imdb_full_raw = pd.read_csv('Data/imdb_complete_raw.csv', encoding="ISO-8859-1").copy()
        new_frame = movie_cleaning.clean(imdb_full_raw)
        #new_frame = new_frame.iloc[[6577]].reset_index()
        decade = []
        year = []
        month = []
        for rdate in new_frame['Release_Date']:
            annum = pd.to_datetime(rdate).year
            mon = pd.to_datetime(rdate).month
            dec = (annum // 10) * 10
            year.append(annum)
            decade.append(dec)
            month.append(mon)

        new_frame['Month'] = (month)
        new_frame['Year'] = year
        new_frame['Decade'] = decade
        return new_frame

    def extraction(soup):
        critic_box = soup.find('div', class_='mop-ratings-wrap__half')
        audience_box = soup.find('div', class_='mop-ratings-wrap__half audience-score')
        try:
            critic = critic_box.find('span', class_='mop-ratings-wrap__percentage').get_text().strip().replace('%','')
            critic_no = critic_box.find('small', class_='mop-ratings-wrap__text--small').get_text().strip()
        except:
            critic = 'N/A'
            critic_no = 'N/A'
        try:
            audience = audience_box.find('span', class_='mop-ratings-wrap__percentage').get_text().strip().replace('%','')
            audience_no = audience_box.find('strong', class_='mop-ratings-wrap__text--small').get_text().strip()
            audience_no = audience_no.replace('User Ratings: ', '')
            audience_no = audience_no.replace('Verified Ratings: ', '')
            audience_no = audience_no.replace(',', '')
        except:
            audience = 'N/A'
            audience_no = 'N/A'
        name = soup.find('h1', class_='mop-ratings-wrap__title mop-ratings-wrap__title--top').get_text()
        info = {'Title_(RT)': name, 'RT_critic': float(critic), 'RT_critic_votes': float(critic_no), 'RT_audience': float(audience),
                'RT_audience_votes': float(audience_no)}
        return info

    def add_tomatoes(self):
        details = []
        a = 0
        year_rows = self['Year']
        for title in self['Title']:
            print('Checking for RT ratings for ' + title)
            suffix = title.replace(' ', '_')
            suffix = suffix.replace(':', '')
            suffix = suffix.replace(" '", '')
            suffix = suffix.replace("' ", '')
            suffix = suffix.replace("'", '')
            suffix = suffix.replace('.', '')
            suffix = suffix.replace(',', '')
            suffix = suffix.replace('*', '')
            suffix = suffix.replace('-', '_')
            suffix = suffix.replace('&', 'and')
            link = 'https://www.rottentomatoes.com/m/' + suffix
            r_movie = requests.get(link)
            rt_soup = BeautifulSoup(r_movie.text, 'html.parser')
            try:
                info = RT.extraction(rt_soup)

            except:
                if math.isnan(year_rows[a]):
                    print('WOOPS! NO MOVIE FOUND!')
                    name = title + ' (no page found)'
                    critic = 'N/A'
                    critic_no = 'N/A'
                    audience = 'N/A'
                    audience_no = 'N/A'
                    info = {'Title_(RT)': name, 'RT_critic': critic, 'RT_critic_votes': critic_no,
                            'RT_audience': audience, 'RT_audience_votes': audience_no}
                else:
                    yr = '_' + str(int(year_rows[a]))
                    link = 'https://www.rottentomatoes.com/m/' + suffix + yr
                    r_movie = requests.get(link)
                    rt_soup = BeautifulSoup(r_movie.text, 'html.parser')
                    try:
                        info = RT.extraction(rt_soup)

                    except:
                        print('WOOPS! NO MOVIE FOUND!')
                        name = title + ' (no page found)'
                        critic = 'N/A'
                        critic_no = 'N/A'
                        audience = 'N/A'
                        audience_no = 'N/A'
                        info = {'Title_(RT)': name, 'RT_critic': critic, 'RT_critic_votes': critic_no,
                                'RT_audience': audience, 'RT_audience_votes': audience_no}

            details.append(info)
            #print(details)
            RT.save_items(details)
            a = a+1
            print('RT data added: ' + str(a))
        details = pd.DataFrame(details)
        full_frame = self.join(details)
        return full_frame




    def save_items(self, path='Data/rt_details_raw_1.csv'):
        dataframe = pd.DataFrame(self)
        dataframe.to_csv(path, index=False, header=True)




########

def main():
    ready = RT.setup()
    df = RT.add_tomatoes(ready)
    RT.save_items(df, path='Data/movies_complete_raw.csv')
    print('RT meter data added')


if __name__ == '__main__':
    main()