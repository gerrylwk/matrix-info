import random
import string
from create_matrix import (
    create_matrix,
    add_information,
    has_information,
    generate_categorical_dict,
)


def generate_random_strings(N=0, length=0):
    # Define the character set: lowercase, uppercase letters, and digits
    characters = string.ascii_letters + string.digits

    # Generate N random strings
    random_strings = ["".join(random.choices(characters, k=length)) for _ in range(N)]

    return random_strings

    # Example usage
    N = 5  # Number of random strings
    length = 5  # Length of each random string
    strings = generate_random_strings(N, length)
    print(strings)


if __name__ == "__main__":
    mat = create_matrix(50, 50)
    categories = generate_random_strings(N=5, length=5)
    categorical_map = generate_categorical_dict(categories)
    print(categorical_map)
