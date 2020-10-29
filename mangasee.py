import html
import utils

from requests_html import HTMLSession
from bs4 import BeautifulSoup


class MangaSee:
    base_url = 'https://mangasee123.com'
    directory_url = f'{base_url}/directory/'
    directory = {}

    def __init__(self):
        pass


    def _soupify(self, url):
        for i in range(3):
            try:
                print(f'Pulling: {url}')
                session = HTMLSession()
                req = session.get(url)
                req.html.render(sleep=5)
                html = req.html.html
                return BeautifulSoup(html, 'html.parser')
            except:
                print('Failed network request | Retrying')


    def _save_image(self, url):
        for i in range(3):
            try:
                print(f'Pulling: {url}')
                session = HTMLSession()
                req = session.get(url)
                filename = url.split('/')[-1]
                with open(filename, 'wb') as f:
                    f.write(req.content)
                break
            except:
                print('Failed network request | Retrying')
    
    
    def get_directory(self):
        '''
        Populates directory, dictionary of title-manga pairs.

        Args:
            None.

        Returns:
            None.
        '''
        soup = self._soupify(self.directory_url)
        data = soup.find_all('a', 'ttip ng-binding')
        for series in data:
            title = series.string.lower()
            title_id = series.string
            manga_id = series['href'].split('/')[-1]
            manga_url = f'''{self.base_url}{series['href']}'''
            manga_html = series['title']
            manga_soup = BeautifulSoup(manga_html, 'html.parser')
            cover_url = manga_soup.img['src']
            self.directory[title] = {
                    'title_id': title_id, 
                    'manga_id': manga_id, 
                    'manga_url': manga_url,
                    'cover_url': cover_url,
                    'chapters': {}}


    def get_chapter(self, title, ch):
        '''
        Populates chapter pages with direct link to page image.
        
        Args:
            ch: chapter number.

        Returns:
            None.
        '''
        title = title.lower()
        manga = self.directory[title]
        manga_id = manga['manga_id']
        chapter_url = f'{self.base_url}/read-online/{manga_id}-chapter-{ch}.html'
        soup = self._soupify(chapter_url)
        manga['chapters'][ch] = [page['src'] for page in soup.find_all('img', 'img-fluid')]
        for url in manga['chapters'][ch]:
            self._save_image(url)
        utils.convert_to_pdf(ch)
        utils.remove_images()
