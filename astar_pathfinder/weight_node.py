

class WeightedNode:
    def __init__(self, value, x, y):
        self.value = value
        self.neighbors = {}
        self.visted = False
        self.x = x
        self.y = y
        self.distance = float('inf')
        self.previous = None

    def add_neighbor(self, neighbor, weight):
        self.neighbors[neighbor] = weight

    def __str__(self):
        return f"weightedNode({self.value})"
    
    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        return self.distance < other.distance
    

class WeightedGraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, value, x, y):
        if value not in self.nodes:
            self.nodes[value] = WeightedNode(value, x, y)

        return self.nodes[value]
    
    def reset_nodes(self):
        for node in self.nodes.values():
            node.visted = False
            node.distance = float('inf')
            node.previous = None
    
    def add_edge(self, from_value, to_value, weight):
        # TODO: Refactor this!
        from_node = self.add_node(from_value, 0, 0)
        to_node = self.add_node(to_value, 0, 0)
        from_node.add_neighbor(to_node, weight)

    def get_node(self, value):
        return self.nodes.get(value)

    def __str__(self):
        edges = []
        for value, node in self.nodes.items():
            for neightbor, weight in node.neighbors.items():
                edges.append(f"{value} -- ({weight}) -- {neightbor.value}")

        print(edges)

        return f"WeightGraph({len(self.nodes)} nodes, {len(edges)} edges)"