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
    
    def generateCanvas(self, mainText):
        self.m.plot(mainText)

    def readFile(self, fname):
        file = open(fname,'r', encoding='utf-8')
        fileContent = file.read()
        fileContent = fileContent.split('Main:')
        fileContent = fileContent[1].split('Summary:')
        newLineSep = fileContent[0].split('\n')
        fileContent = [paragraph.replace('\n','') for paragraph in fileContent]

        mainTextSentences = fileContent[0].split('.')

        summaryTextSentences = fileContent[1].split('.')

        title = [i for i in newLineSep if i][0]
        mainTextSentences = [i for i in mainTextSentences if i]
        summaryTextSentences = [i for i in summaryTextSentences if i]
        print(title)
        print(mainTextSentences)
        print(summaryTextSentences)

        return title, mainTextSentences, summaryTextSentences

        
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
        
        self.ui.GloveModel_Radio.setChecked(True)
        self.ui.NagivationGroupBox.show()
        self.ui.GraphNav_Radio.setChecked(True)
        #call networkx graph function to generate graph
        #display graph with matplotlib
        self.ui.stackedWidget.setCurrentIndex(1)

        fname = self.ui.FileNameTextEdit.text()
        [title, mainText, summaryText] = self.readFile(fname)
        seperator = '. '
        self.ui.title_label.setText(title)
        self.ui.mainText_original.setText(seperator.join(mainText))
        #run summary function
        self.ui.manualSummary_original.setText(seperator.join(summaryText))
        self.ui.manualSummary_summary.setText(seperator.join(summaryText))
        # self.ui.processedSummary_summary.setText(fileContent)

        #run ROUGE function and display score

    def switchToGraph(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def switchToSummary(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def switchToOriginal(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def reloadGraph(self):
        benzerlikThreshold = self.ui.BenzerlikThresholdTextEdit.toPlainText()
        cumleThreshold = self.ui.BenzerlikThresholdTextEdit_2.toPlainText()
        model = 'glove' if self.ui.GloveModel_Radio.isChecked() else 'bert'

        [title, mainText, summaryText] = self.readFile(self.fname)

        if benzerlikThreshold == "" or cumleThreshold == "":
            self.ui.optionsErrorLabel.setText("please enter numbers into both fields")
            return
        elif not benzerlikThreshold.isnumeric() or not cumleThreshold.isnumeric():
            self.ui.optionsErrorLabel.setText("please make sure both fields contain only numbers")
            return
        
        #run graph function
        #run summary function
        #redraw graph and rewrite summary
        
        self.generateCanvas(mainText)
        self.ui.optionsErrorLabel.setText("")
        print(model)
        print(benzerlikThreshold, cumleThreshold)
        print(float(benzerlikThreshold) + float(cumleThreshold))

    
    def browsefiles(self):
        try:
            file = QFileDialog.getOpenFileName(None,'Open file', 'C:','Text files (*.txt)')
            self.fname = file[0]
            self.ui.FileNameTextEdit.setText(self.fname)
        except:
           print("error occurred")


        

app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
sys.exit(app.exec_())