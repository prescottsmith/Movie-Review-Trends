# Importing packages
import requests
from bs4 import BeautifulSoup, ResultSet
import pandas as pd

class IMDBscraper:
    """IMDBscraper extracts imdb charts and movie information from www.imdb.com

    Instantiate IMDBscraper then run the .imdb_scrape() method"""

    base_url = 'https://www.imdb.com'

    url_imdb = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    top250 = '/chart/top/?ref_=nv_mv_250'

    def __init__(self):
        self.url = base_url+top250

    def parse_chart(self):
        """Extracts imdb chart data from HTTP response.
        Outputs a list of dictionaries containing:
        The movie's rank
        The movie's title
        The movie's rating/review"""
        imdb_movies = self.find_all('td', class_="titleColumn")
        imdb_ratings = [b.attrs.get('data-value') for b in self.select('td.posterColumn span[name=ir]')]

        imdb = []
        for index in range(len(imdb_movies)):
            block_text = imdb_movies[index].get_text()
            rank = index + 1
            # rank = int(block_text.splitlines()[1].replace('.','').strip()) <-- realised I didn't need this
            title = block_text.splitlines()[2].strip()
            rating = float(imdb_ratings[index]) / 10
            imdb_data = {"Movie_Rank": rank, "Movie_Title": title, 'Movie_Rating': rating}
            imdb.append(imdb_data)

        imdb_links = []
        for index in range(len(imdb_movies)):
            link = imdb_movies[index].find('a')
            if link.has_attr('href'):
                full_url = base_url + link.attrs['href']
                imdb_links.append(full_url)

    def get_response(self, url=base_url+top250):
        """Generates HTTP response and turns it into useable soup"""
        response = requests.get(url)
        soup_imdb = BeautifulSoup(response.text, 'html.parser')
        return self.parse_chart(soup_imdb)

    def scrape(self):
        """Starts the scraping process"""
        self.get_response(self.url)

    def framed(self):
        """Converts list of dictionaries into a dataframe"""

if __name__ == '__main__':
    scraper = IMDBscraper(url=url)
    scraper.scrape()
    scraper.framed()
    df_imdb = pd.DataFrame(imdb)
    return df_imdb
    print("DataFrame Created")