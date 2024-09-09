import random
from math import ceil
from decimal import Decimal

FIELD_SIZE = 10**5

#Fonction pour Reconstitution du secret 
#En utilisant le polynôme de Lagrange
def reconstruct_secret(shares):
	sums = 0
	prod_arr = []
	#Calcule de L(X)
	for j, share_j in enumerate(shares):
		xj, yj = share_j
		prod = Decimal(1)
		# Calaculer les li
		for i, share_i in enumerate(shares):
			xi, _ = share_i
			if i != j:
				prod *= Decimal(Decimal(xi)/(xi-xj))
		#Calculer li*yi
		prod *= yj
		sums += Decimal(prod)

	return int(round(Decimal(sums), 0))
#Fonction pour calculer y = f(x) = a0 +a1 *x ...
def polynom(x, coefficients):
	point = 0
	for coefficient_index, coefficient_value in enumerate(coefficients):
		point += x ** coefficient_index * coefficient_value
	return point

#Fonction pour calculer des partages
def generate_shares(n, m, secret):
	#Choisir au hasardk- 1 entiers positifs (coefficients ) dans un corps fini p
	p = 31
	#Poser a0= S
	coefficients = [15, 2, 23]
	shares = []
    #Calculer les points (les actions) a l'aide de polynome
	for i in range(1, n+1):
		x = i 
		shares.append((x, polynom(x, coefficients) % p ))
	return shares

if __name__ == '__main__':

	# n est le nombre total d'actions et t est le seuil.
	t, n = 3, 5
	#le secret
	secret = 15
	print(f'Original Secret: {secret}')

	#Generation des partages
	shares = generate_shares(n, t, secret)
	print(f'Shares: {", ".join(str(share) for share in shares)}')

	#Reconstitution du secret avec le polynomes de lagrange 
	pool = random.sample(shares, t)
	print(f'Combining shares: {", ".join(str(share) for share in pool)}')
	print(f'Reconstructed secret: {reconstruct_secret(pool) % 31 }')
