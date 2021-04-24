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

class sequence:
    def __init__(self, next):
        self._next = next
        self.mem = []
    @classmethod
    def by_function(self, func, start = 1, step = 1):
        def inner_next():
            value = func(start)
            start += step
            return value
        return sequence(inner_next)
    def ensure(self, count):
        while len(self.mem) < count:
            self.next()
    def access(self, index):
        self.ensure(index + 1)
        return self.mem[index]
    def next(self):
        val = self._next()
        self.mem.append(val)
        return val
    def __str__(self):
        self.ensure(5)
        return "[%s, ...]" % ", ".join(map(str, self.mem[:5]))
    def __repr__(self):
        return str(self)

def coerce(x):
    if isinstance(x, tuple) or isinstance(x, set):
        return list(x)
    return x

def yuno_typify(x):
    if type(x) == str:
        return list(x)
    try:
        return [yuno_typify(y) for y in x]
    except:
        return x

def try_eval(x):
    try:
        return yuno_typify(eval(x))
    except:
        return x

def compose_seq(seq, lst, func):
    index = 0
    def inner_next():
        if index < len(lst):
            val = func(lst[index], seq.next())
            index += 1
            return val
        return seq.next()
    return sequence(inner_next)

def stringQ(lst):
    return type(lst) == list and all(type(x) == str for x in lst)

def vectorize(func, left = True, right = True, chop = False):
    if type(left) == bool: left = lambda _: left
    if type(right) == bool: right = lambda _: right
    def inner(*args):
        if func.arity == 0:
            return func.call()
        elif func.arity == 1:
            argument = args[0]
            if left(argument):
                if type(argument) == list:
                    return [inner(item) for item in argument]
                elif type(argument) == sequence:
                    return sequence(lambda: inner(argument.next()))
            return func.call(argument)
        else:
            larg, rarg = args
            ltype = type(larg) if left(larg)  else None
            rtype = type(rarg) if right(rarg) else None
            if ltype == list:
                if rtype == list:
                    return [inner(L, R) for L, R in zip(larg, rarg)] + ([] if chop else larg[len(rarg):] + rarg[len(larg):])
                elif rtype == sequence:
                    return compose_seq(rarg, larg, inner)
                else:
                    return [inner(L, rarg) for L in larg]
            elif ltype == sequence:
                if rtype == list:
                    return compose_seq(larg, rarg, lambda x, y: inner(y, x))
                elif rtype == sequence:
                    return sequence(lambda: inner(larg.next(), rarg.next()))
                else:
                    return sequence(lambda: inner(larg.next(), rarg))
            else:
                if rtype == list:
                    return [inner(larg, R) for R in rarg]
                elif rtype == sequence:
                    return sequence(lambda: inner(larg, rarg.next()))
            return func.call(larg, rarg)
    return attrdict(arity = func.arity, call = inner)
