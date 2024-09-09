import numpy as np

NibblSub=['1110', '0100', '1101', '0001', '0010', '1111', '1011', '1000', '0011', '1010', '0110', '1100', '0101', '1001', '0000', '0111']

matrix = [['0011', '0010'],
          ['0010', '0011']]

multiplication_table = [
        ["0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000", "0000"],
        ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"],
        ["0000", "0010", "0100", "0110", "1000", "1010", "1100", "1110", "0011", "0001", "0111", "0101", "1011", "1001", "1111", "1101"],
        ["0000", "0011", "0110", "0101", "1100", "1111", "1010", "1001", "1011", "1000", "1101", "1110", "0111", "0010", "0001", "0010"],
        ["0000", "0100", "1000", "1100", "0011", "0111", "1011", "1111", "0110", "0010", "1110", "1010", "0101", "0001", "1101", "1001"],
        ["0000", "0101", "1010", "1111", "0111", "0010", "1101", "1000", "1110", "1011", "0100", "0001", "1001", "1100", "0011", "0110"],
        ["0000", "0110", "1100", "1010", "1011", "1101", "0111", "0001", "0101", "0011", "1001", "1111", "1110", "1000", "0010", "0100"],
        ["0000", "0111", "1110", "1001", "1111", "1000", "0001", "0110", "1101", "1010", "0011", "0100", "0010", "0101", "1100", "1011"],
        ["0000", "1000", "0011", "1011", "0110", "1110", "0101", "1101", "1100", "0100", "1111", "0111", "1010", "0010", "1001", "0001"],
        ["0000", "1001", "0001", "1000", "0010", "1011", "0011", "1010", "0010", "1101", "0101", "1100", "0110", "1111", "0111", "1110"],
        ["0000", "1010", "0111", "1101", "1110", "0011", "1001", "0011", "1111", "0101", "1000", "0010", "0001", "1011", "0110", "1100"],
        ["0000", "1011", "0101", "1110", "1010", "0001", "1111", "0100", "0111", "1100", "0010", "1001", "1101", "0110", "1000", "0011"],
        ["0000", "1100", "1011", "0111", "0101", "1001", "1110", "0010", "1010", "0110", "0001", "1101", "1111", "0011", "0100", "1000"],
        ["0000", "1101", "1001", "0100", "0001", "1100", "1000", "0101", "0010", "1111", "1011", "0110", "0011", "1110", "1010", "0111"],
        ["0000", "1110", "1111", "0001", "1101", "0011", "0010", "1100", "1001", "0111", "0110", "1000", "0100", "1010", "1011", "0101"],
        ["0000", "1111", "1101", "0010", "1001", "0110", "0100", "1000", "0001", "1110", "1100", "0011", "1000", "0111", "0101", "1010"]
    ]

#Decopage 16 bits en 4 bloc
def split_into_4(s):
    return s[:4], s[4:8], s[8:12], s[12:]

#Xor entre deux suites de bits
def xor(list1, list2):
    list1_int = [int(bit) for bit in list1]
    list2_int = [int(bit) for bit in list2]
    return list_to_str([a ^ b for a, b in zip(list1_int, list2_int)])

def recon(i):
    if i < 8 : 
        return '0001'
    else:
        return '0010'

#Transformation une suite de bits en chaine de caracteres
def list_to_str(l):
    s = ''
    for i in range(len(l)):
        s = s + str(l[i])
    return s

#Retourner le nibble_sub
def nibbl_sub(s):
    return NibblSub[int(s,2)]

def empty_list(len):
    w = []
    for i in range(len):
        w.append(0)
    return w

def generate_keys(key):
    #Initialisation 
    w = empty_list(12)
    #Decopage de K0
    w[0], w[1], w[2], w[3] = split_into_4(key)
    #generation des cles k1 et k2 
    for i in range(4,12):
        if i==4 or i==8 :
            w[i] = xor(xor(w[i-4], nibbl_sub(w[i-1])), recon(i))
        else :
            w[i] = xor(w[i-4], w[i-1])
    return list_to_str(w[4:8]),list_to_str(w[8:])

def shift_rows(b):
    c = [[b[0], b[2]],
         [b[3], b[1]]]
    return c

#retourne le resultat de la multiplication en utilsant tableau GF(24) modulo x4+ x + 1. 
def multiply_GF16(a, b):
    return str(multiplication_table[int(a, 2)][int(b, 2)])

def mix_column( c):
    matrix = [['0011', '0010'],
          ['0010', '0011']]
    e = [[0, 0],
          [0, 0]]
    #le resultat de la multiplication
    e[0][0] = xor(multiply_GF16(matrix[0][0], c[0][0]), multiply_GF16(matrix[0][1], c[1][0]))
    e[0][1] = xor(multiply_GF16(matrix[0][0], c[0][1]), multiply_GF16(matrix[0][1], c[1][1]))
    e[1][0] = xor(multiply_GF16(matrix[1][0], c[0][0]), multiply_GF16(matrix[1][1], c[1][0]))
    e[1][1] = xor(multiply_GF16(matrix[1][0], c[0][1]), multiply_GF16(matrix[1][1], c[1][1]))
    return e

def add_round_key(key, d ):
    e=[]
    e.append(xor(key[0], d[0][0]))
    e.append(xor(key[1], d[1][0]))
    e.append(xor(key[2], d[0][1]))
    e.append(xor(key[3], d[1][1]))
    return e

def chiffrement(message,key0, key1, key2 ):
    #Xor initial 
    m = xor(message, key0 )
    #Rounds
    for i in range(2):
        #Initialisation
        p = empty_list(4)
        b = empty_list(4)
        #Decopage en bloc de 4 bits
        p[0], p[1], p[2], p[3] = split_into_4(m)
        #NIbble sub
        for j in range(4):
            b[j] = nibbl_sub(p[j])
        #Shift rows
        c = shift_rows(b)
        #Mix rows
        d = mix_column( c)
        if i == 0:
            k = split_into_4(key1)
        else:
            k = split_into_4(key2)
        #add_round_key
        e = add_round_key(k , d)
        m = ''.join(e)
    return m

def main():
    key0 = '1100001111110000'
    key1, key2 = generate_keys(key0)
    print("The keys are :",generate_keys(key0))
    message = '1001110001100011'
    
    print(chiffrement(message,key0, key1, key2))

if __name__ == "__main__":
    main()