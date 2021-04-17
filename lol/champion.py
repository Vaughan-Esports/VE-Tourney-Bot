class Champion:
    """
    Represents a League of Legends Champion

    Just here in case I want to do more with it in the future
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other) -> bool:
        return other == self.name

    def __repr__(self):
        return self.name
