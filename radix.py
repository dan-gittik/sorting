MIN = 0
MAX = 1000


def sort(a):
    for n in range(len(str(MAX))):
        digit_sort(a, n)


def digit_sort(a, n):
    c = [0]*10
    for i in range(len(a)):
        c[a[i] // 10**n % 10] += 1
    for i in range(1, len(c)):
        c[i] += c[i-1]
    b = a[:]
    for i in range(len(b)-1, -1, -1):
        d = b[i] // 10**n % 10
        c[d] -= 1
        a[c[d]] = b[i]
