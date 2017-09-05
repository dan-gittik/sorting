def sort(a):
    for i in range(len(a)):
        for j in range(0, i):
            if a[i] < a[j]:
                break
        else:
            continue
        e = a[i]
        for k in range(i, j, -1):
            a[k] = a[k-1]
        a[j] = e


def sort(a):
    for i in range(len(a)):
        for j in range(i, 0, -1):
            if a[j] < a[j-1]:
                a[j], a[j-1] = a[j-1], a[j]
            else:
                break
