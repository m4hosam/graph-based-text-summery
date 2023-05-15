import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5,height=4,dpi=100):
        self.figure = plt.figure()
  
        self.canvas = FigureCanvas(self.figure)
  
        self.toolbar = NavigationToolbar(self.canvas, None)

    def plot(self):
        data = [random.random() for i in range(10)]
  
        # clearing old figure
        self.figure.clear()
  
        # create an axis
        ax = self.figure.add_subplot(111)
  
        # plot data
        ax.plot(data, '*-')
  
        # refresh canvas
        self.canvas.draw()