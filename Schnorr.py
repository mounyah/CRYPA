import random 
import sys 

#données initiales
p = 88667
generator = 70322
secretVal = 755
alpha = pow(generator, secretVal) % p


#Le prouveur envoie les données initiales au vérifieur
print("ALICE (the Prover) generates these values:") 
print("secretVal = ", secretVal) 
print("P= ", p) 
print("alpha= ", alpha) 


#Le prouveur choisit un entier K < q et calculer b=g^k mod p
k = 543
b = pow(generator, k) % p
print("ALICE generates a random value (k):") 
print("k=", k) 
print("ALICE computes b") 
print("b=", b) 

#Le prouveur envoie b au vérifieur
print("BOB generates a random value (c) and passes to Alice:") 

#Le vérifieur choisit un alea r et l'envoie au prouveur
r = 1000 
print("r=", r) 

#Le prouveur calcule c et envoie le resultat au vérifieur
print("ALICE calculates z = y.secretVal^r \ (mod p) and send to the Verifier):") 
c = (k + r * secretVal) 
print("c=", c) 

# Le vérifieur vérifie l'égalité b * alpha^r mod p = g^c mod p 
print("BOB now computes ") 
val1 = pow(generator, c) % p
val2 = (b * (alpha**r)) % p

print("val1= ", val1, end=' ') 
print(" val2= ", val2) 

if (val1 == val2): 
	print("ALICE has proven that she knows x") 
else: 
	print("Failure to prove") 
