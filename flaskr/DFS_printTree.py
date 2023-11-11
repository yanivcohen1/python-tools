class TreeNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def printTree(node, level=0):
    if node != None:
        # print(' ' * 4 * level + '-> ' + str(node.value)) # print from top to bottom, print left first
        printTree(node.right, level + 1)
        val = ""
        try: val = node.value
        except: val = node.val
        print(' ' * 4 * level + '-> ' + str(val)) # print from left to top and then to right, print left first
        printTree(node.left, level + 1)
        # print(' ' * 4 * level + '-> ' + str(node.value)) # print from bottom to top, print left first

class ListNode:
    def __init__(self, x, next=None):
        self.val = x
        self.next = next

def printList(list: ListNode):
    while list:
        print(list.val, end=" ")
        list = list.next
    print()

if __name__ == '__main__':
    tree = TreeNode(1, TreeNode(2, TreeNode(4, TreeNode(7)),   TreeNode(9)),
            TreeNode(3, TreeNode(5),  TreeNode(6)))
    printTree(tree)
    list = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
    printList(list)
#             -> 7
#         -> 4
#     -> 2
#         -> 9
# -> 1
#         -> 5
#     -> 3
#         -> 6
