class Module:
    def __init__(self, name, published, contents=None):
        if contents is None:
            contents = []
        self.id = None
        self.name = name
        self.published = published
        self.contents = contents
