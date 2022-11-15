import secrets

custom_list = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !')

#MY IMPLEMENTATION of DHKE

def DHKE():
    A = secrets.randbelow(1048576)
    B = secrets.randbelow(1048576)

    g = 2
    n = 999983

    kA = (g**A) % n
    kB = (g**B) % n

    kAB = (kA**B) % n
    kBA = (kB**A) % n

    kAB = list(bin(kAB).replace('b', '0'))
    kAB = [int(i) for i in kAB]
    if len(kAB) > 20:
        kAB.pop(0)
    while len(kAB) < 20:
        kAB.insert(0, 0)

    return kAB
