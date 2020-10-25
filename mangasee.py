import html
from requests_html import HTMLSession
from bs4 import BeautifulSoup


class MangaSee:
    base_url = 'https://mangasee123.com'
    session = HTMLSession()


    def __init__(self):
        self.directory_url = f'{self.base_url}/directory/'
        self.directory = {}


    def update_directory(self):
        """
        Populates directory, dictionary of title-manga pairs.

        Args:
            None.

        Returns:
            None.
        """
        soup = self.soupify(self.directory_url)
        data = soup.find_all('a', {'class':'ttip ng-binding'})
        for series in data:
            title = series.string.lower()
            title_id = series.string
            manga_id = series['href'].split('/')[-1]
            manga_url = f"{self.base_url}{series['href']}"
            manga_html = series['title']
            manga_soup = BeautifulSoup(manga_html, 'html.parser')
            cover_url = manga_soup.img['src']
            self.directory[title] = {
                    'title id': title_id, 
                    'manga id': manga_id, 
                    'manga url': manga_url,
                    'cover url': cover_url,
                    'chapters': {}}


    def get_chapter(self, title, ch):
        """
        Populates chapter pages with direct link to page image.
        
        Args:
            ch: chapter number.

        Returns:
            None.
        """
        manga = self.directory[title]
        manga_id = manga['manga id']
        chapter_url = f'{self.base_url}/read-online/{manga_id}-chapter-{ch}.html'
        soup = self.soupify(chapter_url)
        manga['chapters'][ch] = [page['src'] for page in soup.find_all('img',
            {'class':'img-fluid'})]
        for url in manga['chapters'][ch]:
            self.save_image(url)


    def soupify(self, url):
        for i in range(3):
            try:
                print(f"Pulling: {url}")
                req = self.session.get(url)
                req.html.render(sleep=5)
                html = req.html.html
                return BeautifulSoup(html, 'html.parser')
            except:
                print('Failed network request | Retrying')


    def save_image(self, url):
        print(f"Pulling: {url}")
        req = self.session.get(url)
        filename = url.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(req.content)
            f.close()


if __name__ == '__main__':
    ms = MangaSee()
    ms.update_directory()
    ms.get_chapter('one piece', 322)
