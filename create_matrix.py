import numpy as np
from visualise import visualizer_text, visualizer_colour
from polygons import create_mask
from typing import List, Dict


def create_matrix(rows, cols):
    # Create a matrix filled with zeros (initial state)
    return np.zeros((rows, cols), dtype=int)


# Function to add information to a matrix cell
def add_information(matrix, coordinates, information_value):
    # NOTE: Context here is that we are storing information using bits.
    rows, cols = coordinates
    if isinstance(rows, int) and isinstance(cols, int):
        matrix[rows, cols] |= information_value  # Single coordinate case
    else:
        rows, cols = coordinates
        matrix[rows, cols] |= information_value


def find_powers_of_two(value):
    """
    Find which powers of 2 sum up to the given value using bit encoding.

    Args:
    - value: Integer value that is a sum of multiples of 2.

    Returns:
    - A list of integers representing the powers of 2 that sum up to the value.
    """
    powers_of_two = []
    power = 0

    while value > 0:
        if value & 1:  # Check if the lowest bit is set
            powers_of_two.append(2**power)
        value >>= 1  # Right shift to check the next bit
        power += 1

    return powers_of_two


# Function to check if information is present in the cell
def has_information(matrix, row, col, information_value):
    return (matrix[row, col] & information_value) != 0


# Function to generate an index:category dictionary
def generate_categorical_dict(lst: List):
    categorical_map = {i: v for i, v in enumerate(lst)}
    return categorical_map


# Deprecated
# def create_categorical_matrix(category_coordinates_map: Dict, rows: int, cols: int):
#     cat_value_to_category_id = {}
#     category_id_to_cat_value = {}
#     matrix = create_matrix(rows, cols)

#     for category_id, polygon_coordinates in sorted(category_coordinates_map.items()):
#         print(
#             f"Category ID {category_id} has polygon_coordinates:{polygon_coordinates}"
#         )
#         if category_id in category_id_to_cat_value:
#             cat_value = category_id_to_cat_value[category_id]
#         else:
#             start_value = len(cat_value_to_category_id)
#             cat_value = 2**start_value
#             category_id_to_cat_value[category_id] = cat_value
#             cat_value_to_category_id[cat_value] = category_id

#         # create mask for zone
#         mask = create_mask(polygon_coordinates, rows, cols)

#         # Fills the INSIDE of the polygon mask with the specified value
#         filled_indices = np.where(mask)

#         # mark frame matrix with zone value of view_zone. If category_id's index = 2, then value on matrix would be cur_value + 2**i
#         # Value of 1 represents background zone
#         # This value replaced as soon as there is a proper zone with View Zone ID
#         add_information(matrix, filled_indices, cat_value)

#         # For visualisation
#         # from PIL import Image

#         # tmp_matrix = np.zeros(matrix.shape)
#         # tmp_matrix[mask] = 255
#         # tmp_matrix_img = Image.fromarray(tmp_matrix)
#         # tmp_matrix_img = tmp_matrix_img.convert("L")
#         # tmp_matrix_img.save(f"matrix_view-{category_id}.png")

#     # For visualising final drawn frame
#     # unique_elements, inverse_indices = np.unique(matrix, return_inverse=True)
#     # unique_colors = np.random.randint(
#     #     0, 256, size=(len(unique_elements), 3), dtype=np.uint8
#     # )
#     # colored_matrix = unique_colors[inverse_indices]
#     # colored_matrix = colored_matrix.reshape((rows, cols, 3))
#     # matrix_img = Image.fromarray(colored_matrix.reshape(rows, cols, 3))
#     # matrix_img.save(f"final_matrix_view.png")

#     return cat_value_to_category_id, category_id_to_cat_value, matrix


def create_categorical_matrix(
    category_coordinates_map: Dict, rows: int, cols: int
) -> np.ndarray:
    cat_value_to_category_id = {}
    category_id_to_cat_value = {}

    # Initialize an empty matrix with the same size for summing the masks later
    matrix = np.zeros((rows, cols), dtype=int)

    # Iterate over each category and polygon coordinates
    for category_id, polygon_coordinates in sorted(category_coordinates_map.items()):
        print(
            f"Category ID {category_id} has polygon_coordinates: {polygon_coordinates}"
        )

        # Determine the category value (cat_value) for this category_id
        if category_id in category_id_to_cat_value:
            cat_value = category_id_to_cat_value[category_id]
        else:
            start_value = len(cat_value_to_category_id)
            cat_value = 2**start_value
            category_id_to_cat_value[category_id] = cat_value
            cat_value_to_category_id[cat_value] = category_id

        # Create a mask for the current polygon coordinates
        mask = create_mask(polygon_coordinates, rows, cols)

        # Visualize the current mask (optional)
        # visualizer_colour(mask)

        # Multiply the mask by the current cat_value to differentiate it from other categories
        cat_value_mask = mask * cat_value
        # visualizer_colour(cat_value_mask)

        # Sum the current mask elementwise into the final matrix
        matrix = np.add(matrix, cat_value_mask)

        # For visualisation
        # from PIL import Image

        # tmp_matrix = np.zeros(matrix.shape)
        # tmp_matrix[mask] = 255
        # tmp_matrix_img = Image.fromarray(tmp_matrix)
        # tmp_matrix_img = tmp_matrix_img.convert("L")
        # tmp_matrix_img.save(f"matrix_view-{category_id}.png")

    # For visualising final drawn frame
    # unique_elements, inverse_indices = np.unique(matrix, return_inverse=True)
    # unique_colors = np.random.randint(
    #     0, 256, size=(len(unique_elements), 3), dtype=np.uint8
    # )
    # colored_matrix = unique_colors[inverse_indices]
    # colored_matrix = colored_matrix.reshape((rows, cols, 3))
    # matrix_img = Image.fromarray(colored_matrix.reshape(rows, cols, 3))
    # matrix_img.save(f"final_matrix_view.png")

    return cat_value_to_category_id, category_id_to_cat_value, matrix


if __name__ == "__main__":
    # Example usage
    matrix = create_matrix(3, 3)
    # Assume information 1, 2, 3 correspond to bit values 1, 2, and 4 respectively.
    add_information(matrix, [0, 0], 1)  # Add Information 1. Matrix value = 1
    add_information(matrix, [0, 0], 2)  # Add Information 2. Matrix value = 2
    add_information(matrix, [1, 1], 4)  # Add Information 3. Matrix value = 4
    add_information(matrix, [0, 0], 10)  # Add Information 4. Matrix value = 8

    visualizer_text(matrix)

    # Example usage
    # Check if Information 1 is present in matrix[0, 0]
    info_1_present = has_information(matrix, 0, 0, 1)
    print(f"Information 1 present in cell (0, 0): {info_1_present}")

    # Check if Information 3 is present in matrix[1, 1]
    # NOTE: Checking for info 3 requires you to check for value 2^(3-1) = 4
    info_3_present = has_information(matrix, 1, 1, 4)
    print(f"Information 3 present in cell (1, 1): {info_3_present}")

    # Check which powers of 2 are present in matrix[1,1]
    powers_present = find_powers_of_two(matrix[1, 1])
    print(f"Powers of 2 present in cell (1, 1): {powers_present}")

    powers_present = find_powers_of_two(matrix[0, 0])
    # Check which powers of 2 are present in matrix[0,0]
    print(f"Powers of 2 present in cell (0, 0): {powers_present}")
