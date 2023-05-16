import networkx as nx
import matplotlib.pyplot as plt

from pyvis.network import Network


def visualize_graph(G, min_score):
    # Add edge_count attribute to the nodes
    for node in G.nodes():
        edge_count = sum(1 for _, _, data in G.edges(
            node, data=True) if data['similarity'] > min_score)
        G.nodes[node]['edge_count'] = edge_count

    # Create node labels with edge_count information
    node_labels = {
        node: f"{node}\nCount: {data['edge_count']}" for node, data in G.nodes(data=True)}

    pos = nx.spring_layout(G, seed=42)

    # Get the edges with similarity scores greater than min_score
    green_edges = [(u, v) for (u, v, d) in G.edges(
        data=True) if d["similarity"] >= min_score]
    gray_edges = [(u, v) for (u, v, d) in G.edges(
        data=True) if d["similarity"] < min_score]

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1000)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=green_edges,
                           edge_color="g", width=2)
    nx.draw_networkx_edges(G, pos, edgelist=gray_edges,
                           edge_color="gray", width=0.5)

    # Draw node labels with edge_count information
    nx.draw_networkx_labels(G, pos, labels=node_labels,
                            font_weight='bold', font_size=8)

    # Draw edge labels with similarity scores
    edge_labels = nx.get_edge_attributes(G, 'similarity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

    # Show the plot
    plt.show()


def visualize_graph_pyvis(G):
    # Create a PyVis network
    net = Network(notebook=True)

    # Add nodes and edges to the network
    for node in G.nodes():
        net.add_node(node)

    for edge in G.edges(data=True):
        node1, node2, attributes = edge
        similarity = attributes["similarity"]
        if similarity > 0.7:
            color = "green"
        else:
            color = "gray"
        net.add_edge(node1, node2, value=similarity, color=color)

    # Show the network
    net.show("graph.html")


'''
# Assume G is your graph with edges having a "similarity" attribute
G = nx.Graph()
G.add_nodes_from(["A", "B", "C", "D"])
G.add_edges_from([("A", "B", {"similarity": 0.9}), ("A", "C", {"similarity": 0.6}),
                  ("B", "D", {"similarity": 0.8}), ("C", "D", {"similarity": 0.3})])

# Visualize the graph
visualize_graph(G)

# Visualize the graph using PyVis
visualize_graph_pyvis(G)
'''
