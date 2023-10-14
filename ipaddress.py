import time
from flask import Flask, request

app = Flask(__name__)

def generate_unique_number():
    # Get the IP address and port from the Flask request object
    host, port = request.host.split(':')

    # Remove dots from the IP address
    ip_address = host.replace('.', '')

    # Concatenate the IP address, port, and current Unix timestamp
    unique_number = ip_address + port + str(int(time.time()))

    # Check if the string is empty after removing '0'
    if not unique_number:
        unique_number = '0'  # If the string is empty, set it to '0'

    return unique_number

@app.route('/')
def print_server_info():
    # Call the generate_unique_number function
    unique_number = generate_unique_number()

    # Print the generated unique number to the console
    print(f"Unique Number: {unique_number}")

    return "Unique Number printed to console."

if __name__ == '__main__':
    app.run()
