from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

class Communicate(QObject):

    updateBW = pyqtSignal(int)

class Canvas(QWidget):
    
    def __init__(self, _posX, _posY, _population, nm):
        super().__init__()
        #self.position = [_posX, _posY]
        self.population = _population
        self.canvaSize = self.population.canvaSize
        self.pictNum = nm
        self.initUI()

    def initUI(self):
        self.setGeometry(900,100,self.canvaSize[0]+50,self.canvaSize[1]+50)
        self.setWindowTitle(str(self.pictNum))
        #save button here
        self.img = Image.new("RGB", (self.canvaSize[0],self.canvaSize[1]), 'white')
        self.imgDraw = ImageDraw.Draw(self.img)
        self.imgDraw = self.population.individs[self.pictNum-1].paintIndivid(self.imgDraw)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawImage()
        qp.end()

    def drawImage(self):
        qim = ImageQt(self.img)
        pixmap = QPixmap(QImage(qim))
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        self.show()


    def incrPictNum(self):
        if self.pictNum < self.population.size:
            return self.pictNum + 1
        return 1

    def decrPictNum(self):
        if self.pictNum > 1:
            return self.pictNum - 1
        return self.population.size