import numpy as np
import matplotlib.pyplot as plt

def max_adjacent_diff_in_continuous_function(arr):
    # Initialize maximum difference
    max_diff = 0

    # Iterate through adjacent elements
    for i in range(len(arr) - 1):
        # Calculate the absolute difference
        diff = abs(arr[i] - arr[i + 1])
        # Update max_diff if this difference is larger
        max_diff = max(max_diff, diff)

    return max_diff

# Example usage
# arr = [1, 2, 4, 8, 5]
# result = max_adjacent_diff(arr)
# print(result)  # Expected output: 4


def filter_array(arr, tolerance):
    """
    Processes a sorted numpy array (or list) and for any group of
    consecutive numbers where the difference between adjacent elements
    is <= tolerance, only one representative is kept.

    For a group with a single element, that element is output.
    For a group with multiple elements, the median (middle element) is chosen.

    Parameters:
        arr (list or np.array): Sorted array of numbers.
        tolerance (int or float): The maximum allowed difference to consider two
                                  adjacent numbers as "neighbors".

    Returns:
        np.array: The filtered array.
    """
    # Edge case: if array is empty, return an empty numpy array.
    if len(arr) == 0:
        return np.array([])

    # Ensure we have a numpy array
    arr = np.array(arr)

    # This will hold our final output.
    result = []
    # Start the first group with the first element.
    current_group = [arr[0]]

    # Iterate over the array, starting from the second element.
    for i in range(1, len(arr)):
        # Check the difference with the previous element.
        if abs(arr[i] - arr[i-1]) <= tolerance:
            # The numbers are "close"; include them in the current group.
            current_group.append(arr[i])
        else:
            # The chain is broken; process the current group.
            if len(current_group) == 1:
                # Only one element in the group, so simply add it.
                result.append(current_group[0])
            else:
                # For multiple elements, choose the middle element (the median).
                group_median = current_group[len(current_group)//2]
                result.append(group_median)
            # Start a new group with the current element.
            current_group = [arr[i]]

    # Process the final group after the loop ends.
    if current_group:
        if len(current_group) == 1:
            result.append(current_group[0])
        else:
            group_median = current_group[len(current_group)//2]
            result.append(group_median)

    # Return the result as a numpy array.
    return np.array(result)

def equation(x):
    return 3 * np.sin(2 * x) + 4 * np.cos(x) - 5

# Generate x values from -pi to pi
x = np.linspace(-np.pi, np.pi, 500)

# Calculate the corresponding y values
y = equation(x)

# Define a small tolerance for considering y to be near 0
tolerance = max_adjacent_diff_in_continuous_function(y) # 0.1 # min space beween points

# Extract the x and y values near zero
x_near_zero1 = x[np.abs(y) < tolerance]
x_near_zero = filter_array(x_near_zero1, tolerance)
y_near_zero = equation(x_near_zero) # y[near_zero_indices]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='y = 3 sin(2x) + 4 cos(x) - 5')

# Plot the points near zero
plt.scatter(x_near_zero, y_near_zero, color='green', marker='o', label=f'Points Near y=0 (Tolerance < {tolerance:.2f})')

# Add a horizontal line at y=0
plt.axhline(0, color='r', linestyle='--', label='y = 0')

# Add labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of 3 sin(2x) + 4 cos(x) - 5 with Points Near y=0 Highlighted')

# Add a legend
plt.legend()

# Show the solutions on the plot
for sol in x_near_zero:
    plt.annotate(f'{sol:.2f}', xy=(sol, 0), xytext=(0, 10),
        textcoords='offset points', ha='center', color='red')

# Add a grid
plt.grid(True)

# Show the plot
plt.show()
