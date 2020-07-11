import requests
from bs4 import BeautifulSoup
import pandas as pd


base_url = 'https://www.imdb.com'
top250 = '/chart/top/?ref_=nv_mv_250'
url=base_url+top250

r_imdb = requests.get(url)
soup_imdb = BeautifulSoup(r_imdb.text, 'html.parser')

imdb_movies = soup_imdb.find_all('td', class_="titleColumn")
imdb_ratings = [b.attrs.get('data-value') for b in soup_imdb.select('td.posterColumn span[name=ir]')]

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
for movie in imdb_movies:
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

#######
imdb_details = []
for movie in imdb_movies_soup:
    details = movie.split(sep='|')
    genre = details[2].strip().replace('\n','')
    rated = details[0].strip()
    runtime = details[1].strip()
    released = details[-1].strip()
    details_data = {"Genre": genre, "Rated": rated, 'Runtime': runtime, 'Release Date': released}
    imdb_details.append(details_data)
#######

frame1 = pd.DataFrame(imdb)
frame2 = pd.DataFrame(imdb_details)
full_frame = frame1.join(frame2)


# Movie Rank 243 ('The Invisible Guest') has a parsing error
# Wrong data ends up in the fields due to missing information on the page
# See below for the difference in the html

print(imdb_movies_soup[4]) #Usual data format
print(imdb_movies_soup[242]) #Movie with missing information: leads to parsing error
#Currently I'm parsing the movie details using the '|' separator
#See the code between the #####