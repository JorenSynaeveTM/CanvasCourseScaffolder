class Page:
    def __init__(self, title, body, type, published, front_page=False):
        self.id = None
        self.title = title
        self.body = body
        self.published = published
        self.front_page = front_page
        self.type = type
