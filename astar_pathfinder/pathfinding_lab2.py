from weight_node import WeightedNode,WeightedGraph
from DijkstraAlgorithm import DijkstraAlgorithm
from AStarAlgorithm import AStarAlgorithm

graph = WeightedGraph()
graph.add_node('A', 0, 0)
graph.add_node('B', 0, 1)
graph.add_node('C', 1, 1)
graph.add_node('D', 0, 2)
graph.add_node('E', 1, 2)

graph.add_edge('A', 'B', 1)
graph.add_edge('A', 'C', 9)
graph.add_edge('B', 'D', 1)
graph.add_edge('C', 'D', 1)
graph.add_edge('C', 'E', 1)
graph.add_edge('D', 'E', 1)

print(graph)

#path = DijkstraAlgorithm.find_shortest_path(graph, 'A', 'E')
#print(path)

path = AStarAlgorithm.find_shortest_path(graph, 'A', 'E')
print(path)