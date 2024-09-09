from random import randrange
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Fonction pour vérifier si la courbe est non singulière
def is_nonsingular(a, b, p):
    delta = (-16 * (4 * (a**3) + 27 * (b**2))) % p
    return delta != 0

# Fonction pour calculer le symbole de Legendre
def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if (ls == (p - 1)) else ls

# Fonction pour tracer les points de la courbe elliptique
def plot_elliptic_curve(a, b, p):
    x_vals = []
    y_vals_pos = []
    val =[]
    for x in range(p):
        y_square = (x**3 + a*x + b) % p
        if legendre_symbol(y_square, p) == 1:  # Vérifier si y_square est un résidu quadratique modulo p
            y_vals = [y for y in range(int(np.sqrt(p))) if (y**2) % p == y_square]
            print(y_vals)
            if y_vals:
                x_vals.extend([x] * len(y_vals))
                y_vals_pos.extend(y_vals)
                val.extend([[x] * len(y_vals), y_vals])

    plt.scatter(x_vals, y_vals_pos, color='b', label='y')
    plt.title(f'Partie positive de la courbe elliptique sur Z_{p}: $y^2 = x^3 + {a}x + {b}$')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()
    print(val)

# Fonction pour vérifier si un nombre est premier
def prime_number(p):
    if p <= 1 :
        return False
    else:
        for i in range(2,p):
            if p % i == 0 :
                return False
        return True

# Fonction pour l'exponentiation modulaire
def modular_exponentiation(nbr, exp, mod):
    result = 1
    nbr = nbr % mod  
    while exp > 0:
        if exp % 2 == 1:
            result = (result * nbr) % mod
        nbr = (nbr * nbr) % mod
        exp = int(exp / 2)
    return result % mod

# Fonction pour trouver la racine primitive
def primitive_root(g,p):
    for i in range(1,p-1):
        if modular_exponentiation(g,i,p) == i:
            return False
    return True

# Fonction pour générer les clés
def generate_keys(g,p):
    private_key = randrange(1,p)
    public_key = modular_exponentiation(g,p_key,p)
    return private_key, public_key

# Fonction pour calculer la clé secrète
def secret_key(p, p_key, s):
    return modular_exponentiation(s,p_key,p)

# Fonction pour calculer la courbe elliptique
def elliptic_curve(x, a, b):
    return np.sqrt(x**3 + a*x + b), -np.sqrt(x**3 + a*x + b)

def main():
    p = 7  # Nombre premier
    g = 2  # Racine primitive
    # Exemple de nombre premier
    p = 17  
    # Définir les paramètres de la courbe a et b
    a = 1
    b = 1
    # Vérifier si la courbe est non singulière
    if is_nonsingular(a, b, p):
        # Tracer la courbe
        plot_elliptic_curve(a, b, p)
    else:
        print("La courbe est singulière sur Zp.")

    alice = generate_keys(g,p)
    bob = generate_keys(g,p)

if __name__ == '__main__':
    main()
