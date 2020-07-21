import requests
from bs4 import BeautifulSoup
import pandas as pd




base_url = 'https://www.imdb.com'
#search_url = '/search/title/?title_type=feature&release_date=1980-01-01,2020-01-01&sort=release_date,desc&count=250'
#search_url = '/search/title/?title_type=feature&release_date=1980-01-01,2020-01-01&sort=release_date,desc&count=250&after=WzEzNjg0ODk2MDAwMDAsInR0MjY3NDEyNCIsNzM3NTFd'
#search_url = '/search/title/?title_type=feature&release_date=1980-01-01,2020-01-01&sort=release_date,desc&count=250&after=WzEyNjgzNTIwMDAwMDAsInR0MTYxNzI1MCIsMTAwMDAxXQ%3D%3D'
#search_url = '/search/title/?title_type=feature&release_date=1980-01-01,2020-01-01&sort=release_date,desc&count=250&after=WzQxMDkxODQwMDAwMCwidHQwMjYwMjA2IiwyMTI3NTFd'
search_url = '/search/title/?title_type=feature&release_date=1980-01-01,2020-01-01&sort=release_date,desc&count=250&after=WzMyMDYzMDQwMDAwMCwidHQwMDgwNjQ1IiwyMjI1MDFd'
cut_url = '/search/title/?title_type=feature&release_date=1980-01-01,2020-01-01&sort=release_date,desc&count=250&start=10001&ref_=adv_nxt'
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
        self.a = 853

    def page_parse(self, soup):
        page_movies = soup.find_all('h3', class_="lister-item-header")
        for box in page_movies:
            info = box.find('a')
            title = info.get_text()
            link = base_url + info.attrs['href']
            basics = {'Title':title, 'URL':link}
            self.mega_list.append(basics)

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
        if self.a == 895:
        #if url == self.end_url:
            return

        r_imdb_page = requests.get(url)
        soup = BeautifulSoup(r_imdb_page.text, 'html.parser')
        return self.page_parse(soup)

    def crawl_scrape(self):
        """Starts the scraping process"""
        self.page_soup(self.start_url)

    def save_items(self):
        dataframe = pd.DataFrame(self.mega_list)
        dataframe.to_csv(r'imdb_movies_endtest.csv', index=False, header=True)
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
