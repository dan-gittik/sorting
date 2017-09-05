def sort(a, start=None, end=None):
    if start is None:
       start = 0
    if end is None:
       end = len(a)
    if end - start <= 1:
        return
    middle = start + (end - start + 1) // 2
    sort(a, start, middle)
    sort(a, middle, end)
    merge(a, start, middle, end)


def merge(a, start, middle, end):
    l = a[start:middle]
    r = a[middle:end]
    i = j = 0
    for k in range(start, end):
        if j >= len(r) or (i < len(l) and l[i] < r[j]):
            a[k] = l[i]
            i += 1
        else:
            a[k] = r[j]
            j += 1
