from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplWidget(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.figure =  Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axes = self.figure.add_subplot(111)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)