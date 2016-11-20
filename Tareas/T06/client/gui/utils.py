

def similar_word(a, b):  # asumo que s1 y s2 son distintos
    distance = 0
    i = 0

    if len(a) != len(b):
        if len(a) < len(b):
            while i < len(b):
                if b[i] != a[i]:
                    distance += 1
                    if b[:i] + b[i + 1:] == a:
                        i = len(b) + 1
                    else:
                        b = b[:i] + b[i + 1:]
                else:
                    i += 1
        else:
            while i < len(a):
                if a[i] != b[i]:
                    distance += 1
                    if a[:i] + a[i + 1:] == b:
                        i = len(a) + 1
                    else:
                        a = a[:i] + a[i + 1:]
                else:
                    i += 1

    else:
        while i < len(a):
            if a[i] != b[i]:
                distance += 1
                i += 1
            else:
                i += 1

    if distance > 2:
        return False
    else:
        return True
