import requests
from bs4 import BeautifulSoup, ResultSet
import pandas as pd

base_url = 'https://www.metacritic.com'
chart_href = '/browse/movies/score/metascore/all/filtered?sort=desc'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

class MC:
    """MC extracts movie charts and movie information from www.metacritic.com"""

    base_url = 'https://www.metacritic.com'
    chart_href = '/browse/movies/score/metascore/all/filtered?sort=desc'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    def chart_soup(self):
        r_mc = requests.get(self, headers=headers)
        soup_mc = BeautifulSoup(r_mc.text, 'html.parser')
        mc_blocks = soup_mc.find_all('td', class_='clamp-summary-wrap')
        return mc_blocks

    def movies_soup(self):
        mc_links = []
        for movie in self:
            info = movie.find('a', class_='title')
            if info.has_attr('href'):
                full_url = base_url + info.attrs['href'] + '/details'
                mc_links.append(full_url)

        mc_movies_soup = []
        for link in mc_links:
            r_movie = requests.get(link, headers=headers)
            movie_soup = BeautifulSoup(r_movie.text, 'html.parser')
            movieinfo = movie_soup.find('div', class_="next_to_side_col")
            mc_movies_soup.append(movieinfo)
        return mc_movies_soup


    def movie_parse(self):
        mc_movie_details = []
        for info in self:
            try:
                genre_block = info.find('tr', class_='genres')
                genre = genre_block.find('td', class_='data').get_text().strip().replace('\n', '')
            except:
                genre = ' Data not available '
            try:
                rated_block = info.find('tr', class_='movie_rating')
                rated = rated_block.find('td', class_='data').get_text().strip().replace('\n', '')
            except:
                rated = ' Data not available '
            try:
                runtime_block = info.find('tr', class_='runtime')
                runtime = runtime_block.find('td', class_='data').get_text().strip().replace('\n', '')
            except:
                runtime = ' (Data not available) '
            try:
                released = info.find('span', class_='release_date').get_text().strip().replace('\n', '')
            except:
                released = ' Data not available '

            details_data = {"Genre": genre, "Rated": rated, 'Runtime': runtime, 'Release Date': released}
            mc_movie_details.append(details_data)
        return mc_movie_details

    def chart_parse(self):
        metacritic = []
        for index in range(len(self)):
            title = self[index].find('h3').get_text()
            rank = index + 1
            rating = int(self[index].find('a', class_='metascore_anchor').get_text().strip()) / 100
            mc_data = {"Movie_Rank": rank, "Movie_Title": title, 'Movie_Rating': rating}
            metacritic.append(mc_data)
        return metacritic

    def framed(self, self2):
        frame1 = pd.DataFrame(self)
        frame2 = pd.DataFrame(self2)
        full_frame = frame1.join(frame2)
        return full_frame

    def save_items(self):
        """Saves dataframe to csv file in directory"""
        self.to_csv(r'metacritic_chart.csv', index = False, header=True)

def main():
    print('Processing...please wait...')
    url = base_url + chart_href
    chart_soup = MC.chart_soup(url)
    movies_soup = MC.movies_soup(chart_soup)
    chart_parse = MC.chart_parse(chart_soup)
    movie_parse = MC.movie_parse(movies_soup)
    full_df = MC.framed(chart_parse, movie_parse)
    #df2 = MC.framed(movie_parse)
    #full_df = df1.join(df2)
    MC.save_items(full_df)
    print("Scraping complete. Metacritic chart data saved to csv file in directory")

def scrape():
    print('Processing...please wait...')
    url=base_url+chart_href
    chart_soup = MC.chart_soup(url)
    movies_soup = MC.movies_soup(chart_soup)
    chart_parse = MC.chart_parse(chart_soup)
    movie_parse = MC.movie_parse(movies_soup)
    full_df = MC.framed(chart_parse, movie_parse)
    #df1 = MC.framed(chart_parse)
    #df2 = MC.framed(movie_parse)
    #full_df = df1.join(df2)
    print(("Scraping complete. Hopefully you remembered to assign a variable ;)"))
    return full_df


if __name__ == '__main__':
    main()

else: print(" Call the function scrape() from the mc_collect module, and assign it to a variable"
            "\n e.g. df = mc_collect.scrape() ")
