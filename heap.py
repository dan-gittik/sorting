def sort(a):
    build_max_heap(a)
    for n in range(len(a)-1, 0, -1):
        a[0], a[n] = a[n], a[0]
        max_heapify(a, 0, n)


def build_max_heap(a):
    for i in range(len(a) // 2, -1, -1):
        max_heapify(a, i, len(a))


def max_heapify(a, i, n):
    l = 2*i
    r = 2*i+1
    if l < n and a[i] < a[l]:
        m = l
    else:
        m = i
    if r < n and a[m] < a[r]:
        m = r
    if m != i:
        a[i], a[m] = a[m], a[i]
        max_heapify(a, m, n)
