class TreeNode:

    def __init__(self, value):
        self.value = value
        self.children = []
        self.parent = None

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def remove_child(self, child_node):
        self.children.remove(child_node)
        child_node.parent = None

    def is_root(self):
        return self.parent == None
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def __str__(self):
        return f"TreeNode({self.value})"
    
    def __repr__(self):
        return self.__str__()