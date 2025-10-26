from collections import deque
from tree_node import TreeNode

#numbers = [1, 2, 3, 4, 5, 6]
#print(numbers)

#queue = deque([1,2,3,4,5])
#print(queue[0]) # The first element
#print(queue[-1]) # The last elements

#queue.append(6)
#print(queue[-1]) # The last elements

#queue.appendleft(0)
#print(queue)

#a = queue.pop()
#print(queue, a)

#b = queue.popleft()
#print(queue, b)

def BFS(root):
    if not root.is_root():
        return []
    
    result = []
    queue = deque([root])

    while(queue):
        node = queue.popleft()
        result.append(node.value)

        for child in node.children:
            queue.append(child)

    return result

def BFS_find_value(root, target):
    if not root.is_root():
        return []
    
    queue = deque([root])

    while(queue):
        node = queue.popleft()
        if node.value == target:
            return node

        for child in node.children:
            queue.append(child)

    return None
    
def DFS(root):
    if not root.is_root():
        return []
    
    result = []
    stack = [root]

    while(stack):
        node = stack.pop()
        result.append(node.value)

        for child in reversed(node.children):
            stack.append(child)

    return result

def DFS_find_value(root, target):
    if not root.is_root():
        return []
    
    stack = [root]

    while(stack):
        node = stack.pop()
        if node.value == target:
            return node

        for child in node.children:
            stack.append(child)

    return None

a = TreeNode("A")
b = TreeNode("B")
c = TreeNode("C")
d = TreeNode("D")
e = TreeNode("E")
f = TreeNode("F")
h = TreeNode("H")

a.add_child(b)
a.add_child(c)
b.add_child(d)
b.add_child(e)
c.add_child(f)

b_list = BFS(a)
print(b_list)

d_list = DFS(a)
print(d_list)

node_found = BFS_find_value(a, "H")
print(node_found)

node_found = DFS_find_value(a, "C")
print(node_found)
