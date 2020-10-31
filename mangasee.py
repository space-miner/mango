import html
import utils

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from database import DatabaseManager

class MangaSee:
    base_url = 'https://mangasee123.com'
    directory_url = f'{base_url}/directory/'
    db = DatabaseManager('mangasee.db')

    def __init__(self):
        pass


    def _soupify(self, url):
        '''
        Args:
            url: Link you want a soup of.

        Returns:
            A soup of the link (BeautifulSoup object).
        '''
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
        '''
        Saves an image from a direct link.

        Args:
            url: Link to the image.

        Returns:
            None.
        '''
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
    
    
    def _create_directory_database(self):
        '''
        Creates mangasee database.

        Args:
            None.

        Returns:
            None.
        '''
        self.db.create_table('mangasee', {
            'id': 'integer primary key autoincrement',
            'title_id': 'text not null',
            'manga_id': 'text not null',
            'manga_url': 'text',
            'cover_url': 'text'})


    def _add_manga(self, manga_data):
        '''
        Adds manga to directory database.

        Args:
            manga_data: Manga information (dict).

        Returns:
            None.
        '''
        self.db.add('mangasee', manga_data)

    
    def update(self):
        '''
        Update directory database, dictionary of title-manga pairs.

        Args:
            None.

        Returns:
            None.
        '''
        self._create_directory_database()
        soup = self._soupify(self.directory_url)
        data = soup.find_all('a', 'ttip ng-binding')
        for series in data:
            title_id = series.string
            manga_id = series['href'].split('/')[-1]
            manga_url = f'''{self.base_url}{series['href']}'''
            manga_html = series['title']
            manga_soup = BeautifulSoup(manga_html, 'html.parser')
            cover_url = manga_soup.img['src']
            manga = {
                'title_id': title_id, 
                'manga_id': manga_id, 
                'manga_url': manga_url,
                'cover_url': cover_url}
            self._add_manga(manga)


    def get_chapter(self, title, ch):
        '''
        Populates chapter pages with direct link to page image.
        
        Args:
            ch: chapter number.

        Returns:
            None.
        '''
        search = self.db.select('mangasee', {'title_id': title})
        if len(search) == 1:
            id_, title_id, manga_id, manga_url, cover_url = search[0]
        chapter_url = f'{self.base_url}/read-online/{manga_id}-chapter-{ch}.html'
        soup = self._soupify(chapter_url)
        for page in soup.find_all('img', 'img-fluid'):
            url = page['src']
            self._save_image(url)
        utils.convert_to_pdf(ch)
        utils.remove_images()
