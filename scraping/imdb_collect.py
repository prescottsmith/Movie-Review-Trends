# Importing packages
import requests
from bs4 import BeautifulSoup
import pandas as pd


base_url = 'https://www.imdb.com'
top250 = '/chart/top/?ref_=nv_mv_250'

class IMDB:
    """IMDB extracts imdb charts and movie information from www.imdb.com"""

    def chart_soup(self):
        r_imdb = requests.get(self)
        soup_imdb = BeautifulSoup(r_imdb.text, 'html.parser')
        return soup_imdb

    def chart_movies(self):
        imdb_movies = self.find_all('td', class_="titleColumn")
        return imdb_movies

    def chart_parse(self):
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
        return imdb


    def movies_soup(self):
        imdb_links = []
        for movie in self:
            link = movie.find('a')
            if link.has_attr('href'):
                full_url = base_url + link.attrs['href']
                imdb_links.append(full_url)

        imdb_movies_soup = []
        for index in range(len(imdb_links)):
            r_movie = requests.get(imdb_links[index])
            movie_soup = BeautifulSoup(r_movie.text, 'html.parser')
            movieinfo = movie_soup.find('div', class_="subtext").get_text()
            imdb_movies_soup.append(movieinfo)
        return imdb_movies_soup

    def movie_parse(self):
        imdb_details = []
        for movie in self:
            details = movie.split(sep='|')
            genre = details[2].strip().replace('\n','')
            rated = details[0].strip()
            runtime = details[1].strip()
            released = details[-1].strip()
            details_data = {"Genre": genre, "Rated": rated, 'Runtime': runtime, 'Release Date': released}
            imdb_details.append(details_data)
        return imdb_details

    def framed(self, self2):
        frame1 = pd.DataFrame(self)
        frame2 = pd.DataFrame(self2)
        full_frame = frame1.join(frame2)
        return full_frame

    def save_items(self):
        """Saves dataframe to csv file in directory"""
        self.to_csv(r'imdb_chart.csv', index = False, header=True)



##############
# TEST CASES #
##############



##############


def scrape():
    print('Processing...please wait...')
    url=base_url+top250
    chart_soup = IMDB.chart_soup(url)
    chart_movies = IMDB.chart_movies(chart_soup)
    movies_soup = IMDB.movies_soup(chart_movies)
    chart_parse = IMDB.chart_parse(chart_soup)
    movie_parse = IMDB.movie_parse(movies_soup)
    full_df = IMDB.framed(chart_parse, movie_parse)
    print(("IMDB scraping complete."))
    return full_df

def main():
    full_df = scrape()
    IMDB.save_items(full_df)
    print("IMDB chart data saved to csv file in directory")


if __name__ == '__main__':
    main()

else: print(" Call the function scrape() from the imdb_collect module, and assign it to a variable"
            "\n e.g. df = imdb_collect.scrape() ")

