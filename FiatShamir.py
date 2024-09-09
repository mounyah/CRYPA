import random
def fiat_shamir_protocol(n, S):
    #donnée initiale
    I = (S ** 2) % n
    #choisit un entier naturel inversible de manière aléatoire  
    R = random.randint(1, n-1)
    #calcule son carré x modulo n.
    X = (R ** 2) % n
    #Le prouveur envoie x au vérifieur
    #Le vérifieur choisit un bit e de manière aléatoire
    e = random.randint(0, 1)
    #Le prouveur calcule 𝒀 = 𝒓 𝑺𝒆 𝒎𝒐𝒅 𝒏 et l'envoie au vérifieur.
    Y = (R * (S ** e)) % n
    # Le vérifieur vérifie l'égalité 𝑌2 = 𝑥 𝐼𝑒 𝑚𝑜𝑑 𝑛
    if (Y ** 2) % n == (X * (I ** e)) % n:
        print("Proven")
    else:
        print("Failure to prove")
fiat_shamir_protocol(11, 30)