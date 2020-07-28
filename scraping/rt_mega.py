import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

base_url = 'https://www.rottentomatoes.com'
search_url = '/browse/dvd-streaming-all/'


class RTcrawler:
    """RTcrawler extracts movie information from www.rottentomatoes.com"""

    def __init__(self,
                   start_url= base_url+search_url,
                   end_url=None):
        self.start_url = start_url
        self.end_url = end_url
        self.mega_list = []
        self.a = 0

    def page_parse(self, soup):
        #page_movies = soup.find_all('h3', class_="lister-item-header")
        page_movies = soup.find_all('div', class_="movie_info")

        for chunk in page_movies:
            title = chunk.find('h3', class_="movieTitle").get_text()
            link_info = chunk.find('a')
            link = base_url + link_info.attrs['href']
            rt_critic = chunk.find('span', class_='tMeterScore').get_text()

            data = {'Title':title,
                      'URL':link,
                      'RT_Critic_Rating':rt_critic,
                      'Source':'Rotten Tomatoes'}
            self.mega_list.append(data)

        self.a = self.a+1
        print('Scraped page ' + str(self.a))
        try:
            next = soup.find('a', class_='lister-page-next next-page')
            new_url = base_url + next.attrs['href']
            print('Next page url is ' + new_url)
            return self.page_soup(new_url)
        except:
            print('Could not find new link')
            return

    def page_soup(self, url):
        if self.a == 893:
        #if url == self.end_url:
            return

        r_imdb_page = requests.get(url)
        soup = BeautifulSoup(r_imdb_page.text, 'html.parser')
        return self.page_parse(soup)

    def crawl_scrape(self):
        """Starts the scraping process"""
        self.page_soup(self.start_url)

    def rating(soup_chunk):
        try:
            value = soup_chunk.find('strong').get_text()
        except:
            value = ' ~data not found~ '
        return value

    def votes(soup_chunk):
        try:
            votes = soup_chunk.find('p', class_='sort-num_votes-visible').get_text()
            votes = votes.split(':')[1].strip()
        except:
            votes = ' ~data not found~ '
        return votes

    def runtime(soup_chunk):
        try:
            time = soup_chunk.find('span', class_='runtime').get_text()
        except:
            time = ' ~data not found~ '
        return time

    def genres(soup_chunk):
        try:
            genre = soup_chunk.find('span', class_='genre').get_text()
        except:
            genre = ' ~data not found~ '
        return genre

    def mpaa(soup_chunk):
        try:
            rating = soup_chunk.find('span', class_='certificate').get_text()
        except:
            rating = ' ~data not found~ '
        return rating

    def metascore(soup_chunk):
        try:
            meta = soup_chunk.find('div', class_='inline-block ratings-metascore').get_text()
            meta = meta.split('\n')[1].strip()
        except:
            meta = ' ~data not found~ '
        return meta



    def save_items(self):
        dataframe = pd.DataFrame(self.mega_list)
        dataframe.to_csv(r'imdb_raw.csv', index=False, header=True)
        self.mega_list = []




##############


def main():
    start_url = base_url + search_url
    end_url = base_url + cut_url
    rt = RTcrawler(start_url=start_url, end_url=end_url)
    rt.crawl_scrape()
    rt.save_items()

if __name__ == '__main__':
    main()