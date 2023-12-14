class NewsModel:

    def __init__(self, id:int = None, title:str = None, url:str = None, body:str = None, date:str = None, source:str = None) -> None:
        self.id = id
        self.title = title
        self.url = url
        self.body = body
        self.date = date
        self.source = source

    def body_message(self)-> str:
        return f"\n```------- BERITA {self.source} ------\nJudul: {self.title.strip()}\nTanggal: {self.date}``````{self.body.strip()}```\nLihat selengkapnya: {self.url}"