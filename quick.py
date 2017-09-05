def sort(a, start=None, end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(a)
    if end - start <= 1:
        return
    q = partition(a, start, end)
    sort(a, start, q)
    sort(a, q+1, end)


def partition(a, start, end):
    p = end-1
    q = start
    for i in range(start, end-1):
        if a[i] < a[p]:
            a[q], a[i] = a[i], a[q]
            q += 1
    a[p], a[q] = a[q], a[p]
    return q
