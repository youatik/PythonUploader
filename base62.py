#generates a base 62 alphanumeric string based on unix timestamp

import random
import string
import time

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_unique_identifier():
    # Get the current Unix time as a string
    current_time = str(int(time.time()))

    # Generate 6 random digits
    random_digits = ''.join(random.choices(string.digits, k=6))

    # Combine the Unix time and random digits
    unique_identifier = current_time + random_digits

    return unique_identifier

def encode(unique_identifier, alphabet):

    unique_number = int(unique_identifier)

    if unique_number == 0:
        return alphabet[0]

    arr = []
    arr_append = arr.append
    _divmod = divmod
    base = len(alphabet)

    while unique_number:
        unique_number, rem = _divmod(unique_number, base)
        arr_append(alphabet[rem])

    arr.reverse()
    return ''.join(arr)

# Generate a unique identifier
unique_identifier = generate_unique_identifier()

# Convert the unique identifier to base 62
base62_result = encode(unique_identifier, BASE62)

# Print the base 62 representation
print("Base 62 Representation:", base62_result)
