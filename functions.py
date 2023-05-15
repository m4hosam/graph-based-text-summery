import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from interface import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PlotCanvas import PlotCanvas

class MainWindow(object):
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.NagivationGroupBox.hide()
        self.ui.BrowseButton.clicked.connect(self.browsefiles)
        self.ui.ProcessButton.clicked.connect(self.switchToMain)
        self.ui.SummaryNav_Radio.clicked.connect(self.switchToSummary)
        self.ui.GraphNav_Radio.clicked.connect(self.switchToGraph)
        self.ui.OriginalNav_Radio.clicked.connect(self.switchToOriginal)
        self.ui.ReloadButton.clicked.connect(self.reloadGraph)
        self.m = PlotCanvas()
        self.ui.GraphLayout.addWidget(self.m.canvas)
        self.ui.GraphLayout.addWidget(self.m.toolbar)

    def show(self):
        self.main_win.show()
    
    def generateCanvas(self):
        self.m.plot()
        
    def switchToMain(self):
        if(self.ui.FileNameTextEdit.text() == ""):
            self.ui.ErrorLabel.setText("please choose a file")
            return
        elif not os.path.isfile(self.ui.FileNameTextEdit.text()):
            self.ui.ErrorLabel.setText("file does not exist")
            return
        elif not self.ui.FileNameTextEdit.text().endswith('.txt'):
            self.ui.ErrorLabel.setText("invalid file format")
            return
        
        self.ui.NagivationGroupBox.show()
        self.ui.GraphNav_Radio.setChecked(True)
        #call networkx graph function to generate graph
        #display graph with matplotlib
        self.ui.stackedWidget.setCurrentIndex(1)

        fname = self.ui.FileNameTextEdit.text()
        file = open(fname,'r')
        fileContent = file.read()
        self.ui.OriginalTextBrowser.setText(fileContent)
        #run summary function
        self.ui.SummaryTextBrowser.setText(fileContent)

        #run ROUGE function and display score

    def switchToGraph(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def switchToSummary(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def switchToOriginal(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def reloadGraph(self):
        benzerlikThreshold = self.ui.BenzerlikThresholdTextEdit.toPlainText()
        benzerlikThreshold2 = self.ui.BenzerlikThresholdTextEdit_2.toPlainText()

        if benzerlikThreshold == "" or benzerlikThreshold2 == "":
            self.ui.optionsErrorLabel.setText("please enter numbers into both fields")
            return
        elif not benzerlikThreshold.isnumeric() or not benzerlikThreshold2.isnumeric():
            self.ui.optionsErrorLabel.setText("please make sure both fields contain only numbers")
            return
        
        #run graph function
        #run summary function
        #redraw graph and rewrite summary
        
        self.generateCanvas()
        self.ui.optionsErrorLabel.setText("")
        print(benzerlikThreshold, benzerlikThreshold2)
        print(int(benzerlikThreshold) + int(benzerlikThreshold2))



    def browsefiles(self):
        try:
            fname = QFileDialog.getOpenFileName(None,'Open file', 'C:','Text files (*.txt)')
            self.ui.FileNameTextEdit.setText(fname[0])
        except:
           print("error occurred")


        

app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
sys.exit(app.exec_())