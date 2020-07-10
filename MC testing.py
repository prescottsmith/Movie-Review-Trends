import requests
from bs4 import BeautifulSoup, ResultSet
import pandas as pd

base_url = 'https://www.metacritic.com'
chart_href = '/browse/movies/score/metascore/all/filtered?sort=desc'

url = base_url + chart_href

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

r_mc = requests.get(url, headers=headers)
soup_mc = BeautifulSoup(r_mc.text, 'html.parser')
mc_blocks = soup_mc.find_all('td', class_='clamp-summary-wrap')

mc_links = []
for movie in mc_blocks:
    info = movie.find('a', class_='title')
    if info.has_attr('href'):
        full_url = base_url + info.attrs['href'] + '/details'
        mc_links.append(full_url)

mc_movies_soup = []
for link in mc_links:
    r_movie = requests.get(link, headers=headers)
    movie_soup = BeautifulSoup(r_movie.text, 'html.parser')
    movieinfo = movie_soup.find('div', class_="next_to_side_col")
    # movieinfo = movie_soup.find('table', class_="details")
    mc_movies_soup.append(movieinfo)

mc_movie_details = []
for info in mc_movies_soup:
    try:
        genre_block = info.find('tr', class_='genres')
        genre = genre_block.find('td', class_='data').get_text().strip().replace('\n','')
    except:
        genre = ' Data not available '
    try:
        rated_block = info.find('tr', class_='movie_rating')
        rated = rated_block.find('td', class_='data').get_text().strip().replace('\n','')
    except:
        rated = ' Data not available '
    try:
        runtime_block = info.find('tr', class_='runtime')
        runtime = runtime_block.find('td', class_='data').get_text().strip().replace('\n','')
    except:
        runtime = ' Data not available '
    try:
        released = info.find('span', class_='release_date').get_text().strip().replace('\n','')
    except:
        released = ' Data not available '

    details_data = {"Genre": genre, "Rated": rated, 'Runtime': runtime, 'Release Date': released}
    mc_movie_details.append(details_data)

