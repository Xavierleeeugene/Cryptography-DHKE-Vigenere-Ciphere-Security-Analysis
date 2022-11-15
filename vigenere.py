#Vignere Cipher Implementation

custom_list = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !')

def vigenere_cipher(key_exchanged):
    vigenere_key = []

    for i in range(4):
        vigenere_key.append(custom_list[sum(val*(2**idx) for idx, val in enumerate(reversed(key_exchanged[i*5: i*5+5])))])

    return vigenere_key


def convert_text(key, text, encrypt):
    output = []
    counter = 0
    for i in text:
        k_value = key.pop(0)
        counter += 1
        new_char = vigenere_encrypt_decrypt(custom_list.index(i), custom_list.index(k_value), encrypt)
        output.append(custom_list[new_char])
        key.append(k_value)
    return output

def vigenere_encrypt_decrypt(i1, i2, encrypt):
    if encrypt:
        return (i1 + i2) % 64
    else:
        return (i1 - i2) % 64


