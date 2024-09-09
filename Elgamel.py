import random 
from sympy import mod_inverse
import hashlib
from Crypto.Util.number import *

a = random.randint(2, 10)
# Fonction qui verifie pgcd(a,b) = 1
def gcd(a, b):
	if a < b:
		return gcd(b, a)
	elif a % b == 0:
		return b
	else:
		return gcd(b, a % b)

#Fonction qui Génére key avec pgcd(n,key) = 1 et 1=<key<n
def gen_key(n):
	key = random.randint(pow(10, 20), n)
	while gcd(n, key) != 1:
		key = random.randint(pow(10, 20), n)

	return key

#Fonction qui effectue une Exponentiation modulaire
def modular_exponentiation(nbr, exp, mod):
    result = 1
    nbr = nbr % mod  
    while exp > 0:
        if exp % 2 == 1:
            result = (result * nbr) % mod
        nbr = (nbr * nbr) % mod
        exp = int(exp / 2)
    return result % mod

def encrypt(msg, q, h, g):
	en_msg = []
	sign = []
	#Sélectionner une entier aléatoire k, 1≤ k≤ p - 2
	k = gen_key(q)
	# B =g^k mod p
	B = modular_exponentiation(g, k, q)
    # C =h^k mod p
	C = modular_exponentiation(h, k, q)
	for i in range(0, len(msg)):
		en_msg.append(msg[i])
	for i in range(0, len(en_msg)):
		en_msg[i] = C * ord(en_msg[i])
	return en_msg, B, k

def decrypt(en_msg, B, a, p):
	dr_msg = []
	h = modular_exponentiation(B, a, p)
	for i in range(0, len(en_msg)):
		dr_msg.append(chr(int(en_msg[i]/h)))
	return dr_msg

def sign(a, B, p, k , v, g):
	text_bytes = 'Signatory'
	D =  bytes_to_long(text_bytes.encode('utf-8')) 
	k_1 = mod_inverse(k, p)
    #signature
	S_1 = B
	S_2=((D-a*S_1)*k_1) % (p-1)
	#verifie si  𝑨^𝑩 * 𝑩^𝑪 𝒎𝒐𝒅 𝒑= 𝒈𝒉 𝐦𝐨𝐝 𝐩
	v_1 = (modular_exponentiation(h,S_1,p)*modular_exponentiation(B,S_2,p))%p
	v_2 = modular_exponentiation(g,D,p)
	return v_1, v_2

def main():
	msg = 'mounia'
	print("Original Message :", msg)
    #Générer un grand nombre aléatoire p premier et un générateur g 
	p = random.randint(pow(10, 20), pow(10, 50))
	g = random.randint(2, p)
	#Sélectionner une entier aléatoire a, 1≤ a≤ p - 2
	a = gen_key(p)
	#Calculer y =g^a mod p
	h = modular_exponentiation(g, a, p)
	# La clé publique est (p;g; h)
	# La clé privée est a
	en_msg, B , k = encrypt(msg, p, h, g) 
	print("Encrypted Message :", en_msg)
	dr_msg = decrypt(en_msg, B, a, p)
	dmsg = ''.join(dr_msg)
	print("Decrypted Message :", dmsg)

if __name__ == '__main__':
	main()
