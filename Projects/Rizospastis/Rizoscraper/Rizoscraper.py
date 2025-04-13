import requests, os, time
from bs4 import BeautifulSoup
import pandas as pd

class Scraper:
    def __init__(self, site):
        self.site = site
        self.links_to_download = []

    def get_links_to_download(self):
        print(f' 💡 On page: {self.site}')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        page = requests.get(self.site, headers=headers, timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')
        for link in soup.find_all('a'):
            if 'story.do?id=' in link.get('href') and not link.get('href').split('=')[1] == '6668139':
                self.links_to_download.append('https://www.rizospastis.gr/story.do?id=' + link.get('href').split('=')[1])
                print(f"    ✅ Article found: https://www.rizospastis.gr/story.do?id={link.get('href').split('=')[1]}")
        # time.sleep(3)
        self.chech_for_next_valid_page()

    def chech_for_next_valid_page(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        page = requests.get(self.site, headers=headers, timeout=5)
        soup = BeautifulSoup(page.content, 'html.parser')
        next_page_to_search_for =  'pageNo=' + str(int(self.site.split('pageNo=')[1]) + 1)
        valid_page_found = False
        for link in soup.find_all('a'):
            if next_page_to_search_for in link.get('href') and not valid_page_found:
                valid_page_found = True
                self.site = self.site.split('pageNo=')[0] + next_page_to_search_for
                self.get_links_to_download()
        if not valid_page_found:
            next_page_to_search_for =  'pageNo=' + str(int(self.site.split('pageNo=')[1]) + 2)
            for link in soup.find_all('a'):
                if next_page_to_search_for in link.get('href') and not valid_page_found:
                    valid_page_found = True
                    self.site = self.site.split('pageNo=')[0] + next_page_to_search_for
                    self.get_links_to_download()
        if not valid_page_found:
            next_page_to_search_for =  'pageNo=' + str(int(self.site.split('pageNo=')[1]) + 3)
            for link in soup.find_all('a'):
                if next_page_to_search_for in link.get('href') and not valid_page_found:
                    valid_page_found = True
                    self.site = self.site.split('pageNo=')[0] + next_page_to_search_for
                    self.get_links_to_download()
        if not valid_page_found:
            print('    ❌ No Article Found')

# for date in pd.date_range(start=pd.to_datetime('1995-01-01'), end=pd.to_datetime('today'), freq='d')[::-1]:
for date in pd.date_range(start=pd.to_datetime('today') - pd.DateOffset(days=10), end=pd.to_datetime('today'), freq='d')[::-1]:
    filename = os.path.join(os.path.dirname(__file__), 'Data', f'Rizospastis-{date.strftime("%Y-%m-%d")}')
    extension = '.csv'
    # if folder is not exist, create it
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'Data')):
        os.mkdir(os.path.join(os.path.dirname(__file__), 'Data'))
    if not os.path.exists(filename + extension):
        r = Scraper('https://www.rizospastis.gr/page.do?publDate=' + date.strftime('%d/%m/%Y')+'&pageNo=2')
        r.get_links_to_download()
        if len(r.links_to_download) != 0:
            df = pd.DataFrame(r.links_to_download, columns=['Links of Articles'])
            if extension == '.csv' or extension == '.txt':
                df.to_csv(filename + extension, index=False)
            elif extension == '.xlsx':
                df.to_excel(filename + '.xlsx', index=False)