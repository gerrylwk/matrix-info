import numpy as np
import matplotlib.pyplot as plt


def visualizer_text(matrix):
    """
    This function does not scale well with large matrices due to text drawing.
    More for debugging small matrices
    """
    # Create the plot
    fig, ax = plt.subplots()
    cax = ax.matshow(matrix, cmap="coolwarm")

    # Add a color bar
    plt.colorbar(cax)

    # Calculate the font size based on the figure size and matrix size
    num_rows, num_cols = matrix.shape
    cell_width = fig.get_figwidth() / num_cols
    cell_height = fig.get_figheight() / num_rows
    font_size = min(cell_width, cell_height) * 20  # Adjust multiplier as needed

    # Loop over data dimensions and create text annotations with scaled font size
    for i in range(num_rows):
        for j in range(num_cols):
            ax.text(
                j,
                i,
                str(matrix[i, j]),
                va="center",
                ha="center",
                fontsize=font_size,
                color="black",
            )

    # Set axis labels
    ax.set_xlabel("Column Index")
    ax.set_ylabel("Row Index")

    # Remove ticks for a cleaner look
    ax.set_xticks([])
    ax.set_yticks([])

    # Show the plot
    plt.show()


def visualizer_colour(matrix):
    """
    VIsualizer for larger matrix, only uses colour for representation, no text drawn
    """
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 7))  # Adjust the figure size as needed
    cax = ax.matshow(matrix, cmap="viridis")  # Use a perceptually uniform colormap

    # Add a color bar to indicate value ranges
    plt.colorbar(cax)

    # Optionally, you can remove the axis ticks and labels to focus on the color
    ax.set_xticks([])
    ax.set_yticks([])

    # Show the plot
    plt.show()


if __name__ == "__main__":
    # Example 2D matrix
    small_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    visualizer_text(small_matrix)

    # Example 1080 by 1920 matrix with random integer values
    large_matrix = np.random.randint(0, 100, size=(1080, 1920))
    visualizer_colour(large_matrix)
