import random
import string
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
    # NOTE: For now, haven't ensured that polygon edges do no intersect. Future work?
    points = [
        (random.uniform(0, width), random.uniform(0, height))
        for _ in range(num_vertices)
    ]

    # Sort points by polar angle relative to their centroid to ensure clockwise order
    centroid = (
        sum(x for x, y in points) / num_vertices,
        sum(y for x, y in points) / num_vertices,
    )

    def polar_angle(p):
        return (p[0] - centroid[0], p[1] - centroid[1])

    points.sort(key=lambda p: (polar_angle(p)[1], polar_angle(p)[0]))

    # Convert the points to a string format that matches your required input
    coordinate_string = " ".join(f"{int(x)} {int(y)}" for x, y in points)

    return coordinate_string


if __name__ == "__main__":

    height, width = 500, 500
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

    visualizer_colour(matrix)
