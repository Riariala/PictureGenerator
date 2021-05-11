from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QCoreApplication, Qt
import sys

import Population
import Canvas

class Interface(QMainWindow):

    def __init__(self):
        super().__init__()
        self.layout = 0
        self.setGeometry(20,30,1500,850)
        self.population = Population.Population()
        self.GenerCanvas = []
        self.initUI()
        self.setAnotherLay()
        self.examleOfWork = []

    def initUI(self):
                #Generation
        self.setWindowTitle("Step 0: Generetion")
        self.GNext = QtWidgets.QPushButton("К отбору", self)
        self.GNext.move(1350, 800)
        self.GNext.clicked.connect(self.chageLay)

        self.GenerateBtn = QtWidgets.QPushButton("Генерировать", self)
        self.GenerateBtn.move(100, 800)
        self.GenerateBtn.clicked.connect(self.generateEvent)

        self.PopSizeSetter = QtWidgets.QLineEdit(self)
        self.PopSizeSetter.move(60, 100)
        self.PopSizeSetter.textChanged[str].connect(self.population.setSize)

        self.XLabel =  QLabel(self)
        self.XLabel.move(50,150)
        self.XLabel.setText("X")
        self.CanvasSizeSetterX = QtWidgets.QLineEdit(self)
        self.CanvasSizeSetterX.move(60, 150)
        self.CanvasSizeSetterX.textChanged[str].connect(self.population.setcanvaSizeX)
        self.YLabel =  QLabel(self)
        self.YLabel.move(190,150)
        self.YLabel.setText("Y")
        self.CanvasSizeSetterY = QtWidgets.QLineEdit(self)
        self.CanvasSizeSetterY.move(200, 150)
        self.CanvasSizeSetterY.textChanged[str].connect(self.population.setcanvaSizeY)

        self.circleLabel =  QLabel(self)
        self.circleLabel.move(50,190)
        self.circleLabel.setText("circles")
        self.circleSetter = QtWidgets.QLineEdit(self)
        self.circleSetter.move(60, 220)
        self.circleSetter.textChanged[str].connect(self.population.setCircleCount)

        self.rectLabel =  QLabel(self)
        self.rectLabel.move(50,270)
        self.rectLabel.setText("rectangles")
        self.rectSetter = QtWidgets.QLineEdit(self)
        self.rectSetter.move(60, 300)
        self.rectSetter.textChanged[str].connect(self.population.setRectCount)

        self.lineLabel =  QLabel(self)
        self.lineLabel.move(50,350)
        self.lineLabel.setText("lines")
        self.lineSetter = QtWidgets.QLineEdit(self)
        self.lineSetter.move(60, 380)
        self.lineSetter.textChanged[str].connect(self.population.setLineCount)
        
        
                #Selection
        self.SNext = QtWidgets.QPushButton("К скрещиванию", self)
        self.SNext.move(1350, 800)
        self.SNext.clicked.connect(self.chageLay)
        self.SNext.hide()
        self.ImgNext = QtWidgets.QPushButton(">", self)
        self.ImgNext.move(800, 50)
        self.ImgNext.hide()
        self.ImgPrev = QtWidgets.QPushButton("<", self)
        self.ImgPrev.move(500, 50)
        self.ImgPrev.hide()

        self.sld1 = QSlider(Qt.Horizontal, self)
        self.sld1.setFocusPolicy(Qt.NoFocus)
        self.sld1.setGeometry(50, 150, 230, 30)
        self.sld1.valueChanged[int].connect(self.changeValueSelect)
        self.selectLabel =  QLabel(self)
        self.selectLabel.move(50,100)
        self.selectLabel.setText("-")
        self.sld1.hide()
        self.selectLabel.hide()

                #Crossover
        self.CNext = QtWidgets.QPushButton("К мутации", self)
        self.CNext.move(1350, 800)
        self.CNext.clicked.connect(self.chageLay)
        self.CNext.hide()

        self.parent1NextBtn = QtWidgets.QPushButton(">", self)
        self.parent1NextBtn.move(400, 20)
        self.parent1NextBtn.hide()
        self.parent1PrevBtn = QtWidgets.QPushButton("<", self)
        self.parent1PrevBtn.move(100, 20)
        self.parent1PrevBtn.hide()
        self.parent2NextBtn = QtWidgets.QPushButton(">", self)
        self.parent2NextBtn.move(900, 20)
        self.parent2NextBtn.hide()
        self.parent2PrevBtn = QtWidgets.QPushButton("<", self)
        self.parent2PrevBtn.move(600, 20)
        self.parent2PrevBtn.hide()

        self.crossway1 = QtWidgets.QPushButton("Crossover 1", self)
        self.crossway1.move(500, 120)
        self.crossway1.hide()


                #Mutation
        self.MNext = QtWidgets.QPushButton("Новый круг", self)
        self.MNext.move(1350, 800)
        self.MNext.clicked.connect(self.chageLay)
        self.MNext.hide()


    def hideGeneration(self):
        self.GNext.hide()
        self.PopSizeSetter.hide()
        self.CanvasSizeSetterX.hide()
        self.CanvasSizeSetterY.hide()
        self.YLabel.hide()
        self.XLabel.hide()
        self.circleLabel.hide()
        self.circleSetter.hide()
        self.rectLabel.hide()
        self.rectSetter.hide()
        self.lineLabel.hide()
        self.lineSetter.hide()
        self.GenerateBtn.hide()

    def showSelection(self):
        self.SNext.show()
        self.ImgNext.show()
        self.ImgPrev.show()
        self.GenerCanvas = [Canvas.Canvas(800,150, self.population, 1)]
        self.GenerCanvas[0].drawImage()
        self.ImgPrev.clicked.connect(self.callPrevPict(0))
        self.ImgNext.clicked.connect(self.callNextPict(0))
        self.sld1.show()
        self.selectLabel.show()

    def hideSelection(self):
        self.SNext.hide()
        self.sld1.hide()
        self.selectLabel.hide()
        self.ImgNext.hide()
        self.ImgPrev.hide()

    def showCrossover(self):
        self.CNext.show()
        self.GenerCanvas = [Canvas.Canvas(800,150, self.population, 1),Canvas.Canvas(800,150, self.population, 1)]
        self.parent1NextBtn.show()
        self.parent1PrevBtn.show()
        self.parent2NextBtn.show()
        self.parent2PrevBtn.show()
        self.parent1PrevBtn.clicked.connect(self.callPrevPict(0))
        self.parent1NextBtn.clicked.connect(self.callNextPict(0))
        self.parent2PrevBtn.clicked.connect(self.callPrevPict(1))
        self.parent2NextBtn.clicked.connect(self.callNextPict(1))
        self.crossway1.show()
        self.crossway1.clicked.connect(self.callCrossover)

    def hideCrossover(self):
        self.CNext.hide()
        self.parent1NextBtn.hide()
        self.parent1PrevBtn.hide()
        self.parent2NextBtn.hide()
        self.parent2PrevBtn.hide()
        self.crossway1.hide()

    def showMutation(self):
        self.MNext.show()

    def hideMutation(self):
        self.MNext.hide()



    def callCrossover(self):
        self.population.crossover(self.GenerCanvas[0].pictNum, self.GenerCanvas[1].pictNum)

    def changeValueSelect(self, value):
        self.selectLabel.setText("<div style ='color: #ff0000' >"+str(value)+"</div>")
        pictind = self.GenerCanvas[0].pictNum-1
        self.population.setFitToIndivid(value, pictind)

    def callNextPict(self, nm):
        def nextPicture():
            n = self.GenerCanvas[nm].incrPictNum()
            self.GenerCanvas[nm] = Canvas.Canvas(800, 150, self.population, n)
            self.sld1.setValue(self.population.individs[n-1].fit)
            self.GenerCanvas[nm].drawImage()
        return nextPicture

    def callPrevPict(self, nm):
        def prevPicture():
            n = self.GenerCanvas[nm].decrPictNum()
            self.GenerCanvas[nm] = Canvas.Canvas(800, 150, self.population, n)
            self.sld1.setValue(self.population.individs[n-1].fit)
            self.GenerCanvas[nm].drawImage()
        return prevPicture

    def generateEvent(self):
        if self.population.canvaSize[0] !=0 and  self.population.canvaSize[1] !=0:
            if self.population.size !=0:
                self.population.genetatePopulation()
                self.GenerCanvas = [Canvas.Canvas(800, 150, self.population, 1)]
                self.GenerCanvas[0].drawImage()
                self.GenerCanvas[0].move(800,100)
                #self.GenerCanvas[0].repaint()          подумать почему виджет не  работает
                #self.show()

    def chageLay(self):
        if self.layout < 3:
            self.layout += 1
        else: self.layout = 1
        self.setAnotherLay()

    def setAnotherLay(self):
        if self.layout == 0:
            pass
        elif self.layout == 1:
            self.hideGeneration()
            self.hideCrossover()
            self.hideMutation()
            self.showSelection()
        elif self.layout == 2:
            self.hideGeneration()
            self.hideSelection()
            self.hideMutation()
            self.showCrossover()
            self.population.prepareTOCrossover()
        elif self.layout == 3:
            self.hideGeneration()
            self.hideSelection()
            self.hideCrossover()
            self.showMutation()
        elif self.layout == 4:
            self.hideGeneration()
            self.hideSelection()
            self.hideCrossover()
            self.hideMutation()