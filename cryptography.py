import bcrypt


def encrypt(key, file):
    salt = bcrypt.gensalt()
    key = bcrypt.hashpw(key.encode(), salt)
    key *= int(len(file) / len(key)) + 1
    result = bytearray(file)
    for i in range(len(file)):
        result[i] ^= key[i]
    for i in range(len(file)):
        result[i], result[key[i] ** key[i] % len(result)] = result[key[i] ** key[i] % len(result)], result[i]
    return salt + bytes(result)


def decrypt(key, file):
    salt = file[:29]
    file = file[29:]
    key = bcrypt.hashpw(key.encode(), salt)
    key *= int(len(file) / len(key)) + 1
    result = bytearray(file)
    for i in range(len(file)-1, -1, -1):
        result[i], result[key[i] ** key[i] % len(result)] = result[key[i] ** key[i] % len(result)], result[i]
    for i in range(len(file)):
        result[i] ^= key[i]
    return bytes(result)


password = "Password123"
print("Password: ", password)

data = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc sed diam commodo, efficitur nisi sed, egestas mi. Nam vel consectetur justo. Aliquam sed elit velit. Nullam cursus id orci fringilla laoreet. Aliquam dictum hendrerit libero. Etiam vitae sem at orci consectetur feugiat. Mauris justo massa, lobortis a hendrerit sed, fringilla nec magna. Praesent diam arcu, lacinia id felis non, luctus varius purus. Aliquam erat volutpat. Duis ut enim sed orci placerat vulputate. Curabitur tristique fringilla dui id fermentum. Vestibulum eget consectetur mi, varius viverra purus. Donec at vestibulum leo."
print("Data:     ", data)

encrypted = encrypt(password, data)
print("Encrypted:", encrypted)

decrypted = decrypt(password, encrypted)
print("Decrypted:", decrypted)
