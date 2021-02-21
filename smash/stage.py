class Stage:
    name = None
    removed = None

    def __init__(self, name: str, removed: bool = False):
        self.name = name
        self.removed = removed
