import random
import string
import math
from typing import Dict
from polygons import coordinate_string_to_tuple_array
from visualise import visualizer_colour
from create_matrix import (
    create_matrix,
    add_information,
    has_information,
    generate_categorical_dict,
    create_categorical_matrix,
)


def generate_random_strings(N=0, length=0):
    # Define the character set: lowercase, uppercase letters, and digits
    characters = string.ascii_letters + string.digits

    # Generate N random strings
    random_strings = ["".join(random.choices(characters, k=length)) for _ in range(N)]

    # Example: [10 50 100 35 90 120 111 222]
    return random_strings


def generate_random_polygon(
    num_vertices: int, width: int = 1000, height: int = 1000
) -> str:
    # Generate random points within the given width and height
    points = [
        (random.uniform(0, width), random.uniform(0, height))
        for _ in range(num_vertices)
    ]

    # Calculate the centroid of the points
    centroid = (
        sum(x for x, y in points) / num_vertices,
        sum(y for x, y in points) / num_vertices,
    )

    # Calculate the polar angle (angle from the centroid) for sorting
    def polar_angle(p):
        return math.atan2(p[1] - centroid[1], p[0] - centroid[0])

    # Sort points by the polar angle (this ensures they are ordered in a consistent manner)
    points.sort(key=polar_angle)

    # Convert the points to a string format that matches your required input
    coordinate_string = " ".join(f"{int(x)} {int(y)}" for x, y in points)

    return coordinate_string


if __name__ == "__main__":

    height, width = 50, 50
    num_categories = 5
    categories = generate_random_strings(N=num_categories, length=5)
    categorical_map = generate_categorical_dict(categories)

    category_coordinates = {
        i: coordinate_string_to_tuple_array(
            generate_random_polygon(num_categories, height, width)
        )
        for i in categorical_map
    }
    cat_value_to_category_id, category_id_to_cat_value, matrix = (
        create_categorical_matrix(category_coordinates, height, width)
    )

    print(f"All possible categorical matrix values: {cat_value_to_category_id.keys()}")
    visualizer_colour(matrix)
