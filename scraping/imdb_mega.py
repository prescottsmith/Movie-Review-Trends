import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np




base_url = 'https://www.imdb.com'
search_url = '/search/title/?title_type=feature&release_date=1950-01-01,2019-12-31&sort=release_date,desc&count=250'
cut_url = '/search/title/?title_type=feature&release_date=1950-01-01,2019-12-31&sort=release_date,desc&count=250&start=10001&ref_=adv_nxt'
start_url = base_url + search_url
end_url = base_url + cut_url

class IMDBcrawler:
    """IMDB extracts movie information from www.imdb.com"""

    def __init__(self,
                   start_url= base_url+search_url,
                   end_url=None):
        self.start_url = start_url
        self.end_url = end_url
        self.mega_list = []
        self.a = 0

    def page_parse(self, soup):
        #page_movies = soup.find_all('h3', class_="lister-item-header")
        page_movies = soup.find_all('div', class_="lister-item-content")

        for chunk in page_movies:
            header = chunk.find('h3', class_="lister-item-header")
            header_info = header.find('a')
            title = header_info.get_text()
            link = base_url + header_info.attrs['href']
            imdb_rating = IMDBcrawler.rating(chunk)
            no_votes = IMDBcrawler.votes(chunk)
            runtime = IMDBcrawler.runtime(chunk)
            genres = IMDBcrawler.genres(chunk)
            mpaa = IMDBcrawler.mpaa(chunk)
            metascore = IMDBcrawler.metascore(chunk)

            data = {'Title':title,
                      'URL':link,
                      'IMDB_Rating':imdb_rating,
                      'Number_of_votes':no_votes,
                      'Runtime':runtime,
                      'Genre':genres,
                      'MPAA/TV_Rating':mpaa,
                      'Metascore (*)':metascore,
                      'Source':'IMDB'}
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
            meta = np.NaN
        return meta



    def save_items(self):
        dataframe = pd.DataFrame(self.mega_list)
        dataframe.to_csv(r'Data/imdb_giant_raw.csv', index=False, header=True)
        self.mega_list = []




##############


def main():
    start_url = base_url + search_url
    end_url = base_url + cut_url
    imdb = IMDBcrawler(start_url=start_url, end_url=end_url)
    imdb.crawl_scrape()
    imdb.save_items()

if __name__ == '__main__':
    main()
