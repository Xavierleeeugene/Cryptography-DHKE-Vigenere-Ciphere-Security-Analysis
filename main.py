import vigenere
import DHKE
import brute1
import optimized


def main():
    original_message = "I love Cryptography!"
    
    #DHKE
    print("\n--DIFFIE-HELLMAN KEY EXCHANGE--\n")
    key_exchanged = DHKE.DHKE()
    print("Key Generated: ", key_exchanged)

    #VIGENERE CIPHER
    print("\n--VIGENERE CIPHER ENCRYPTION AND DECRYPTION--\n")
    vigenere_key = vigenere.vigenere_cipher(key_exchanged)
    print("Vigenere Key: " + str(vigenere_key))
    vigenere_encrypt = vigenere.convert_text(vigenere_key, original_message, 1)
    print("Vigenere Encrypted Message: " + ''.join([str(elem) for i,elem in enumerate(vigenere_encrypt)]))
    vigenere_decrypt = vigenere.convert_text(vigenere_key, vigenere_encrypt, 0)
    print("Vigenere Decrypted Message: " + ''.join([str(elem) for i,elem in enumerate(vigenere_decrypt)]))
    #due to limitation of DHKE, expected time complexity of vigenere_cipher = O(32^4) for brute force

    #BRUTE FORCE ATTACK 1
    print("\n--BRUTE FORCE ATTACK 1--\n")

    #Given plain-text, we are going to find cipher text that matches, and once that is found, we can then obtain the key
    pt = original_message
    ct = vigenere_encrypt
    get_key = brute1.brute(pt, ct)

    #OPTIMIZED ATTACK
    print("\n--OPTIMIZED ATTACK--\n")

    get_key1 = optimized.optimized_attack(pt,ct)

    #Given plain-text, we are going to find cipher text that matches, and once that is found, we can then obtain the key





if __name__ == '__main__':
    main()