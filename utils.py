class attrdict(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)
        self.__dict__ = self

class Constant:
    def __init__(self, value):
        self.arity = 0
        self.value = value
    def call(self, *args, **kwargs):
        return self.value
    def __str__(self):
        return f"<Constant Function: {self.value}>"
    def __repr__(self):
        return str(self)

def coerce(x):
    if isinstance(x, tuple) or isinstance(x, set):
        return list(x)
    return x

def try_eval(x):
    try:
        return eval(x)
    except:
        return x
