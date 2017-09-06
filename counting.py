MIN = 0
MAX = 100


def sort(a):
    c = [0]*(MAX+1)
    for i in range(len(a)):
        c[a[i]] += 1
    k = 0
    for i in range(len(c)):
        for j in range(c[i]):
            a[k] = i
            k += 1
