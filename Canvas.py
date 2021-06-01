import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

class Communicate(QObject):

    updateBW = pyqtSignal(int)

class Canvas(QWidget):
    
    def __init__(self, _population, nm):
        super().__init__()
        self.population = _population
        self.canvaSize = self.population.canvaSize
        self.pictNum = nm
        self.origPict = 0
        if self.population.individs:
            self.origPict = self.population.individs[self.pictNum-1]
        self.initUI()

    def initUI(self):
        #if self.pictNum <= len(self.population.individs):
        #save button here
        self.img = Image.new("RGB",  (self.canvaSize[0],self.canvaSize[1]), 'white')
        self.imgDraw = ImageDraw.Draw(self.img)
        ##print(self.pictNum)
        if self.pictNum > 0 and self.pictNum <=len(self.population.individs):
            print(self.pictNum, len(self.population.individs), self.population.individs[self.pictNum-1].gen[0], self.canvaSize)
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
        #self.show()

    def changeImage(self):
        self.img = Image.new("RGB", (self.canvaSize[0],self.canvaSize[1]), 'white')
        self.imgDraw = ImageDraw.Draw(self.img)
        if self.pictNum > 0 and self.pictNum <=len(self.population.individs):
            self.imgDraw = self.population.individs[self.pictNum-1].paintIndivid(self.imgDraw)

    def incrPictNum(self):
        if self.pictNum < len(self.population.individs):
            return self.pictNum + 1
        return 1

    def decrPictNum(self):
        if self.pictNum > 1:
            return self.pictNum - 1
        return len(self.population.individs)

    def savePicture(self):
        if not os.path.isdir("savedpict"):
            os.mkdir("savedpict")
        name = self.population.individs[self.pictNum-1].name
        if not name:
            name = "untitled"
        count = 0
        for address, dirs, files in os.walk("savedpict//"):
            nameaddition = ".jpg"
            while (name + nameaddition) in files:
                count += 1
                nameaddition = "(" + str(count) +").jpg"
                print(name, files, nameaddition)
        #count = len([files for address, dirs, files in os.walk("savedpict//") if name in files]) ###
        if count != 0:
            name += nameaddition
        savename = "savedpict//"+name
        self.img.save(savename)