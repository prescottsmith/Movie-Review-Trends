# Importing packages
import requests
from bs4 import BeautifulSoup, ResultSet
import pandas as pd

class IMDBscraper:
    """IMDBscraper extracts imdb charts and movie information from www.imdb.com

    Instantiate IMDBscraper then run the .imdb_scrape() method"""
    import requests
    from bs4 import BeautifulSoup, ResultSet
    import pandas as pd
    def imdb_scrape():

        print('Processing...please wait...')
        base_url = 'https://www.imdb.com'

        top250 = '/chart/top/?ref_=nv_mv_250'

        url = base_url+top250

        def __init__(url):
            url = base_url+top250

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

            imdb_details = []
            for index in range(len(imdb_links)):
                r_movie = requests.get(imdb_links[index])
                movie_soup = BeautifulSoup(r_movie.text, 'html.parser')
                movieinfo = movie_soup.find('div', class_="subtext").get_text()
                genre = movieinfo.splitlines()[6].strip().replace(',',
                                                                  '')  # this only pulls the first genre listed. See below for more info
                rated = movieinfo.splitlines()[1].strip()
                runtime = movieinfo.splitlines()[3].strip()
                released = movieinfo.splitlines()[-2].strip()
                details_data = {"Genre": genre, "Rated": rated, 'Runtime': runtime, 'Release Date': released}
                imdb_details.append(details_data)

            frames = [imdb, imdb_details]
            return frames

        def get_response(self):
            """Generates HTTP response and turns it into useable soup"""
            response = requests.get(self)
            soup_imdb = BeautifulSoup(response.text, 'html.parser')
            return parse_chart(soup_imdb)

        def scrape(self):
            """Starts the scraping process"""
            return get_response(self)


        def framed(self):
            """Converts list of dictionaries into a dataframe"""
            df_imdb = pd.DataFrame(self[0])
            df_imdb_details = pd.DataFrame(self[1])
            df_imdb_full = df_imdb.join(df_imdb_details)
            return df_imdb_full

        result = framed(scrape(url))
        print("Scraping complete. Hopefully you remembered to assign this function to a variable"
              "so that the data frame is in your environment")
        return result



