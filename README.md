# 🧩 Matrix Information Storage: Test Script Collection

## Requirements
```python
pip install numpy shapely rasterio matplotlib
```

## Problem Statement

Given a 2D matrix of size `m x n`, where each cell represents different types of categorical information, write scripts that:

1. **Store Information:** Implement functions to efficiently store information in the matrix.
2. **Retrieve Information:** Develop algorithms to retrieve specific types of information based on matrix values.

---

## Input/Output

- **Input:** A matrix `M` of size `m x n`, where `m` and `n` are integers representing the number of rows and columns respectively. FOr simplicity's sake, we only work on 2-d matrices for now, but the solution can hopefully extend to N-dimensional matrices.
- **Output:** Results from various operations such as storing, retrieving.

---

## Example

```python
# Example matrix M (3x3)
M = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Example Operation 1: Retrieve information at position (1, 2)
result = retrieve_info(M, 1, 2)  # Output: 6

# Example Operation 2: Analyze pattern in the matrix
patterns = analyze_matrix(M)
# Output: Patterns identified: Diagonal sequence [1, 5, 9]


```

## Background
Came across a problem where I had to store information pertaining to every cell in a 2-dimensional matrix. Upon the need for retrieval, there is a need to check for information residing in a particular cell. I started to get interested in this problem as it can be extended to store all types of categorical information, e.g. strings/funcs/data structures.

## Updates
3/9/2024: Initial repo created. Helper functions to create and visualise matrices added.