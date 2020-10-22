from requests_html import HTMLSession
from bs4 import BeautifulSoup


def unescape(s):
    s = s.replace('&lt;', '<')
    s = s.replace('&gt;', '>')
    s = s.replace('&amp;', '&')
    return s


class Manga:
    def __init__(self, title=None, manga_id=None, manga_url=None,
            cover_url=None, chapters={}):
        self.title = title
        self.manga_id = manga_id
        self.manga_url = manga_url
        self.cover_url = cover_url
        self.chapters = chapters

class MangaSee:
    base_url = 'https://mangasee123.com'
    session = HTMLSession()


    def __init__(self):
        self.directory_url = f'{self.base_url}/directory/'
        self.directory = {}


    def get_directory(self):
        """
        Populates directory, dictionary of title-manga pairs.

        Args:
            None.

        Returns:
            None.
        """
        req = self.session.get(self.directory_url)
        req.html.render(sleep=5)
        html = req.html.html
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all('a', {'class':'ttip ng-binding'})
        for series in data:
            title = series.string
            manga_id = series['href'].split('/')[-1]
            manga_url = f"{self.base_url}{series['href']}"
            manga = title.lower()
            manga_html = unescape(series['title'])
            manga_soup = BeautifulSoup(manga_html, 'html.parser')
            print(manga_soup.prettify())
            cover_url = manga_soup.img['src']
            print(cover_url)
            self.directory[manga] = Manga(
                    title, 
                    manga_id, 
                    manga_url,
                    cover_url)


    def get_manga(self, manga):
        """
        Populates chapters with chapter and the chapter url pairs.

        Args:
            None.

        Returns:
            None.
        """
        req = self.session.get(manga.manga_url)
        req.html.render(sleep=5)
        html = req.html.html
        soup = BeautifulSoup(html, 'html.parser')
        # need to populate self.chapters
        # self.chapters = {}


    def get_chapter(self, manga, ch):
        """
        Populates chapters[ch]['pages'] with a list of page urls.
        
        Args:
            ch: chapter number.

        Returns:
            None.
        """
        chapter_url = f'{self.base_url}/read-online/{manga.manga_id}-chapter-{ch}.html'
        self.chapter[ch]['url'] = chapter_url
        
        req = self.session.get(chapter_url)
        req.html.render(sleep=5)
        html = req.html.html
        soup = BeautifulSoup(html, 'html.parser')
        self.chapter[ch]['pages'] = [page['src'] for page in soup.find_all('img',
            {'class':'img-fluid'})]


