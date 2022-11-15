from math import sqrt
import numpy as np

sBox = {
    (0, 0, 0, 0): [1, 1, 1, 0], (0, 0, 0, 1): [0, 1, 0, 0], (0, 0, 1, 0): [1, 1, 0, 1], (0, 0, 1, 1): [0, 0, 0, 1],
    (0, 1, 0, 0): [0, 0, 1, 0], (0, 1, 0, 1): [1, 1, 1, 1], (0, 1, 1, 0): [1, 0, 1, 1], (0, 1, 1, 1): [1, 0, 0, 0],
    (1, 0, 0, 0): [0, 0, 1, 1], (1, 0, 0, 1): [1, 0, 1, 0], (1, 0, 1, 0): [0, 1, 1, 0], (1, 0, 1, 1): [1, 1, 0, 0],
    (1, 1, 0, 0): [0, 1, 0, 1], (1, 1, 0, 1): [1, 0, 0, 1], (1, 1, 1, 0): [0, 0, 0, 0], (1, 1, 1, 1): [0, 1, 1, 1],
    }

sInvBox = {
    (0, 0, 0, 0): [1, 1, 1, 0], (0, 0, 0, 1): [0, 0, 1, 1], (0, 0, 1, 0): [0, 1, 0, 0], (0, 0, 1, 1): [1, 0, 0, 0],
    (0, 1, 0, 0): [0, 0, 0, 1], (0, 1, 0, 1): [1, 1, 0, 0], (0, 1, 1, 0): [1, 0, 1, 0], (0, 1, 1, 1): [1, 1, 1, 1],
    (1, 0, 0, 0): [0, 1, 1, 1], (1, 0, 0, 1): [1, 1, 0, 1], (1, 0, 1, 0): [1, 0, 0, 1], (1, 0, 1, 1): [0, 1, 1, 0],
    (1, 1, 0, 0): [1, 0, 1, 1], (1, 1, 0, 1): [0, 0, 1, 0], (1, 1, 1, 0): [0, 0, 0, 0], (1, 1, 1, 1): [0, 1, 0, 1]
    }

c1 = [0, 0, 0, 1]
c2 = [0, 0, 1, 0]

constnMat = [[0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1]]

#AES Implementation
def AES_key_generator(k):
    output = []
    for i in range(4):
        temp = []
        temp.append(k[i*4 + 0])
        temp.append(k[i*4 + 1])
        temp.append(k[i*4 + 2])
        temp.append(k[i*4 + 3])
        output.append(temp)

    return output

def nibbleSub(n, subBox):
    nibbleSub = subBox.get(n)

    return nibbleSub

def getGenerateKeySchedule(key, c1, c2):

    k0, k1, k2 = (np.zeros(shape=(4, 4), dtype=int) for i in range(3))

    for round in range(3):

        if round == 0:
            try:
                k0 = np.array(key)
                #print(key)
                print("1st Round key: %s" % k0)
            except Exception as ex:
                print("Error occurred while generating the %sst round key: " % round, ex)
        elif round == 1:
            try:
                print("2nd Round key - k1")
                kSub1 = nibbleSub(tuple(k0[3]), sBox)
                for ind in range(4):
                    if ind == 0:
                        k1[ind] = k0[ind] ^ kSub1 ^ c1
                        print("k1[%s]  created: %s" % ((ind + 1), k1[ind]))
                    else:
                        k1[ind] = k0[ind] ^ k1[ind - 1]
                        print("k1[%s]  created: %s" % ((ind + 1), k1[ind]))
            except Exception as ex:
                print("Error occurred while generating the %sst round key: " % round, ex)
        elif round == 2:
            try:
                print("3rd Round key - k2")
                kSub2 = nibbleSub(tuple(k1[3]), sBox)
                for ind in range(4):
                    if ind == 0:
                        k2[ind] = k1[ind] ^ kSub2 ^ c2
                        print("k2[%s]  created: %s" % ((ind + 1), k2[ind]))

                    else:
                        k2[ind] = k1[ind] ^ k2[ind - 1]
                        print("k2[%s]  created: %s" % ((ind + 1), k2[ind]))
            except Exception as ex:
                print("Error occurred while generating the %sst round key: " % round, ex)
        else:
            print("Error: Maximum Number of rounds have configured to 3")

    return k0, k1, k2

def getKeyAddition(ptxt, rndk0):

    add = ptxt ^ rndk0
    print("Plain text before addition = %s" % ptxt)
    print("Key Addition with text = %s" % add)
    return add

def getShiftRow(etxt):

    print("Before Shit Row: %s" % etxt)
    etxt[[1, 3], :] = etxt[[3, 1], :]
    print("After Shift Row: %s" % etxt)
    return etxt

def getMixColumn(etxt):

    constMat = np.array(constnMat)
    lenetxt = int(sqrt(len(etxt)))
    lenconstmat = int(sqrt(len(constMat)))
    mixCol = np.zeros(shape=(4, 4), dtype=int)

    #total number of iterations (decides column 1 or column 2 of the input array)
    for etxtColNum in range(lenetxt):       ## when column 1 --> n index is iterating between 0 and 1
        n = etxtColNum * lenetxt            ## when column 2 --> n index is iterating between 2 and 3
        j = etxtColNum * lenetxt

        for constMatInd in range(lenconstmat):
            m = constMatInd
            waitMat = np.zeros(shape=(2, 4), dtype=int)

            for num in range(lenetxt):
                waitMat[num] = getGfMultiplication(constMat[m], etxt[n])
                n = n + 1
                m = m + 2
            k = 0
            for num2 in range(int(sqrt(len(waitMat)))):
                mixCol[j] = waitMat[k] ^ waitMat[k + 1]
            j = j + 1
            n = n - 2

    return mixCol

def convert_bits_to_index_form(bits):

    bits.reverse()
    indexes = []
    for i, bit in enumerate(bits):
        if bit != 0:
            indexes.append(i)
    indexes.sort(reverse=True)
    return indexes


def xor(input1, input2):

    output = []
    for i in input1:
        if i in input2:
            input2.remove(i)
            continue
        output.append(i)
    output.extend(input2)
    return output


def reduce(output):
    poly_of_reduction = [4, 1, 0]   # this represents x4 + x + 1
    while output[0] >= poly_of_reduction[0]:
        multiplier = output[0] - poly_of_reduction[0]                       # similar to dividing x6 by x4. ie, 6 - 4 = 2
        operand = [element + multiplier for element in poly_of_reduction]   # similar to multiplying polynomial_of_red by x2. In this case, adds 2 to each value in [4,1,0] => [6,3,2]  which represents x6+x3+x2

        output = xor(output, operand)                                       # performs XOR operation of the two values

    return output


def convert_to_bits(reduced_output, bit_length):

    output = [0 for i in range(bit_length)]
    for i in range(len(output)):
        for element in reduced_output:
            if i == element:
                output[i] = 1
    output.reverse()
    return output

def getGfMultiplication(constMat, txtBit):
    
    if np.all(constMat == [0, 0, 0, 0]) | np.all(txtBit == [0, 0, 0, 0]):

        output_1 = [0, 0, 0, 0]

    else:
        waitList = []
        for i in range(4):
            waitList.append([0, 0, 0, 0, 0, 0, 0])
            for j, bit in enumerate(constMat):
                if (bit != 0) and (txtBit[i] != 0):
                    waitList[i][j + i] = bit * txtBit[i]

        output = []
        for i in range(7):
            sum = 0
            for j in range(4):
                sum += waitList[j][i]
            output.append(sum % 2)

        # extracting Mod value
        output_index_form = convert_bits_to_index_form(output)  # converts to index form
        reduced_form = reduce(output_index_form) # performs reduction
        output_1 = convert_to_bits(reduced_form, len(constMat))  # convert back to bit form

    return output_1

def getRoundOneEncTxt(encTxtAd, rndk1, sBox):

    for num in range(len(encTxtAd)):
        encTxtSub[num] = nibbleSub(tuple(encTxtAd[num]), sBox)

    encTxtShift = getShiftRow(encTxtSub)


    encTxtMix = getMixColumn(encTxtShift)
    encTxtRndOne = getKeyAddition(encTxtMix, rndk1)


    return encTxtRndOne

def getRoundTwoEncTxt(encTxtR1, rndk2, sBox):

    for num in range(len(encTxtR1)):
        encTxtSub[num] = nibbleSub(tuple(encTxtR1[num]), sBox)

    encTxtShift = getShiftRow(encTxtSub)
    ciphrTxt = getKeyAddition(encTxtShift, rndk2)
    print("Cipher Text")
    print(ciphrTxt)

    return ciphrTxt
def getRoundOneDycTxt(dencTxtAd, rndk1, sInvBox):

    dencTxtAd = getKeyAddition(dencTxtAd, rndk1)
    print(dencTxtAd)
    dencTxtMix = getMixColumn(dencTxtAd)
    print(dencTxtMix)
    dencTxtShift = getShiftRow(dencTxtMix)


    for num in range(len(encTxtAd)):

        dencTxtRndOne[num] = nibbleSub(tuple(dencTxtShift[num]), sInvBox)


    return dencTxtRndOne