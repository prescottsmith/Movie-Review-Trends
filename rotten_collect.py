import requests
from bs4 import BeautifulSoup
import pandas as pd

url_rt='https://www.rottentomatoes.com/top/bestofrt/'
base_url = 'https://www.rottentomatoes.com'

r_rt = requests.get(url_rt)
soup_rt = BeautifulSoup(r_rt.text)


#confining html scraping to the main section so as to avoid scraping extra unwanted data
rt_body = soup_rt.find('section', id="top_movies_main")

#collecting movie and rating info
rt_movies = rt_body.select('a.unstyled.articleLink')
rt_ratings = rt_body.select('td span[class=tMeterScore]')



#Parsing html data into a dataframe
rottentomatoes = []

for index in range(0, len(rt_movies)):
    title = rt_movies[index].get_text().splitlines()[1].strip()[:-7]
    #i removed the year info from the title to match imdb and mc
    rank = index+1
    rating = int(rt_ratings[index].get_text().strip().replace('%',''))/100
    rt_data={"Movie_Rank":rank, "Movie_Title":title, 'Movie_Rating':rating}
    rottentomatoes.append(rt_data)

df_rt = pd.DataFrame(rottentomatoes)

#Scraping individual movie information
rt_links = []
for index in range(len(rt_movies)):
    link = rt_movies[index]
    if link.has_attr('href'):
        full_url = base_url + link.attrs['href']
        rt_links.append(full_url)


rt_movie_soup = []
for movie in rt_links:
    r_movie = requests.get(movie)
    movie_soup = BeautifulSoup(r_movie.text)
    movieinfo = movie_soup.find_all('div', class_="meta-value")
    rt_movie_soup.append(movieinfo)



rt_movie_details = []
for info in rt_movie_soup:
    genre = info[1].get_text().splitlines()
    genre = ' '.join(genre).strip()
    rated = info[0].get_text().strip()
    runtime = info[-2].get_text().strip()
    released = info[4].get_text().strip()
    details_data = {"Genre": genre, "Rated": rated, 'Runtime':runtime, 'Release Date': released}
    rt_movie_details.append(details_data)

df_rt_details = pd.DataFrame(rt_movie_details)

#Combining movie information with charts
df_rt_full = df_rt.join(df_rt_details)

class RTscraper:
    """IMDBscraper extracts imdb charts and movie information from www.imdb.com

    Instantiate IMDBscraper then run the .imdb_scrape() method"""
    import requests
    from bs4 import BeautifulSoup, ResultSet
    import pandas as pd

    base_url = 'https://www.rottentomatoes.com'
    chart_href = '/top/bestofrt/'
    def chart_soup():
        r_rt = requests.get(base_url+chart_href)
        soup_rt = BeautifulSoup(r_rt.text)
        rt_body = soup_rt.find('section', id="top_movies_main")
        return rt_body

    def movie_soup(self):
        rt_movies = self.select('a.unstyled.articleLink')

        rt_links=[]
        for movie in rt_movies:
            if movie.has_attr('href'):
                full_url = base_url + link.attrs['href']
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

    def framed(self):
        frame = pd.DataFrame(self)
        return frame

    def save_items(self):
        """Saves dataframe to csv file in directory"""

    def main():
        chart_soup = chart_soup()
        movie_soup = movie_soup(chart_soup)
        chart_parse = chart_parse(chart_soup)
        movie_parse = movie_parse(chart_parse)
        df1 = framed(chart_parse)
        df2 = framed(movie_parse)
        main_df = df1.join(df2)
        main_df.save_items()
        print("Scraping complete. Rotten Tomatoes chart data saved to csv file in directory")

    def scrape():
        chart_soup = chart_soup()
        movies_soup = movies_soup(chart_soup)
        chart_parse = chart_parse(chart_soup)
        movie_parse = movie_parse(movies_soup)
        df1 = framed(chart_parse)
        df2 = framed(movie_parse)
        main_df = df1.join(df2)
        print(("Scraping complete. Hopefully you remembered to assign this function to a variable"
              "so that the Rotten Tomatoes data frame is saved in your environment"))
        return main_df


if __name__ == '__main__'
    main()

else: print("call the rt_collect module and function scrape(), and assign it to a variable to save the scraped data"
               "to your environment")
