import networkx as nx
import matplotlib.pyplot as plt
from functions import *
from pyvis.network import Network


text = '''
Gallery unveils interactive tree

A Christmas tree that can receive text messages has been unveiled at London's Tate Britain art gallery.

The spruce has an antenna which can receive Bluetooth texts sent by visitors to the Tate. The messages will be "unwrapped" by sculptor Richard Wentworth, who is responsible for decorating the tree with broken plates and light bulbs. It is the 17th year that the gallery has invited an artist to dress their Christmas tree. Artists who have decorated the Tate tree in previous years include Tracey Emin in 2002.

The plain green Norway spruce is displayed in the gallery's foyer. Its light bulb adornments are dimmed, ordinary domestic ones joined together with string. The plates decorating the branches will be auctioned off for the children's charity ArtWorks. Wentworth worked as an assistant to sculptor Henry Moore in the late 1960s. His reputation as a sculptor grew in the 1980s, while he has been one of the most influential teachers during the last two decades. Wentworth is also known for his photography of mundane, everyday subjects such as a cigarette packet jammed under the wonky leg of a table.
'''

# Split the text into lines
title, document = separate_title_and_paragraph(text)


theme_words_arr = theme_words(document)


def visualize_graph(G, min_score):
    # Add edge_count attribute to the nodes
    print("\n\nOZET\n\n\n\n")

    for node in G.nodes():
        edge_count = sum(1 for _, _, data in G.edges(
            node, data=True) if data['similarity'] > min_score)
        G.nodes[node]['edge_count'] = edge_count
        G.nodes[node]['score'] = round(sentence_score(node, theme_words_arr,
                                                      title, edge_count/10), 4)

    for node in G.nodes():
        if G.nodes[node]['score'] >= 0.4:
            print(G.nodes[node]['score'])
            print(node)

    # Create node labels with edge_count information
    node_labels = {
        node: f"{node}\nCount: {data['edge_count']}" for node, data in G.nodes(data=True)}

    score_labels = {
        node: f"{node}\nScore: {data['score']}" for node, data in G.nodes(data=True)}

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
    nx.draw_networkx_labels(G, pos, labels=score_labels,
                            font_weight='bold', font_size=8)
    # nx.draw_networkx_labels(G, pos, labels=score_labels,
    #                         font_weight='bold', font_size=3)

    # Draw edge labels with similarity scores
    edge_labels = nx.get_edge_attributes(G, 'similarity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

    # score_labels = nx.get_edge_attributes(G, 'score')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=score_labels, font_size=6)

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
