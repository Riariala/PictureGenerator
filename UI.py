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
        self.GenerCanvas = [0,0]
        self.initUI()
        self.setAnotherLay()
        self.examleOfWork = []

    def initUI(self):
        self.setWindowTitle("Step 0: Generetion")
        self.mainwind = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.mainwind)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(50,140,136))
        self.setPalette(p)
        self.mainFont = QtGui.QFont("Helvetica [Cronyx]", 18, QtGui.QFont.Bold)
        self.headFont = QtGui.QFont("Helvetica [Cronyx]", 25, QtGui.QFont.Bold)


                #Generation
        self.genLay = QWidget()
        self.mainwind.addWidget(self.genLay)
        self.vboxg = QVBoxLayout()
        self.hboxg = QHBoxLayout()
        self.vboxg.addLayout(self.hboxg)
        self.genLay.setLayout(self.vboxg)
        self.hboxg.insertSpacing(0, 900)
        self.vboxg.insertSpacing(0, 250)

        self.GenNameLbl =  QLabel(self)
        self.GenNameLbl.setText("<div style='color: rgb(255, 255, 255); background-color: rgb(45,125,120); text-align: center; padding-top: 20px;'> Генерация первого поколения </div>")
        self.GenNameLbl.setFont(self.headFont)
        self.GenNameLbl.setGeometry(QtCore.QRect(0, 0, 1500, 100))
    
        self.GNext = QtWidgets.QPushButton("К отбору", self)
        self.GNext.move(1350, 800)
        self.GNext.clicked.connect(self.chageLay) 
        #self.GNext.setParent(self.genLay)

        self.GenerateBtn = QtWidgets.QPushButton("Генерировать", self)
        self.GenerateBtn.move(100, 800)
        self.GenerateBtn.clicked.connect(self.repaintImage)

        self.XLabel =  QLabel(self)
        self.XLabel.setGeometry(QtCore.QRect(0, 100, 70, 50))
        self.XLabel.setText("<div style='color: rgb(255, 255, 255); text-align: right;'> X </div>")
        self.XLabel.setFont(self.mainFont)
        self.CanvasSizeSetterX = QtWidgets.QLineEdit(self)
        self.CanvasSizeSetterX.setGeometry(QtCore.QRect(90, 100, 400, 50))
        self.CanvasSizeSetterX.textChanged[str].connect(self.population.setcanvaSizeX)
        self.YLabel =  QLabel(self)
        self.YLabel.setGeometry(QtCore.QRect(490, 100, 70, 50))
        self.YLabel.setText("<div style='color: rgb(255, 255, 255); text-align: right;'>Y</div>")
        self.YLabel.setFont(self.mainFont)
        self.CanvasSizeSetterY = QtWidgets.QLineEdit(self)
        self.CanvasSizeSetterY.setGeometry(QtCore.QRect(580, 100, 400, 50))
        self.CanvasSizeSetterY.textChanged[str].connect(self.population.setcanvaSizeY)

        self.PopSizeLbl =  QLabel(self)
        self.PopSizeLbl.setText("<div style='color: rgb(255, 255, 255); text-align: right;'> Количество в первом поколении </div>")
        self.PopSizeLbl.setGeometry(QtCore.QRect(0, 155, 550, 50))
        self.PopSizeLbl.setFont(self.mainFont)
        #self.PopSizeLbl.adjustSize()
        self.PopSizeSetter = QtWidgets.QLineEdit(self)
        self.PopSizeSetter.setGeometry(QtCore.QRect(580, 155, 400, 50))
        self.PopSizeSetter.textChanged[str].connect(self.population.setSize)

        self.mutchanseLabel =  QLabel(self)
        self.mutchanseLabel.setGeometry(QtCore.QRect(0, 210, 550, 50))
        self.mutchanseLabel.setText("<div style='color: rgb(255, 255, 255); text-align: right;'>Шанс мутации (%)</div>")
        self.mutchanseLabel.setFont(self.mainFont)
        self.mutChanceSetter = QtWidgets.QLineEdit(self)
        self.mutChanceSetter.setGeometry(QtCore.QRect(580, 210, 400, 50))
        self.mutChanceSetter.textChanged[str].connect(self.population.setMutationChance)

        self.circleLabel =  QLabel(self)
        self.circleLabel.move(50,300)
        self.circleLabel.setText("circles")
        self.circleSetter = QtWidgets.QLineEdit(self)
        self.circleSetter.move(80, 300)
        self.circleSetter.textChanged[str].connect(self.population.setCircleCount)

        self.rectLabel =  QLabel(self)
        self.rectLabel.move(50,350)
        self.rectLabel.setText("rectangles")
        self.rectSetter = QtWidgets.QLineEdit(self)
        self.rectSetter.move(700, 370)
        self.rectSetter.textChanged[str].connect(self.population.setRectCount)

        self.lineLabel =  QLabel(self)
        self.lineLabel.move(50,410)
        self.lineLabel.setText("lines")
        self.lineSetter = QtWidgets.QLineEdit(self)
        self.lineSetter.move(700, 420)
        self.lineSetter.textChanged[str].connect(self.population.setLineCount)


        
        
                #Selection
        self.selLay = QWidget()
        self.mainwind.addWidget(self.selLay)
        self.vboxs = QVBoxLayout()
        self.hboxs = QHBoxLayout()
        self.vboxs.addLayout(self.hboxs)
        self.selLay.setLayout(self.vboxs)
        self.hboxs.insertSpacing(0, 500)
        self.vboxs.insertSpacing(0, 200)

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

        self.SavePicbtn = QtWidgets.QPushButton("Сохранить изображение", self)
        self.SavePicbtn.move(650, 150)
        self.SavePicbtn.hide()
        self.SavePicbtn.clicked.connect(self.savePicturefnc)
        self.setPictName = QtWidgets.QLineEdit(self)
        self.setPictName.move(650, 50)
        self.setPictName.textChanged[str].connect(self.setSaveName)
        self.setPictName.hide()

        
        self.ImgPrev.clicked.connect(self.callPrevPict(0))
        self.ImgNext.clicked.connect(self.callNextPict(0))

        self.setPictRang = QtWidgets.QLineEdit(self)
        self.setPictRang.move(650, 550)
        self.setPictRang.textChanged[str].connect(self.callPictRangSetter)
        self.setPictRang.hide()
        self.warning1 =  QLabel(self)
        self.warning1.setGeometry(QtCore.QRect(0, 600, 1000, 50))
        self.warning1.setText("<div style='color: rgb(255, 255, 255); text-align: center;'>Убедитесь, что расставили значения для всех изображений</div>")
        self.warning1.setFont(self.mainFont)
        self.warning1.hide()

        ####
        #self.selectdelinfo =  QLabel(self)
        #self.selectdelinfo.move(50,80)
        ##self.selectdelinfo.setText("<div style ='color: #ff0000' >Количество в первом поколении</div>")
        #self.selectdelinfo.setText("Данное изображение будет удалено")
        #self.selectdelinfo.adjustSize()
        #self.selectdelinfo.hide()

        #self.delornotPictureBtn = QtWidgets.QPushButton("Оставить", self)
        #self.delornotPictureBtn.move(50, 200)
        #self.delornotPictureBtn.clicked.connect(self.changedelstatus)
        #self.delornotPictureBtn.hide()
        ####

                #Crossover
        self.crosLay = QWidget()
        self.mainwind.addWidget(self.crosLay)
        self.mainboxc = QVBoxLayout()
        self.vboxc = [QVBoxLayout(),QVBoxLayout()]
        self.hboxc = QHBoxLayout()
        self.hboxc.addLayout(self.vboxc[0])
        self.hboxc.addLayout(self.vboxc[1])
        self.mainboxc.addLayout(self.hboxc)
        self.crosLay.setLayout(self.mainboxc)
        self.hboxc.insertSpacing(0, 150)
        self.vboxc[0].insertSpacing(0, 70)
        self.vboxc[1].insertSpacing(0, 70)

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
        self.parent1PrevBtn.clicked.connect(self.callPrevPict(0))
        self.parent1NextBtn.clicked.connect(self.callNextPict(0))
        self.parent2PrevBtn.clicked.connect(self.callPrevPict(1))
        self.parent2NextBtn.clicked.connect(self.callNextPict(1))

        self.crossway1 = QtWidgets.QPushButton("Перемешать гены через один", self)
        self.crossway1.move(500, 120)
        self.crossway1.hide()
        self.crossway1.clicked.connect(self.callCrossover_1)

        self.crossway2 = QtWidgets.QPushButton("Поменять цветами", self)
        self.crossway2.move(500, 170)
        self.crossway2.hide()
        self.crossway2.clicked.connect(self.callCrossover_2)

        self.crossway3 = QtWidgets.QPushButton("Двухточечное смешение", self)
        self.crossway3.move(500, 220)
        self.crossway3.hide()
        self.crossway3.clicked.connect(self.callCrossover_3)

        self.crossway4 = QtWidgets.QPushButton("50 на 50", self)
        self.crossway4.move(500, 270)
        self.crossway4.hide()
        self.crossway4.clicked.connect(self.callCrossover_4)


                #Mutation
        self.MNext = QtWidgets.QPushButton("Далее", self) ####!!!!
        self.MNext.move(1350, 800)
        self.MNext.clicked.connect(self.endCycle)
        self.MNext.hide()

        self.mutLay = QWidget()
        self.mainwind.addWidget(self.mutLay)
        self.vboxm = QVBoxLayout()
        self.hboxm = QHBoxLayout()
        self.vboxm.addLayout(self.hboxm)
        self.mutLay.setLayout(self.vboxm)
        self.hboxm.insertSpacing(0, 650)
        self.vboxm.insertSpacing(0, 200)


        self.mutPictNextBtn = QtWidgets.QPushButton(">", self)
        self.mutPictNextBtn.move(800, 20)
        self.mutPictNextBtn.hide()
        self.mutPictPrevBtn = QtWidgets.QPushButton("<", self)
        self.mutPictPrevBtn.move(700, 20)
        self.mutPictPrevBtn.hide()
        self.mutPictPrevBtn.clicked.connect(self.callPrevPict(0))
        self.mutPictNextBtn.clicked.connect(self.callNextPict(0))

        self.mchangeOrderBtn = QtWidgets.QPushButton("Сменить порядок", self)
        self.mchangeOrderBtn.move(200, 200)
        self.mchangeOrderBtn.hide()
        self.mchangeOrderBtn.clicked.connect(self.changeOrder)

        self.mchangeColorBtn = QtWidgets.QPushButton("Сменить цвет", self)
        self.mchangeColorBtn.move(200, 300)
        self.mchangeColorBtn.hide()
        self.mchangeColorBtn.clicked.connect(self.changeColor)

        self.mchangePosBtn = QtWidgets.QPushButton("Сменить положение", self)
        self.mchangePosBtn.move(200, 400)
        self.mchangePosBtn.hide()
        self.mchangePosBtn.clicked.connect(self.changePos)

        self.mcancelMutationbtn = QtWidgets.QPushButton("Отмена изменений", self)
        self.mcancelMutationbtn.move(200, 500)
        self.mcancelMutationbtn.hide()
        self.mcancelMutationbtn.clicked.connect(self.canselMutation)


        self.mainwind.setCurrentIndex(0)


    def hideGeneration(self):
        self.GenNameLbl.hide()
        self.PopSizeLbl.hide()
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
        self.mutChanceSetter.hide()
        self.mutchanseLabel.hide()

    def showSelection(self):
        self.mainwind.setCurrentIndex(1) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.SNext.show()
        self.ImgNext.show()
        self.ImgPrev.show()
        self.GenerCanvas = [Canvas.Canvas(self.population, 1)]
        self.hboxs.addWidget(self.GenerCanvas[0])
        self.GenerCanvas[0].drawImage()
        self.SavePicbtn.show()
        self.setPictName.show()
        #self.delornotPictureBtn.show()
        #self.selectdelinfo.show()
        self.setPictRang.show()
        self.warning1.show()

    def hideSelection(self):
        self.hboxs.removeWidget(self.GenerCanvas[0])
        self.warning1.hide()
        self.SNext.hide()
        self.setPictRang.hide()
        self.ImgNext.hide()
        self.ImgPrev.hide()
        self.SavePicbtn.hide()
        self.setPictName.hide()
        self.warning1.hide()
        self.population.size = len(self.population.individs) ##изменение количество в популяяции идет здесь. Оно будет необходимо позже? Ибо ничего не удаляется.....
        #self.delornotPictureBtn.hide()
        #self.selectdelinfo.hide()

    def showCrossover(self):
        self.mainwind.setCurrentIndex(2)
        self.CNext.show()
        self.GenerCanvas = [Canvas.Canvas(self.population, 1), Canvas.Canvas(self.population, 1)]
        self.vboxc[0].addWidget(self.GenerCanvas[0])
        self.vboxc[1].addWidget(self.GenerCanvas[1])
        self.GenerCanvas[0].drawImage()
        self.GenerCanvas[1].drawImage()
        self.parent1NextBtn.show()
        self.parent1PrevBtn.show()
        self.parent2NextBtn.show()
        self.parent2PrevBtn.show()
        self.crossway1.show()
        self.crossway2.show()
        self.crossway3.show()
        self.crossway4.show()

    def hideCrossover(self):
        self.vboxc[0].removeWidget(self.GenerCanvas[0])
        self.vboxc[1].removeWidget(self.GenerCanvas[1])
        self.CNext.hide()
        self.parent1NextBtn.hide()
        self.parent1PrevBtn.hide()
        self.parent2NextBtn.hide()
        self.parent2PrevBtn.hide()
        self.crossway1.hide()
        self.crossway2.hide()
        self.crossway3.hide()
        self.crossway4.hide()

    def showMutation(self):
        self.mainwind.setCurrentIndex(3)
        self.GenerCanvas = [Canvas.Canvas(self.population.subPopulation, 1)]
        self.vboxm.addWidget(self.GenerCanvas[0])
        self.GenerCanvas[0].drawImage()
        self.mutPictNextBtn.show()
        self.mutPictPrevBtn.show()
        self.mchangeOrderBtn.show()
        self.MNext.show()
        self.mcancelMutationbtn.show()
        self.mchangeColorBtn.show()
        self.mchangePosBtn.show()

    def hideMutation(self):
        self.hboxs.removeWidget(self.GenerCanvas[0])
        self.mutPictNextBtn.hide()
        self.mutPictPrevBtn.hide()
        self.MNext.hide()
        self.mcancelMutationbtn.hide()
        self.mchangeOrderBtn.hide()
        self.mchangeColorBtn.hide()
        self.mchangePosBtn.hide()

    def endCycle(self):
        self.layout = 3
        print(self.layout)
        self.population.autoGenerating()
        self.population.removeLoosers()
        self.chageLay() #последним

    def callCrossover_1(self):
        self.population.crossover_1(self.GenerCanvas[0].pictNum, self.GenerCanvas[1].pictNum)

    def callCrossover_2(self):
        self.population.crossover_2(self.GenerCanvas[0].pictNum, self.GenerCanvas[1].pictNum)

    def callCrossover_3(self):
        self.population.crossover_3(self.GenerCanvas[0].pictNum, self.GenerCanvas[1].pictNum)

    def callCrossover_4(self):
        self.population.crossover_4(self.GenerCanvas[0].pictNum, self.GenerCanvas[1].pictNum)

    def changeOrder(self):
        self.population.subPopulation.individs[self.GenerCanvas[0].pictNum - 1].changeOrderfunc()
        self.GenerCanvas[0].population = self.population.subPopulation
        self.GenerCanvas[0].changeImage()

    def changeColor(self):
        self.population.subPopulation.individs[self.GenerCanvas[0].pictNum - 1].changeColorfunc()
        self.GenerCanvas[0].population = self.population.subPopulation
        self.GenerCanvas[0].changeImage()

    def changePos(self):
        self.population.subPopulation.individs[self.GenerCanvas[0].pictNum - 1].changePosfunc()
        self.GenerCanvas[0].population = self.population.subPopulation
        self.GenerCanvas[0].changeImage()

    def canselMutation(self):
        print(self.GenerCanvas[0].population.individs[self.GenerCanvas[0].pictNum - 1].gen[0],self.GenerCanvas[0].origPict.gen[0] )
        if self.GenerCanvas[0].origPict:
            self.GenerCanvas[0].population.individs[self.GenerCanvas[0].pictNum - 1] = self.GenerCanvas[0].origPict
            self.GenerCanvas[0].changeImage()

    def changedelstatus(self):
        self.GenerCanvas[0].population.individs[self.GenerCanvas[0].pictNum - 1].delInd = not self.GenerCanvas[0].population.individs[self.GenerCanvas[0].pictNum - 1].delInd
        if self.GenerCanvas[0].population.individs[self.GenerCanvas[0].pictNum - 1].delInd:
            self.selectdelinfo.setText("Изображение будет оставлено!")
            self.delornotPictureBtn.setText("Удалить")
        else:
            self.selectdelinfo.setText("Данное изображение будет удалено!")
            self.delornotPictureBtn.setText("Оставить")
        self.selectdelinfo.adjustSize()

    def drawPictINCurrLay(self, canvacount, n):
        if self.layout == 1 :
            self.vboxs.removeWidget(self.GenerCanvas[canvacount])
            self.GenerCanvas[canvacount] = Canvas.Canvas( self.population, n)
            self.hboxs.addWidget(self.GenerCanvas[canvacount])
            self.setPictRang.setText(str(self.GenerCanvas[0].population.individs[self.GenerCanvas[0].pictNum - 1].rang))
            #if self.population.individs[n-1].delInd:
            #    self.selectdelinfo.setText("Изображение будет оставлено!")
            #    self.delornotPictureBtn.setText("Удалить")
            #else:
            #    self.selectdelinfo.setText("Данное изображение будет удалено!")
            #    self.delornotPictureBtn.setText("Оставить")
            #self.selectdelinfo.adjustSize()
        elif self.layout == 2 :
            self.vboxc[canvacount].removeWidget(self.GenerCanvas[canvacount])
            self.GenerCanvas[canvacount] = Canvas.Canvas( self.population, n)
            self.vboxc[canvacount].addWidget(self.GenerCanvas[canvacount])
        elif self.layout == 3 :
            self.vboxm.removeWidget(self.GenerCanvas[canvacount])
            self.GenerCanvas[canvacount] = Canvas.Canvas( self.population.subPopulation, n)
            self.hboxm.addWidget(self.GenerCanvas[canvacount])
        self.GenerCanvas[canvacount].drawImage()

    def callNextPict(self, canvacount): 
        def nextPicture(): 
            n = self.GenerCanvas[canvacount].incrPictNum()
            self.drawPictINCurrLay(canvacount, n)
        return nextPicture

    def callPrevPict(self, canvacount):
        def prevPicture():
            n = self.GenerCanvas[canvacount].decrPictNum()
            self.drawPictINCurrLay(canvacount, n)
        return prevPicture

    def setSaveName(self,text):
        self.population.individs[self.GenerCanvas[0].pictNum-1].setName(text)

    def callPictRangSetter(self, text):
        self.population.setRang(text,self.GenerCanvas[0].pictNum-1)

    def savePicturefnc(self):
        self.GenerCanvas[0].savePicture()

    def repaintImage(self):
        if self.population.canvaSize[0] !=0 and  self.population.canvaSize[1] !=0:
            if self.population.size !=0:
                self.population.genetatePopulation()
                if self.GenerCanvas[0] != 0:
                    self.vboxg.removeWidget(self.GenerCanvas[0])
                self.GenerCanvas = [Canvas.Canvas(self.population, 1)]
                self.GenerCanvas[0].move(800,100)
                self.hboxg.addWidget(self.GenerCanvas[0])
                self.GenerCanvas[0].drawImage()
                self.show()

    def chageLay(self):
        if self.layout < 3:
            self.layout += 1
        else: self.layout = 1
        self.setAnotherLay()

    def setAnotherLay(self):
        if self.layout == 0:
            pass
        elif self.layout == 1:
            self.setWindowTitle("Step 1: Selection")
            self.population.prepareToSelect()
            self.hideGeneration()
            self.hideMutation()
            self.showSelection()
        elif self.layout == 2:
            self.setWindowTitle("Step 2: Crossover")
            self.hideSelection()
            self.showCrossover()
            self.population.prepareTOCrossover()
        elif self.layout == 3:
            self.setWindowTitle("Step 3: Mutation")
            self.hideCrossover()
            self.showMutation()