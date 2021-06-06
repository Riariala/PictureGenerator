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
            self.origPict = self.population.individs[self.pictNum-1].copyIndivid()
        self.initUI()

    def initUI(self):
        self.img = Image.new("RGB",  (self.canvaSize[0],self.canvaSize[1]), 'white')
        if self.pictNum > 0 and self.pictNum <=len(self.population.individs):
            self.img = self.population.individs[self.pictNum-1].img
            self.imgDraw = self.population.individs[self.pictNum-1].imgDrawn

    def drawImage(self):
        qim = ImageQt(self.img)
        pixmap = QPixmap(QImage(qim))
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        lbl.show()

    def changeImage(self):
        self.img = Image.new("RGB", (self.canvaSize[0],self.canvaSize[1]), 'white')
        if self.pictNum > 0 and self.pictNum <=len(self.population.individs):
            self.img = self.population.individs[self.pictNum-1].img
            self.imgDraw = self.population.individs[self.pictNum-1].imgDrawn

    def incrPictNum(self):
        if self.pictNum < len(self.population.individs):
            return self.pictNum + 1
        return 1

    def decrPictNum(self):
        print(self.pictNum)
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
        print(name)
        for address, dirs, files in os.walk("savedpict//"):
            nameaddition = ".jpg"
            print(name)
            while (name + nameaddition) in files:
                count += 1
                nameaddition = "(" + str(count) +").jpg"
                print(name, files, nameaddition)

        if count != 0:
            name += nameaddition
        else:
            name += ".jpg"
        savename = "savedpict//"+name
        self.img.save(savename)