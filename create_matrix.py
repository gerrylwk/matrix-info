import numpy as np
from visualise import visualizer_text, visualizer_colour


def create_matrix(rows, cols):
    # Create a matrix filled with zeros (initial state)
    return np.zeros((rows, cols), dtype=int)


# Function to add information to a matrix cell
def add_information(matrix, row, col, information_value):
    # NOTE: Context here is that we are storing information using bits.
    matrix[row, col] |= information_value


def has_information(matrix, row, col, information_value):
    return (matrix[row, col] & information_value) != 0


if __name__ == "__main__":
    # Example usage
    matrix = create_matrix(3, 3)
    # Assume information 1, 2, 3 correspond to bit values 1, 2, and 4 respectively.
    add_information(matrix, 0, 0, 1)  # Add Information 1
    add_information(matrix, 0, 0, 2)  # Add Information 2
    add_information(matrix, 1, 1, 4)  # Add Information 3
    add_information(matrix, 0, 0, 10)

    visualizer_text(matrix)

    # Example usage
    # Check if Information 1 is present in matrix[0, 0]
    info_1_present = has_information(matrix, 0, 0, 1)
    print(f"Information 1 present in cell (0, 0): {info_1_present}")

    # Check if Information 3 is present in matrix[1, 1]
    # NOTE: Checking for info 3 requires you to check for value 2^(3-1) = 4
    info_3_present = has_information(matrix, 1, 1, 4)
    print(f"Information 3 present in cell (1, 1): {info_3_present}")
