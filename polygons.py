"""
Collection of polygon related functions
"""

from collections import defaultdict
from typing import List, Tuple
from shapely import Polygon, Point
import rasterio.features
import numpy as np
import itertools


def coordinate_string_to_tuple_array(points: str = "") -> List[Tuple[int, int]]:
    values = map(lambda x: int(float(x)), points.split(" "))
    return list(zip(values, values))


def create_mask(
    array: List[List[float]] = None, height: int = 1080, width: int = 1920
) -> np.ndarray:
    """Create a numpy boolean mask based off specified coordinates"""
    polygon = Polygon(array)
    mask = rasterio.features.geometry_mask(
        [polygon],
        out_shape=(height, width),
        transform=rasterio.transform.from_origin(
            0, height, 1, 1
        ),  # Adjust the transform as needed
        invert=True,
    )
    # Fills the INSIDE of the polygon mask with the specified value
    mask = np.flip(mask, axis=0)
    return mask


def scale_polygon_resolution(
    current_shape: Tuple[int, int] = (720, 1280),
    new_shape: Tuple[int, int] = (1080, 1920),
    coordinates=List[List[float]],
):
    height_scale_factor = new_shape[0] / current_shape[0]
    width_scale_factor = new_shape[1] / current_shape[1]

    return [
        [pair[0] * height_scale_factor, pair[1] * width_scale_factor]
        for pair in coordinates
    ]


def check_overlapping_geofences(polygons: List[Polygon]) -> List[Tuple[int, int]]:
    """
    Returns list of indices of intersecting geofences e.g. [(0,1)] -> Geofence at index 0 and 1 are intersecting
    """
    intersecting_indices = []

    # Generate all combinations of 2 polygons
    combinations = itertools.combinations(range(len(polygons)), 2)

    for i, j in combinations:
        poly1, poly2 = polygons[i], polygons[j]

        # Generate all permutations of 2 polygons
        permutations = itertools.permutations([poly1, poly2])

        for perm_poly1, perm_poly2 in permutations:
            if perm_poly1.intersects(perm_poly2):
                intersecting_indices.append((i, j))
                break

    return intersecting_indices


def resolve_zones(zone_vals: List[int], zone_val: int):
    # NOTE: Not sure why I modelled this function after coin change problem. Seems similar?
    def backtrack(index, current_val, current_combination):
        if current_val == 1:
            return
        if current_val == 0:
            combinations.append(current_combination)
            return
        if current_val < 0 or index >= len(zone_vals):
            return

        # Include the current zone in the combination
        new_combination = current_combination + [zone_vals[index]]
        backtrack(index + 1, current_val - zone_vals[index], new_combination)

        # Skip current zone
        backtrack(index + 1, current_val, current_combination)

    combinations = []
    backtrack(0, zone_val, [])
    if not combinations:
        return combinations

    return combinations[0]


def zone_resolution(
    coordinate_history: List[List[int]] = None,
    matrix: np.ndarray = None,
    cat_value_to_category_id: dict = None,
):
    """
    Takes in coordinate history, and matches its value on the matrix to a category ID.
    cat_value_to_category_id is a dict that maps the value in the matrix to its correct category id
    """
    zone_history = []
    matrix_zone_values = list(cat_value_to_category_id)
    for coord in coordinate_history:
        cur_zone_val = matrix[coord[1], coord[0]]
        possible_zone_values = resolve_zones(matrix_zone_values, cur_zone_val)
        possible_zone_ids = [
            cat_value_to_category_id[val] for val in possible_zone_values if val
        ]

        zone_history.append(possible_zone_ids)
    return zone_history
