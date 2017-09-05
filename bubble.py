def sort(a):
    swap = True
    while swap:
        swap = False
        for i in range(len(a)-1):
            if a[i] > a[i+1]:
                a[i], a[i+1] = a[i+1], a[i]
                swap = True
