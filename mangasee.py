from requests_html import HTMLSession
from bs4 import BeautifulSoup


class MangaSee:
    base_url = 'https://mangasee123.com/'
    session = HTMLSession()

    def __init__(self, manga_url):
        self.manga_url = manga_url
        self.cover_url = None
        self.chapters = {}
        

    def get_info(self):
        """
        Args:
            None.

        Returns:
            None.
        """
        req = self.session.get(self.manga_url)
        req.html.render(sleep=5)
        html = req.html.html
        soup = BeautifulSoup(html, 'html.parser')
        self.cover_url = soup.find('img', {'class':'img-fluid bottom-5'})['src']
        self.manga_id = self.manga_url.split('/')[-1]
        

    def get_chapter(self, ch, debug=False):
        """
        Args:
            ch: chapter number.
            debug: True prints debug messages.

        Returns:
            None.
        """
        chapter_url = f'{self.base_url}/read-online/{self.manga_id}-chapter-{ch}.html'
        req = self.session.get(chapter_url)
        req.html.render(sleep=5)
        html = req.html.html
        soup = BeautifulSoup(html, 'html.parser')
        images = [page['src'] for page in soup.find_all('img',
            {'class':'img-fluid'})]
        for i, image in enumerate(images):
            pg = str(i+1)
            filename = f'{ch.zfill(4)}-{pg.zfill(3)}.png'
            image_req = session.get(image)
            content = image_req.content
            save(filename, content)
            if debug:
                print(f'ch.{ch} pg.{pg}')
        if debug:
            print('done')


def save(self, filename, content):
    """
    Args:
        filename: name of the file you want to write to.
        content: content you want to write to the file.

    Returns:
        None.
    """
    with open(filename, 'wb') as f:
        f.write(content)
        f.close()
            
