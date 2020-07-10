from imdb_collect import IMDBscraper
import rt_collect
import mc_collect



#Scrape IMDB
df_imdb = IMDBscraper.imdb_scrape()

#Scrape Rotten Tomatoes
df_rt = rt_collect.scrape()

#Scrape Metacritic
df_mc = mc_collect.scrape()



