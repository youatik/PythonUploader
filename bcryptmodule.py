import os

import bcrypt


def _hash_password(salt, password):
    password = bytearray(salt + password.encode())
    for iterator in range(1, 16):
        for index in range(len(password)):
            password[index] ^= password[(index + iterator) % len(password)]
    return password


def encrypt(password, file):
    salt = os.urandom(16)
    password = _hash_password(salt, password)
    password *= int(len(file) / len(password)) + 1
    result = bytearray(file)
    for i in range(len(file)):
        result[i] ^= password[i]
    for i in range(len(file)):
        result[i], result[password[i] ** password[i] % len(result)] = result[password[i] ** password[i] % len(result)], result[i]
    return salt + bytes(result)


def decrypt(password, file):
    salt = file[:16]
    file = file[16:]
    password = _hash_password(salt, password)
    password *= int(len(file) / len(password)) + 1
    result = bytearray(file)
    for i in range(len(file)-1, -1, -1):
        result[i], result[password[i] ** password[i] % len(result)] = result[password[i] ** password[i] % len(result)], result[i]
    for i in range(len(file)):
        result[i] ^= password[i]
    return bytes(result)


password = "Password123"
print("Password: ", password)

data = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc sed diam commodo, efficitur nisi sed, egestas mi. Nam vel consectetur justo. Aliquam sed elit velit. Nullam cursus id orci fringilla laoreet. Aliquam dictum hendrerit libero. Etiam vitae sem at orci consectetur feugiat. Mauris justo massa, lobortis a hendrerit sed, fringilla nec magna. Praesent diam arcu, lacinia id felis non, luctus varius purus. Aliquam erat volutpat. Duis ut enim sed orci placerat vulputate. Curabitur tristique fringilla dui id fermentum. Vestibulum eget consectetur mi, varius viverra purus. Donec at vestibulum leo."
print("Data:     ", data)

encrypted = encrypt(password, data)
print("Encrypted:", encrypted)

decrypted = decrypt(password, encrypted)
print("Decrypted:", decrypted)
