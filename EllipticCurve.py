import numpy as np
import matplotlib.pyplot as plt

#Verifier si le point appartient a la courbe
def belong(point, a, b, p):
    x, y = point
    y_2 = (y**2)  % p
    y_x = ((x**3) + (a*x) + b ) % p
    if y_2 == y_x :
        return True
    else:
        return False

#Arithmétique sur les courbes elliptiques
#Addition des points
def plus(point1, point2, p):
    x1, y1 = point1
    x2, y2 = point2
    gamma = ((y2 - y1) * (mod_inverse_fermat(x2 - x1, p))) % p
    x_3 = ((gamma**2 ) - x1 - x2) % p
    y_3 = ((gamma * (x1 - x_3)) - y1) % p
    result = (x_3, y_3)
    return result

#Doublement de points
def mul(point,a,  p):
    x, y = point
    gamma = (((3 * (x**2)) + a) * (mod_inverse_fermat(2 * y , p))) % p
    x_ = ((gamma**2 ) - (2 * x)) % p
    y_ = ((gamma * (x - x_)) - y ) % p
    result = (x_, y_)
    return result

#Faire 7.p dans Zp
def k_p(point,a,  p, k):
    p_2 = mul(point,a,  p)
    p_3 = plus(p_2, point, p)
    p_4 = plus(p_3, point, p)
    p_5 = plus(p_4, point, p)
    p_6 = plus(p_5, point, p)
    p_7 = plus(p_6, point, p)
    return(p_7)

#Fonction de cryptage 
def crypt(Qb, M,a, p):
    result = mul(Qb, a,  p)
    result = plus(M, result, p)
    return result

#Fonction de decryptage:
def dycrypt(point, Lc, Qb, a, b, p ):
    k = 2
    s = mul(point,a,  p)
    s = mul(point,a,  p)
    s = plus(s , point, p)
    x, y = s 
    s = -x % p, -y % p
    result = plus(Lc, s, p)#
    
    x, y = result
    result = int(x / 2), y 
    return result

def is_nonsingular(a, b, p):
    delta = (-16 * (4 * (a**3) + 27 * (b**2))) % p
    return delta != 0

def mod_inverse_fermat(a, p):
    return pow(a, p - 2, p)

def plot_elliptic_curve(a, b):
    x_values = np.linspace(-7, 7, 400)
    # Calculate corresponding y values
    y_values_positive = np.sqrt(x_values**3 + a*x_values + b)
    y_values_negative = -np.sqrt(x_values**3 + a*x_values + b)

    # Plot the positive branch of the curve
    plt.plot(x_values, y_values_positive, label='Positive Branch')

    # Plot the negative branch of the curve
    plt.plot(x_values, y_values_negative, label='Negative Branch')

    # Add labels and title
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Elliptic Curve: y^2 = x^3 + {}x + {}'.format(a, b))

    # Add legend
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.show()

def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if (ls == (p - 1)) else ls

def mod_sqrt(a, p):
    if legendre_symbol(a, p) != 1:
        return None  # No square root exists
    x = pow(a, (p + 1) // 4, p)
    return x, p - x

def plot_elliptic_curve_mod(a, b, p):
    x_vals = []
    y_vals_pos = []
    val =[]

    for x in range(p):
        y_square = (x**3 + a*x + b) % p
        if legendre_symbol(y_square, p) == 1:  # Check if y_square is a quadratic residue modulo p
            y_vals = [y for y in range(int(np.sqrt(p))) if (y**2) % p == y_square]
            print(y_vals)
            if y_vals:
                x_vals.extend([x] * len(y_vals))
                y_vals_pos.extend(y_vals)
                val.extend([[x] * len(y_vals), y_vals])

    plt.scatter(x_vals, y_vals_pos, color='b', label='y')
    plt.title(f'Positive Part of the Elliptic Curve over Z_{p}: $y^2 = x^3 + {a}x + {b}$')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()
    print(val)

def main():
    a = -5
    b = 3
    p = 31
    k = 7
    plot_elliptic_curve(a, b)
    plot_elliptic_curve_mod(a, b, p)
    print('The curve is non singular :',is_nonsingular(a, b, p))
    M = (12,11)
    B = (9,6)
    point =(5, 14)
    print('B belongs to the curve :',belong(B, a, b, p))
    print('M belongs to the curve :',belong(M, a, b, p))
    print('The result of 7P is ;',k_p(point,a,  p, k))
    Qb = k_p(point,a,  p, k)
    print('The cipher:',crypt( k_p(point,a,  p, k), M, a, p))
    cipher = crypt( k_p(point,a,  p, k), M, a, p)
    print('The decrypted cipher:', dycrypt(point, cipher, Qb, a, b, p ))

   
if __name__ == "__main__":
    main()