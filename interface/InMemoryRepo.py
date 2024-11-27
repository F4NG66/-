class InMemoryRepo:
    def __init__(self):
        self.data = {}

    def add(self, item):
        self.data[item.title] = item

    def get(self, title):
        return self.data.get(title)

    def get_all(self):
        return list(self.data.values())
