import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import graph,embedding,preprocessing,visualize_graph
from transformers import DistilBertModel, DistilBertTokenizer
import pprint
import networkx as nx
from visualize_graph import visualize_graph
import graph as g

import random


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5,height=4,dpi=100):
        self.figure = plt.figure()
  
        self.canvas = FigureCanvas(self.figure)
  
        self.toolbar = NavigationToolbar(self.canvas, None)

    def plot(self,sentences, similarityThreshold, model, tokenizer, model_option):
        self.figure.clear()
        
        # model_name = "distilbert-base-uncased"
        # model = DistilBertModel.from_pretrained(model_name)
        # tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        # sentences = ['The cat sits outside',
        #     'A man is playing guitar',
        #     'I love pasta',
        #     'The new movie is awesome',
        #     'The cat plays in the garden',
        #     'A woman watches TV',
        #     'The new movie is so great',
        #     'Do you like pizza?']



        similarity_matrix, graph = g.compute_sentence_similarity_graph(
            sentences, model, tokenizer, method=model_option)
        
        #visualize graph
        visualize_graph(graph, similarityThreshold)

        print("Similarity Matrix:")
        pprint.pprint(similarity_matrix)
        
        # pos = nx.spring_layout(graph, seed=42)
        # nx.draw(graph, pos, with_labels=True, font_weight='bold',
        #         node_color='skyblue', font_size=8, node_size=1000)

        # edge_labels = nx.get_edge_attributes(graph, 'similarity')
        # nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6)

        self.figure.tight_layout()
        self.canvas.draw_idle()
