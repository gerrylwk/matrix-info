import numpy as np
from visualise import visualizer_text, visualizer_colour
from polygons import create_mask
from typing import List, Dict


def create_matrix(rows, cols):
    # Create a matrix filled with zeros (initial state)
    return np.zeros((rows, cols), dtype=int)


# Function to add information to a matrix cell
def add_information(matrix, row, col, information_value):
    # NOTE: Context here is that we are storing information using bits.
    matrix[row, col] |= information_value


# Function to check if information is present in the cell
def has_information(matrix, row, col, information_value):
    return (matrix[row, col] & information_value) != 0


# Function to generate an index:category dictionary
def generate_categorical_dict(lst: List):
    categorical_map = {i: v for i, v in enumerate(lst)}
    return categorical_map


def create_categorical_matrix(category_coordinates_map: Dict, rows: int, cols: int):
    cat_value_to_category_id = {}
    category_id_to_cat_value = {}
    matrix = create_matrix(rows, cols)

    for category_id, polygon_coordinates in sorted(category_coordinates_map.items()):
        print(
            f"Category ID {category_id} has polygon_coordinates:{polygon_coordinates}"
        )
        if category_id in category_id_to_cat_value:
            cat_value = category_id_to_cat_value[category_id]
        else:
            start_value = len(cat_value_to_category_id)
            cat_value = 2**start_value
            category_id_to_cat_value[category_id] = cat_value
            cat_value_to_category_id[cat_value] = category_id

        # create mask for zone
        mask = create_mask(polygon_coordinates, rows, cols)

        # Fills the INSIDE of the polygon mask with the specified value
        filled_indices = np.where(mask)
        filled_coordinates = list(zip(filled_indices[0], filled_indices[1]))

        # mark frame matrix with zone value of view_zone. If category_id's index = 2, then value on matrix would be cur_value + 2**i
        for coords in filled_coordinates:
            # Value of 1 represents background zone
            # This value replaced as soon as there is a proper zone with View Zone ID
            add_information(matrix, coords[0], coords[1], cat_value)

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
