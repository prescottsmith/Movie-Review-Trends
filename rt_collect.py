import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.rottentomatoes.com'
chart_href = '/top/bestofrt/'

class RT:
    """RT extracts rotten tomatoes charts and movie information from www.rottentomatoes.com"""

    base_url = 'https://www.rottentomatoes.com'
    chart_href = '/top/bestofrt/'

    def chart_soup(self):
        r_rt = requests.get(self)
        soup_rt = BeautifulSoup(r_rt.text, 'html.parser')
        rt_body = soup_rt.find('section', id="top_movies_main")
        return rt_body

    def movies_soup(self):
        rt_movies = self.select('a.unstyled.articleLink')

        rt_links = []
        for movie in rt_movies:
            if movie.has_attr('href'):
                full_url = base_url + movie.attrs['href']
                rt_links.append(full_url)

        rt_movies_soup = []
        for link in rt_links:
            r_movie = requests.get(link)
            movie_soup = BeautifulSoup(r_movie.text, 'html.parser')
            movieinfo = movie_soup.find_all('div', class_="meta-value")
            rt_movies_soup.append(movieinfo)
        return rt_movies_soup

    def movie_parse(self):
        rt_movie_details = []
        for info in self:
            genre = info[1].get_text().splitlines()
            genre = ' '.join(genre).strip()
            rated = info[0].get_text().strip()
            runtime = info[-2].get_text().strip()
            released = info[4].get_text().strip()
            details_data = {"Genre": genre, "Rated": rated, 'Runtime': runtime, 'Release Date': released}
            rt_movie_details.append(details_data)
        return rt_movie_details

    def chart_parse(self):
        rt_movies = self.select('a.unstyled.articleLink')
        rt_ratings = self.select('td span[class=tMeterScore]')
        rottentomatoes = []
        for index in range(len(rt_movies)):
            title = rt_movies[index].get_text().splitlines()[1].strip()[:-7]
            # i removed the year info from the title to match imdb and mc
            rank = index + 1
            rating = int(rt_ratings[index].get_text().strip().replace('%', '')) / 100
            rt_data = {"Movie_Rank": rank, "Movie_Title": title, 'Movie_Rating': rating}
            rottentomatoes.append(rt_data)
        return rottentomatoes

    def framed(self, self2):
        frame1 = pd.DataFrame(self)
        frame2 = pd.DataFrame(self2)
        full_frame = frame1.join(frame2)
        return full_frame

    def save_items(self):
        """Saves dataframe to csv file in directory"""
        self.to_csv(r'rottentomatoes_chart.csv', index = False, header=True)


##############
# TEST CASES #
##############


##############

def scrape():
    print('Processing...please wait...')
    url=base_url+chart_href
    chart_soup = RT.chart_soup(url)
    movies_soup = RT.movies_soup(chart_soup)
    chart_parse = RT.chart_parse(chart_soup)
    movie_parse = RT.movie_parse(movies_soup)
    full_df = RT.framed(chart_parse, movie_parse)
    print(("Rotten Tomatoes scraping complete."))
    return full_df

def main():
    full_df = scrape()
    RT.save_items(full_df)
    print("Rotten Tomatoes chart data saved to csv file in directory")


if __name__ == '__main__':
    main()

else: print(" Call the function scrape() from the rt_collect module, and assign it to a variable"
            "\n e.g. df = rt_collect.scrape() ")
