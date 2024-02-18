class NewsModel:

    def __init__(self, news:dict = {}) -> None:
        self.id = news.get("id")
        self.title = news.get("title")
        self.url = news.get("url")
        self.body = news.get("body")
        self.date = news.get("date")
        self.source = news.get("source")
        
    def body_message(self)-> str:
        return f"\n```------- BERITA {self.source} ------\nJudul: {self.title}\nTanggal: {self.date}``````{self.body}```\nLihat selengkapnya: {self.url}"
    