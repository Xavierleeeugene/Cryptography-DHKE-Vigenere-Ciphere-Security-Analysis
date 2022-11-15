import vigenere
import sys
import time

alphabet = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !')

def optimized_attack(pt,ct):

    key_output1 = assume_unknown(pt,ct)
    key_output = assume_4_bit(pt,ct)

    partial_pt = pt[:5]

    print("\n--CONDUCTING OPTIMIZED ATTACK GIVEN PARTIAL PLAINTEXT--\n")
    key_output1 = assume_unknown(partial_pt,ct[:5])

    return key_output1


def assume_4_bit(pt, ct):
    print("\nAssuming we know it is a 4 Bit Key:")
    output = []
    counter = 0
    for i in range(4):
        key = (alphabet.index(ct[i]) - alphabet.index(pt[i])) % 64
        output += alphabet[key]
    
    counter += 1
    newCT = vigenere.convert_text(output,pt,1)
    if newCT == ct:
        print("Key Found:", ''.join(output))
        print("Total Tries: ", counter)
        print("\n")
        return output
    else:
        print("No key found")
        print("\n")
        return -1

def assume_unknown(pt, ct):
    curr_key = []
    counter = 0
    print("\nAssuming we do not know it is a 4 Bit Key: \n")
    for i in range(len(pt)):
        key = (alphabet.index(ct[i]) - alphabet.index(pt[i])) % 64
        curr_key += alphabet[key]
        counter += 1
        sys.stdout.write('\r' + "Currently Testing Key: " + ''.join(curr_key))
        newCT = optimized_convert(curr_key,pt)
        time.sleep(0.1)
        sys.stdout.flush()

        if newCT == ct:
            print("\nKey Found:", ''.join(curr_key))
            print("Total Tries: ", counter)
            return curr_key

    print("No key found")
    return -1


def optimized_convert(k, pt):
    output = []
    for i in range(len(pt)):
        k_val = i % len(k)
        output += alphabet[(alphabet.index(k[k_val]) + alphabet.index(pt[i])) % 64]
    
    return output
