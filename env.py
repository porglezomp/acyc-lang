class Env:
    def __init__(self, parent=None):
        self.parent = parent
        self.items = {}

    def __getitem__(self, index):
        if index in self.items:
            return self.items[index]
        elif self.parent is not None:
            return self.parent[index]

    def __setitem__(self, index, item):
        self.items[index] = item

    def __contains__(self, item):
        if item in self.items:
            return True
        elif self.parent is not None:
            return (item in self.parent)
        return False

    def strictly_contains(self, item):
        return (item in self.items)
