from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt_AES(key, plaintext):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
    iv = cipher.iv
    return ct_bytes, iv

def decrypt_AES(key, ct_bytes, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
    return pt

def main():
    key = get_random_bytes(16)

    plaintext = input("Entrez le message à chiffrer: ").encode()

    ct, iv = encrypt_AES(key, plaintext)
    print("Message chiffré:", ct.hex())

    decrypted = decrypt_AES(key, ct, iv)
    print("Message déchiffré:", decrypted.decode())

if __name__ == "__main__":
    main()