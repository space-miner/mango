import html
import sys
import utils

from requests_html import HTMLSession
from bs4 import BeautifulSoup
from database import DatabaseManager

class MangaSee:
    def __init__(self):
        self.base_url = 'https://mangasee123.com'
        self.directory_url = f'{self.base_url}/directory/'
        self.database = DatabaseManager('mangasee.db')


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
    
    
    def _create_table(self):
        '''
        Creates mangasee database.

        Args:
            None.

        Returns:
            None.
        '''
        self.database.create_table('mangasee', {
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
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
        self.database.add('mangasee', manga_data)

    
    def _search(self, title):
        '''
        Search for title in database

        Args: 
            title: Name of the series.

        Returns:
            List of matches.
        '''
        # need to implement fuzzy search
        cursor = self.database.select('mangasee', {'title': title})
        return cursor.fetchall()
  

    def print_matches(self, matches):
        '''
        Prints matches

        Args:
            matches: List of matches (list).

        Returns:
            None.
        '''
        for i, match in enumerate(matches):
            id_, title, manga_id, manga_url, cover_url = match
            print(f'{i+1}. {title}')


    def get_title(self):
        '''
        Prompts user for the title to search for.

        Args:
            None.

        Returns:
            matches: Query results (list).
        '''
        title = input('Enter title: ')
        matches = self._search(title)
        if matches:
            return self.get_match(matches)
        else:
            print('{title} has 0 matches. Try again.')
            self.get_title()
    
    
    def get_match(self, matches):
        '''
        Prompts user to choose a title from matches.

        Args:
            None.

        Returns:
            match: Manga represented as a tuple (id_, title, manga_id, manga_url, cover_url)
        '''
        self.print_matches(matches)
        choice = input('Enter the number for the manga:')
        if choice.isdigit():
            n = int(choice)
            if 0 < n <= len(matches):
                return matches[n-1]
        self.get_match(matches)


    def get_chapter(self):
        '''
        Prompts user for chapter number.

        Args:
            None.

        Returns:
            ch: Chapter number (str).
        '''
        ch = input('Enter chapter number: ')
        if ch.isdigit():
            return ch
        else:
            print('{ch} is not a valid chapter.')
            self.get_chapter()


    def create_database(self):
        '''
        Update MangaSee database.

        Args:
            None.

        Returns:
            None.
        '''
        print('This may take a while...')
        self._create_table()
        soup = self._soupify(self.directory_url)
        data = soup.find_all('a', 'ttip ng-binding')
        for series in data:
            title = series.string
            manga_id = series['href'].split('/')[-1]
            manga_url = f'''{self.base_url}{series['href']}'''
            manga_html = series['title']
            manga_soup = BeautifulSoup(manga_html, 'html.parser')
            cover_url = manga_soup.img['src']
            manga_data = {
                'title': title, 
                'manga_id': manga_id, 
                'manga_url': manga_url,
                'cover_url': cover_url}
            self._add_manga(manga_data)
    
    
    def search(self):
        '''
        Search for a series.

        Args:
            None.

        Returns:
            None.
        '''
        title = input('Enter title: ')
        matches = self._search(title)
        if matches:
            self.print_matches(matches)
        else:
            print(f'{title} has 0 matches. Try again.')


    def download(self):
        '''
        Downloads a chapter.
        
        Args:
            None.

        Returns:
            None.
        '''
        id_, title, manga_id, manga_url, cover_url = self.get_title()
        ch = self.get_chapter()
        chapter_url = f'{self.base_url}/read-online/{manga_id}-chapter-{ch}.html'
        soup = self._soupify(chapter_url)
        for page in soup.find_all('img', 'img-fluid'):
            url = page['src']
            self._save_image(url)
        utils.convert_to_pdf(ch.zfill(4))
        utils.remove_images()


    def exit(self):
        '''
        Exits program

        Args:
            None.

        Returns:
            None.
        '''
        sys.exit(0)
