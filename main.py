import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
import re

replacements = {
    'sin' : 'np.sin',
    'cos' : 'np.cos',
    'tan' : 'np.tan',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    '^': '**',
}

allowed_words = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
    'z',
    'tan'
]

def string2func(string):
    ''' evaluates the string and returns a function of x '''
    # find all words and check if all are allowed:
    for word in re.findall('[a-zA-Z_]+', string):
        if word not in allowed_words:
            return False

    for old, new in replacements.items():
        string = string.replace(old, new)

    def func(x):
        return eval(string)

    return func

class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)

        # self.setFixedWidth(500)
        # self.setFixedSize(500,500)
        self.setWindowTitle("My first app")
        loadUi('mainWindow.ui',self)
        self.pushButton.clicked.connect(self.generate)
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas,self))
        self.listWidget.itemDoubleClicked.connect(self.removeSel)
      
        

    def generate(self):
        text = self.lineEdit.text()
     
        self.listWidget.addItem(text)
        self.update_graph()

        
       

    def removeSel(self):
        listItems = self.listWidget.selectedItems()
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item))
        
        self.update_graph()
        
    def update_graph(self):
        self.MplWidget.axes.cla()
        for i in range(self.listWidget.count()):
            text = self.listWidget.item(i).text()
           
            func = string2func(text)
            if func == False:
                self.listWidget.item(i).setText("INVALID EQUATION")
                continue


            x = np.linspace(-10, 10, 1000)
            y = func(x)
            self.MplWidget.axes.plot(x,y,label=text)
            self.MplWidget.axes.legend()
        self.MplWidget.canvas.draw()
    
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800,700)
    window.show()
    

    app.exec_()