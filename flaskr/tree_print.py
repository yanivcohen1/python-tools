class TreeNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# Function to build ASCII representation of a binary tree
# Returns list of strings, width, height, and horizontal coordinate of the root


def build_ascii_tree(node):
    if node is None:
        return [], 0, 0, 0

    # Recursively build left and right subtrees
    left_lines, left_width, left_height, left_middle = build_ascii_tree(node.left)
    right_lines, right_width, right_height, right_middle = build_ascii_tree(node.right)

    value_str = str(node.value)
    root_width = len(value_str)

    # Compute positions
    height = max(left_height, right_height) + 2
    width = left_width + root_width + right_width + 2
    middle = left_width + root_width // 2 + 1

    # Prepare a blank canvas
    lines = [" " * width for _ in range(height)]

    # Place root value
    root_pos = left_width + 1
    lines[0] = lines[0][:root_pos] + value_str + lines[0][root_pos + root_width :]

    # Draw branches
    if node.left:
        left_root = left_middle + 1
        lines[1] = lines[1][:left_root] + "/" + lines[1][left_root + 1 :]
        for i in range(left_root + 1, root_pos):
            lines[1] = lines[1][:i] + "_" + lines[1][i + 1 :]
    if node.right:
        right_root = left_width + root_width + 1 + right_middle
        lines[1] = (
            lines[1][: root_pos + root_width]
            + "\\"
            + lines[1][root_pos + root_width + 1 :]
        )
        for i in range(root_pos + root_width + 1, right_root):
            lines[1] = lines[1][:i] + "_" + lines[1][i + 1 :]

    # Merge left and right subtree lines safely
    for i in range(max(left_height, right_height)):
        left_part = left_lines[i] if i < left_height else " " * left_width
        right_part = right_lines[i] if i < right_height else " " * right_width
        lines[i + 2] = left_part + " " * (width - left_width - right_width) + right_part

    return lines, width, height, middle


# Function to print the built ASCII tree


def print_ascii_tree(node):
    lines, *_ = build_ascii_tree(node)
    for line in lines:
        print(line.rstrip())


# Example usage
if __name__ == "__main__":
    # Construct the tree
    t = TreeNode(1,
        TreeNode(2, TreeNode(4, TreeNode(7)), TreeNode(9)),
        TreeNode(3, TreeNode(5), TreeNode(6)),
    )

    # Print the tree in a centered ASCII layout
    print_ascii_tree(t)
#              1
#         /____ \___
#        2           3
#      /_ \        /_ \
#     4     9     5     6
#   /_
#  7
