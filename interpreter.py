def yuno_print(x):
    print(x, end = "") # TODO

def arities(links):
    return [link.arity for link in links]

def LCC(links):
    copy = links[:]
    if copy == []:
        return False
    if copy.pop(0).arity != 0:
        return False
    while copy:
        if copy[0].arity == 1:
            copy.pop(0)
            continue
        else:
            if len(copy) == 1:
                return False
            if copy.pop(0).arity + copy.pop(0).arity != 2:
                return False
    return True

links = None
ilist = []

def quick_invoke(index, *arguments):
    ilist.append(index)
    val = invoke(links[index % len(links)], *arguments)
    ilist.pop()
    return val

def invoke(link, *arguments):
    if link == []:
        return [arguments[:1] or [0]][0]
    arity = len(arguments)
    if arity == 0:
        if link[0] == []:
            value = 0
            link = link[1:]
        elif link[0][0].arity == 0:
            return invoke([link[0][1:], *link[1:]], link[0][0].call())
        else:
            return invoke(link, 0)
    elif arity == 1:
        copy = link[0][:]
        if copy == []:
            value = arguments[0]
        elif copy[0].arity == 0:
            value = copy[0].call()
            copy.pop(0)
        else:
            value = arguments[0]
        while copy:
            a = arities(copy[:2])
            if a == [2, 1]:
                value = copy.pop(0).call(value, copy.pop(0).call(arguments[0]))
            elif a == [2, 0]:
                value = copy.pop(0).call(value, copy.pop(0).call())
            elif a == [0, 2]:
                value = copy.pop(1).call(copy.pop(0).call(), value)
            elif a[0] == 2:
                value = copy.pop(0).call(value, arguments[0])
            elif a[0] == 1:
                value = copy.pop(0).call(value)
            else:
                yuno_print(value)
                value = copy.pop(0).call()
    elif arity == 2:
        copy = link[0][:]
        if copy == []:
            value = arguments[0]
        if arities(copy[:3]) == [2, 2, 2]:
            value = copy.pop(0).call(arguments[0], arguments[1])
        elif LCC(copy):
            value = copy.pop(0).call()
        else:
            value = arguments[0]
        while copy:
            a = arities(copy[:2])
            if a == [2, 2]:
                if len(copy) >= 3 and LCC(copy[2:]):
                    value = copy.pop(0).call(value, arguments[1])
                    value = copy.pop(0).call(value, copy.pop(0).call())
                else:
                    value = copy.pop(0).call(value, copy.pop(0).call(arguments[0], arguments[1]))
            elif a == [2, 0]:
                value = copy.pop(0).call(value, copy.pop(0).call())
            elif a == [0, 2]:
                value = copy.pop(1).call(copy.pop(0).call(), value)
            elif a[0] == 2:
                value = copy.pop(0).call(value, arguments[1])
            elif a[0] == 1:
                value = copy.pop(0).call(value)
            else:
                yuno_print(value)
                value = copy.pop(0).call()
    if len(link) > 1:
        return invoke([link[1][1:], *link[2:]], *link[1][0](value, *arguments))
    return value
