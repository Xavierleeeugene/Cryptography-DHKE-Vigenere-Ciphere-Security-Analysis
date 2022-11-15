import time
import vigenere
import sys

key_gen = []
alphabet = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !')

c1 = 0
c2 = 0
c3 = 0
c4 = 0

for i in range(32**4):
    output = ""
    output += alphabet[c1]
    output += alphabet[c2]
    output += alphabet[c3]
    output += alphabet[c4]

    if c4 < 31:
        c4 += 1
    elif c3 < 31:
        c4 = 0
        c3 += 1

    elif c2 < 31:
        c3 = 0
        c4 = 0
        c2 += 1

    else:
        c2 = 0
        c3 = 0
        c4 = 0
        c1 += 1
    
    key_gen.append(output)

def brute(pt, ct):
    counter = 0
    for i in key_gen:
        counter += 1
        key_test = [j for j in i]
        sys.stdout.write('\r' + "Currently Testing Key: " + i)
        time.sleep(0.000001)
        newCT = vigenere.convert_text(key_test,pt,1)
        sys.stdout.flush()

        if newCT == ct:
            print("Key Found: " + i)
            print("Total Tries:", counter)
            return i

    return -1

