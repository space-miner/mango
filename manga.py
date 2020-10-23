class Manga:

    def __init__(self, title=None, manga_id=None, manga_url=None,
            cover_url=None, chapters={}):
        self.title = title
        self.manga_id = manga_id
        self.manga_url = manga_url
        self.cover_url = cover_url
        self.chapters = chapters
