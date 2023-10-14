import string
import time
import random


def generate_unique_identifier():
    # Get the current Unix time as a string
    current_time = str(int(time.time()))

    # Generate 6 random digits
    random_digits = ''.join(random.choices(string.digits, k=6))

    # Combine the Unix time and random digits
    unique_identifier = current_time + random_digits

    return unique_identifier


# Generate a unique identifier
unique_id = generate_unique_identifier()
print(unique_id)
