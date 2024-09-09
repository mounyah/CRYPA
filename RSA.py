#Importation des bibliotheque
import random
from sympy import isprime
import math

#Generer un number premier p d'une taille=size
def generate_large_prime(size):
    #Intervalle de choix
    min_value = 2 ** (size - 1)
    max_value = 2 ** size - 1
    #Choisir un nombre et verifier si il est premier
    while True:
        candidate = random.randrange(min_value, max_value)
        if candidate % 2 == 0:
            candidate += 1  # Make it odd
        if isprime(candidate):
            return candidate

#Trouver e avec 1<e<o and gcd(o, e) = 1
def generate_random_coprime(o):
    while True:
        e = random.randint(2, o - 1) 
        if math.gcd(e, o) == 1: 
            return e

#Implementation de theorem de Bezout pour trouver x avec:
#  ax + by = gcd(a, b)
def extended_gcd_iterative(a, b):
    x_prev, x = 1, 0
    y_prev, y = 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x_prev, x = x, x_prev - q * x
        y_prev, y = y, y_prev - q * y

    return a, x_prev, y_prev

#Trouver d avec d * e ≡ 1 (mod o)
def find_unique_d(e, o):
    #trouver coefficient x
    gcd, x, _ = extended_gcd_iterative(e, o)
    d = x % o
    if d <= 0:
        d += o
    return d


def generate_keypair():
    #taille de la cle
    prime_size = 128 
    #generer deux entier premier p et q
    p = generate_large_prime(prime_size)
    q = generate_large_prime(prime_size)
    n = p * q 
    #function  Euler Totient 
    o = (p-1) * (q-1)
    #cle publique
    e = generate_random_coprime(o)
    #cle prive
    d = find_unique_d(e, o)
    return ((n, e), (n, d))


def encrypt(message, public_key):
    n, e = public_key
    #encrypter : C = (M^e)
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def decrypt(encrypted_message, private_key):
    n, d = private_key
    #decrypter : M = (C^d)
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted_message


public_key, private_key = generate_keypair()
n, e = public_key
n, d = private_key
message = 'mounia'

print('message:',message)
print('public_key:', e)
print('private_key:', d)


encrypted_message = encrypt(message, public_key)
print('encrypted_message:',encrypted_message)
print('decrypted_message:',decrypt(encrypted_message, private_key))