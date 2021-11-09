class TafsirMimpi:
    def __init__(self, js) -> None:
        self.result = js['hasil']
        self.count = js['total']
    def __getitem__(self, x):
        return self.result[1]
    def __iter__(self):
        return self.result
    def __repr__(self):
        return self.result.__str__()