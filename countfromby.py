class CountFromBy:

    def __init__(self, v=0, i=1):
        self.val = v
        self.incr = i

    def increase(self):
        self.val += self.incr

    def __repr__(self) -> str:
        return str(self.val)
