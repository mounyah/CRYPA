from collections import deque


p10 = [3,5,2,7,4,10,1,9,8,6]
p8 = [6 ,3 ,7 ,4 ,8 ,5 ,10 , 9]
pi = [2, 6, 3, 1, 4, 8, 5, 7]
ep = [4, 1, 2, 3, 2, 3, 4, 1]
pi_1 = [4, 1, 3, 5, 7, 2, 8, 6]
p4 = [2, 4, 3, 1]

S_0 = [
    [['0', '1'], ['0', '0'], ['1', '1'], ['1', '0']],
    [['1', '1'], ['1', '0'], ['0', '1'], ['0', '0']],
    [['0', '0'], ['1', '0'], ['0', '1'], ['1', '1']],
    [['1', '1'], ['0', '1'], ['1', '1'], ['1', '0']]
]
S_1 = [
    [['0', '0'], ['1', '0'], ['1', '0'], ['1', '1']],
    [['1', '0'], ['0', '0'], ['0', '1'], ['1', '1']],
    [['1', '1'], ['0', '0'], ['0', '1'], ['0', '0']],
    [['1', '0'], ['0', '1'], ['0', '0'], ['1', '1']]
]

#Effectue une rotation sur une suite de bits vers la gauche par 'c' positions.
def rotate_left(liste,c):
    return liste[c:] +  liste[:c]

#Effectue une permutation sur une suite de bits en fonction de la table de permutation fournie'
def permutation(string, p_table):
    k=[]
    for i in range(len(p_table)):
        k.append(string[p_table[i]-1])
    return k

#Effectue un Xor sur 2 suite de bits
def xor(list1, list2):
    list1_int = [int(bit) for bit in list1]
    list2_int = [int(bit) for bit in list2]
    return [a ^ b for a, b in zip(list1_int, list2_int)]  

def generate_key(key):
    #Initialisation des variables
    k=[]
    key1=[]
    key2=[]
    #Permutation avec p10
    pk_10 = permutation(key, p10)
    #Decoupage de la cles en deux
    l0 = pk_10[:5]
    r0 = pk_10[5:]
    #Effectuer Decalages des bits a gouche, ensuite Xor pour avoir les cles
    key1 = permutation(rotate_left(l0,1) + rotate_left(r0,1), p8)
    key2 = permutation(rotate_left(l0,3) + rotate_left(r0,3), p8)
    return key1, key2

def chiffrement_function(message, key):
    l = message[:4]
    r = message[4:]
    r_ep = permutation(r, ep)
  
    xor_result = xor(r_ep, key)
    s_0 = xor_result[:4]
    s_1 = xor_result[4:]

    s_boxes = S_0[int(str(s_0[0])+str(s_0[-1]),2)][int(str(s_0[1])+str(s_0[2]),2)] + S_1[int(str(s_1[0])+str(s_1[-1]),2)][int(str(s_1[1])+str(s_1[2]),2)]
    result_pk4 =permutation(s_boxes, p4)

    r1 = xor (result_pk4, l)

    return r, r1

def chiffrer(message, key1, key2):
    #Faire la permutation intial pour message a chiffrer
    message = permutation(message, pi)
    #Faire le premier Round avec la fonction de chiffrement 
    r0, r1 = chiffrement_function(message, key1)
    #Faire le premier Round avec la fonction de chiffrement 
    r11, r2 = chiffrement_function(r0 + r1, key2)

    return permutation(r2 + r11, pi_1)

def main():
    #key= list(input("Enter the key : "))
    #message= list(input("Enter the message : "))

    key = '1010000010'
    message = '01110010'

    key1 ,key2 = generate_key(key)
    print('The keys:', key1, key2)
    
    chiffrement = chiffrer(message, key1, key2)
    print('resultat:', chiffrement)

if __name__ == "__main__":
    main()