from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QCoreApplication, Qt
from PIL.ImageQt import ImageQt
from PIL import Image
import sys

import Configcr
import Population
import Canvas

class Interface(QMainWindow):

    def __init__(self):
        super().__init__()
        self.layout = 0
        self.setGeometry(20,30,1500,800)
        self.population = Population.Population()
        self.GenerCanvas = [0,0]
        self.initUI()
        self.setAnotherLay()
        self.examleOfWork = []

        ###########################
        self.countGeneration = 0
        #self.originalImg = Image.open('3.jpg') #

        ###########################

    def initUI(self):
        self.setWindowTitle("Step 0: Generetion")
        self.mainwind = QtWidgets.QStackedWidget()
        self.maintab = QTabWidget()
        self.setCentralWidget(self.maintab)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(50,140,136))
        self.setPalette(p)
        self.mainFont = QtGui.QFont("Helvetica [Cronyx]", 16, QtGui.QFont.Bold)
        self.headFont = QtGui.QFont("Helvetica [Cronyx]", 28, QtGui.QFont.Bold)
        self.genLay = QWidget()
        self.selLay = QWidget()
        self.crosLay = QWidget()
        self.mutLay = QWidget()
        self.maintab.addTab(self.genLay, "Генерация")
        self.maintab.addTab(self.selLay, "Селекция")
        self.maintab.addTab(self.crosLay, "Кроссовер")
        self.maintab.addTab(self.mutLay, "Мутация")
        

                #Generation
        self.vboxg = QVBoxLayout()
        self.hboxg = QHBoxLayout()
        self.maintab.setGeometry(QtCore.QRect(-50, 0, 1500,800))

        self.GenNameLbl =  QLabel(self)
        self.GenNameLbl.setText("<div style='color: rgb(255, 255, 255); background-color: rgb(45,125,120); text-align: center; padding-top: 20px;'> Генерация первого поколения </div>")
        self.GenNameLbl.setFont(self.headFont)
        self.GenNameLbl.setGeometry(QtCore.QRect(0, 0, 1500, 120))
        self.GenNameLbl.setParent(self.genLay)
    
        self.GNext = QtWidgets.QPushButton("К отбору", self)
        self.GNext.setGeometry(QtCore.QRect(995, 660, 500, 100))
        self.GNext.setFont(self.headFont)
        self.GNext.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.GNext.clicked.connect(self.chageLay) 
        #self.GNext.clicked.connect(self.startPlay) 
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.GNext.setEnabled(False)
        self.GNext.setParent(self.genLay)

        self.GenerateBtn = QtWidgets.QPushButton("Генерировать", self)
        self.GenerateBtn.setFont(self.headFont)
        self.GenerateBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.GenerateBtn.setGeometry(QtCore.QRect(20, 660, 950, 100))
        self.GenerateBtn.clicked.connect(self.repaintImage)
        self.GenerateBtn.setParent(self.genLay)

        self.GentextLbl =  QLabel(self)
        self.GentextLbl.setText("<div style='color: rgb(255, 255, 255); '> Пример изображения: </div>")
        self.GentextLbl.setGeometry(QtCore.QRect(995, 95, 500, 150))
        self.GentextLbl.setWordWrap(True)
        self.GentextLbl.setFont(self.headFont)
        self.GentextLbl.setParent(self.genLay)

        self.XLabel =  QLabel(self)
        self.XLabel.setGeometry(QtCore.QRect(0, 120, 70, 50))
        self.XLabel.setText("<div style='color: rgb(255, 255, 255); text-align: right;'> X </div>")
        self.XLabel.setFont(self.mainFont)
        self.CanvasSizeSetterX = QtWidgets.QLineEdit(self)
        self.CanvasSizeSetterX.setGeometry(QtCore.QRect(90, 120, 400, 50))
        self.CanvasSizeSetterX.textChanged[str].connect(self.population.setcanvaSizeX)
        self.CanvasSizeSetterX.setFont(self.mainFont)
        self.YLabel =  QLabel(self)
        self.YLabel.setGeometry(QtCore.QRect(490, 120, 70, 50))
        self.YLabel.setText("<div style='color: rgb(255, 255, 255); text-align: right;'>Y</div>")
        self.YLabel.setFont(self.mainFont)
        self.CanvasSizeSetterY = QtWidgets.QLineEdit(self)
        self.CanvasSizeSetterY.setGeometry(QtCore.QRect(580, 120, 400, 50))
        self.CanvasSizeSetterY.textChanged[str].connect(self.population.setcanvaSizeY)
        self.CanvasSizeSetterY.setFont(self.mainFont)
        self.XLabel.setParent(self.genLay)
        self.CanvasSizeSetterX.setParent(self.genLay)
        self.YLabel.setParent(self.genLay)
        self.CanvasSizeSetterY.setParent(self.genLay)

        self.PopSizeLbl =  QLabel(self)
        self.PopSizeLbl.setText("<div style='color: rgb(255, 255, 255); text-align: right;'> Количество в первом поколении </div>")
        self.PopSizeLbl.setGeometry(QtCore.QRect(0, 175, 550, 50))
        self.PopSizeLbl.setFont(self.mainFont)
        self.PopSizeLbl.setParent(self.genLay)
        self.PopSizeSetter = QtWidgets.QLineEdit(self)
        self.PopSizeSetter.setGeometry(QtCore.QRect(580, 175, 400, 50))
        self.PopSizeSetter.textChanged[str].connect(self.population.setSize)
        self.PopSizeSetter.setFont(self.mainFont)
        self.PopSizeSetter.setParent(self.genLay)

        self.mutchanseLabel =  QLabel(self)
        self.mutchanseLabel.setGeometry(QtCore.QRect(0, 230, 550, 50))
        self.mutchanseLabel.setText("<div style='color: rgb(255, 255, 255); text-align: right;'>Шанс мутации (%)</div>")
        self.mutchanseLabel.setFont(self.mainFont)
        self.mutchanseLabel.setParent(self.genLay)
        self.mutChanceSetter = QtWidgets.QLineEdit(self)
        self.mutChanceSetter.setGeometry(QtCore.QRect(580, 230, 400, 50))
        self.mutChanceSetter.textChanged[str].connect(self.population.setMutationChance)
        self.mutChanceSetter.setFont(self.mainFont)
        self.mutChanceSetter.setParent(self.genLay)

        self.circleLabel =  QLabel(self)
        self.circleLabel.setGeometry(QtCore.QRect(0, 285, 550, 50))
        self.circleLabel.setText("<div style='color: rgb(255, 255, 255); text-align: right;'>Количество эллипсов</div>")
        self.circleLabel.setFont(self.mainFont)
        self.circleLabel.setParent(self.genLay)
        self.circleSetter = QtWidgets.QLineEdit(self)
        self.circleSetter.setGeometry(QtCore.QRect(580, 285, 400, 50))
        self.circleSetter.textChanged[str].connect(self.population.setCircleCount)
        self.circleSetter.setFont(self.mainFont)
        self.circleSetter.setParent(self.genLay)

        self.rectLabel =  QLabel(self)
        self.rectLabel.setGeometry(QtCore.QRect(0, 340, 550, 50))
        self.rectLabel.setText("<div style='color: rgb(255, 255, 255); text-align: right;'>Количество прямоугольников</div>")
        self.rectLabel.setFont(self.mainFont)
        self.rectLabel.setParent(self.genLay)
        self.rectSetter = QtWidgets.QLineEdit(self)
        self.rectSetter.setGeometry(QtCore.QRect(580, 340, 400, 50))
        self.rectSetter.textChanged[str].connect(self.population.setRectCount)
        self.rectSetter.setFont(self.mainFont)
        self.rectSetter.setParent(self.genLay)

        self.lineLabel =  QLabel(self)
        self.lineLabel.setGeometry(QtCore.QRect(0, 395, 550, 50))
        self.lineLabel.setText("<div style='color: rgb(255, 255, 255); text-align: right;'>Количество линий</div>")
        self.lineLabel.setFont(self.mainFont)
        self.lineLabel.setParent(self.genLay)
        self.lineSetter = QtWidgets.QLineEdit(self)
        self.lineSetter.setGeometry(QtCore.QRect(580, 395, 400, 50))
        self.lineSetter.textChanged[str].connect(self.population.setLineCount)
        self.lineSetter.setFont(self.mainFont)
        self.lineSetter.setParent(self.genLay)

        self.genInfoLabel =  QLabel(self)
        self.genInfoLabel.setGeometry(QtCore.QRect(10, 450, 950, 150))
        self.genInfoLabel.setText("<div style='color: rgb(255, 255, 255); text-align: center;'>Заполните все необходимые поля и нажмите 'генерировать' перед тем, как перейти к следующему этапу.</div>")
        self.genInfoLabel.setFont(self.mainFont)
        self.genInfoLabel.setWordWrap(True)
        self.genInfoLabel.setParent(self.genLay)

               
                #Selection
        self.vboxs = QVBoxLayout()
        self.hboxs = QHBoxLayout()
        self.SelNameLbl =  QLabel(self)
        self.SelNameLbl.setText("<div style='color: rgb(255, 255, 255); background-color: rgb(45,125,120); text-align: center; padding-top: 20px;'> Выбор лучших изображений </div>")
        self.SelNameLbl.setFont(self.headFont)
        self.SelNameLbl.setGeometry(QtCore.QRect(0, 0, 1500, 120))
        self.SelNameLbl.setParent(self.selLay)

        self.SNext = QtWidgets.QPushButton("К кроссоверу", self)
        self.SNext.setGeometry(QtCore.QRect(995, 660, 500, 100))
        self.SNext.setFont(self.headFont)
        self.SNext.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.SNext.clicked.connect(self.chageLay)
        self.SNext.setParent(self.selLay)

        self.Autogen = QtWidgets.QPushButton("Автогенерация", self)
        self.Autogen.setGeometry(QtCore.QRect(20, 660, 950, 100))
        self.Autogen.setFont(self.headFont)
        self.Autogen.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.Autogen.clicked.connect(self.endCycle)
        self.Autogen.setParent(self.selLay)

        self.selsaveInfo =  QLabel(self)
        self.selsaveInfo.setGeometry(QtCore.QRect(995, 120, 500, 120))
        self.selsaveInfo.setText("<div style='color: rgb(255, 255, 255); text-align: center;'>Если хотите сохранить изображение, введите название и нажимите 'сохранить'. </div>")
        self.selsaveInfo.setFont(self.mainFont)
        self.selsaveInfo.setWordWrap(True)
        self.selsaveInfo.setParent(self.selLay)

        self.SavePicbtn = QtWidgets.QPushButton("Сохранить изображение", self)
        self.SavePicbtn.setGeometry(QtCore.QRect(995, 320, 500, 100))
        self.SavePicbtn.setFont(self.mainFont)
        self.SavePicbtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.SavePicbtn.setParent(self.selLay)
        self.SavePicbtn.clicked.connect(self.savePicturefnc)

        self.setPictName = QtWidgets.QLineEdit(self)
        self.setPictName.setGeometry(QtCore.QRect(995, 255, 500, 60))
        self.setPictName.setFont(self.mainFont)
        self.setPictName.textChanged[str].connect(self.setSaveName)
        self.setPictName.setParent(self.selLay)

        self.selgradeInfo =  QLabel(self)
        self.selgradeInfo.setGeometry(QtCore.QRect(995, 470, 500, 150))
        self.selgradeInfo.setText("<div style='color: rgb(255, 255, 255); text-align: center;'> </div>")
        self.selgradeInfo.setFont(self.headFont)
        self.selgradeInfo.setWordWrap(True)
        self.selgradeInfo.setParent(self.selLay)

        self.selgradeInfo2 =  QLabel(self)
        self.selgradeInfo2.setGeometry(QtCore.QRect(995, 430, 500, 40))
        self.selgradeInfo2.setText("<div style='color: rgb(255, 255, 255); text-align: center;'> Выставьте следующие оценки: </div>")
        self.selgradeInfo2.setFont(self.mainFont)
        self.selgradeInfo2.setWordWrap(True)
        self.selgradeInfo2.setParent(self.selLay)

        self.warning1 =  QLabel(self)
        self.warning1.setGeometry(QtCore.QRect(0, 100, 990, 100))
        self.warning1.setText("<div style='color: rgb(255, 255, 255); text-align: center;'>Расставьте уникальное значение для каждого изображения, где 1 - наименее подходящее изображение, "+str(self.population.size) +" - наиболее подходящее.</div>")
        self.warning1.setFont(self.mainFont)
        self.warning1.setWordWrap(True)
        self.warning1.setParent(self.selLay)

        self.ImgNext = QtWidgets.QPushButton("►", self)
        self.ImgNext.setGeometry(QtCore.QRect(650, 210, 60, 60))
        self.ImgNext.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.ImgNext.setFont(self.mainFont)
        self.ImgNext.setParent(self.selLay)
        self.ImgPrev = QtWidgets.QPushButton("◄", self)
        self.ImgPrev.setGeometry(QtCore.QRect(200, 210, 60, 60))
        self.ImgPrev.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.ImgPrev.setFont(self.mainFont)
        self.ImgPrev.setParent(self.selLay)
        self.ImgPrev.clicked.connect(self.callPrevPict(0))
        self.ImgNext.clicked.connect(self.callNextPict(0))

        self.setPictRang = QtWidgets.QLineEdit(self)
        self.setPictRang.setGeometry(QtCore.QRect(270, 210, 370, 60))
        self.setPictRang.setFont(self.mainFont)
        self.setPictRang.textChanged[str].connect(self.callPictRangSetter)
        self.setPictRang.setParent(self.selLay)

        self.warning2 = QLabel(self)
        self.warning2.setGeometry(QtCore.QRect(0, 585, 990, 100))
        self.warning2.setText("<div style='color: rgb(255, 255, 255); text-align: center;'>Проверьте, чтобы все изображения были оценены.</div>")
        self.warning2.setFont(self.mainFont)
        self.warning2.setWordWrap(True)
        self.warning2.setParent(self.selLay)
        self.warning2.hide()


                #Crossover
        self.vboxc = [QVBoxLayout(),QVBoxLayout()]
        self.hboxc = QHBoxLayout()

        self.CrosNameLbl =  QLabel(self)
        self.CrosNameLbl.setText("<div style='color: rgb(255, 255, 255); background-color: rgb(45,125,120); text-align: center; padding-top: 20px;'> Выбор родителей и метода скрещивания </div>")
        self.CrosNameLbl.setFont(self.headFont)
        self.CrosNameLbl.setGeometry(QtCore.QRect(0, 0, 1500, 120))
        self.CrosNameLbl.setParent(self.crosLay)

        self.CNext = QtWidgets.QPushButton("К мутациям", self)
        self.CNext.setGeometry(QtCore.QRect(995, 660, 500, 100))
        self.CNext.setFont(self.headFont)
        self.CNext.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.CNext.setParent(self.crosLay)
        self.CNext.clicked.connect(self.chageLay)

        self.infolbl1 = QLabel(self)
        self.infolbl1.setGeometry(QtCore.QRect(160, 150, 200, 60))
        self.infolbl1.setText("<div style='color: rgb(255, 255, 255); text-align: center;'> Родитель 1</div>")
        self.infolbl1.setFont(self.mainFont)
        self.infolbl1.setWordWrap(True)
        self.infolbl1.setParent(self.crosLay)

        self.infolbl2 = QLabel(self)
        self.infolbl2.setGeometry(QtCore.QRect(670, 150, 200, 60))
        self.infolbl2.setText("<div style='color: rgb(255, 255, 255); text-align: center;'> Родитель 2</div>")
        self.infolbl2.setFont(self.mainFont)
        self.infolbl2.setWordWrap(True)
        self.infolbl2.setParent(self.crosLay)

        self.parent1NextBtn = QtWidgets.QPushButton("►", self)
        self.parent1NextBtn.setGeometry(QtCore.QRect(360, 150, 60, 60))
        self.parent1NextBtn.setParent(self.crosLay)
        self.parent1NextBtn.setFont(self.mainFont)
        self.parent1NextBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.parent1PrevBtn = QtWidgets.QPushButton("◄", self)
        self.parent1PrevBtn.setGeometry(QtCore.QRect(100, 150, 60, 60))
        self.parent1PrevBtn.setParent(self.crosLay)
        self.parent1PrevBtn.setFont(self.mainFont)
        self.parent1PrevBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.parent2NextBtn = QtWidgets.QPushButton("►", self)
        self.parent2NextBtn.setGeometry(QtCore.QRect(870, 150, 60, 60))
        self.parent2NextBtn.setParent(self.crosLay)
        self.parent2NextBtn.setFont(self.mainFont)
        self.parent2NextBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.parent2PrevBtn = QtWidgets.QPushButton("◄", self)
        self.parent2PrevBtn.setGeometry(QtCore.QRect(610, 150, 60, 60))
        self.parent2PrevBtn.setParent(self.crosLay)
        self.parent2PrevBtn.setFont(self.mainFont)
        self.parent2PrevBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.parent1PrevBtn.clicked.connect(self.callPrevPict(0))
        self.parent1NextBtn.clicked.connect(self.callNextPict(0))
        self.parent2PrevBtn.clicked.connect(self.callPrevPict(1))
        self.parent2NextBtn.clicked.connect(self.callNextPict(1))

        self.crossway1 = QtWidgets.QPushButton("Смешать порядок", self)
        self.crossway1.setGeometry(QtCore.QRect(995, 120, 500, 90))
        self.crossway1.setParent(self.crosLay)
        self.crossway1.setFont(self.mainFont)
        self.crossway1.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.crossway1.clicked.connect(self.callOrderMate)

        self.crossway2 = QtWidgets.QPushButton("Полное смешивание", self)
        self.crossway2.setGeometry(QtCore.QRect(995, 220, 500, 90))
        self.crossway2.setParent(self.crosLay)
        self.crossway2.setFont(self.mainFont)
        self.crossway2.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.crossway2.clicked.connect(self.callGenerate_1)


                #Mutation
        self.vboxm = QVBoxLayout()
        self.hboxm = QHBoxLayout()

        self.MutNameLbl =  QLabel(self)
        self.MutNameLbl.setText("<div style='color: rgb(255, 255, 255); background-color: rgb(45,125,120); text-align: center; padding-top: 20px;'> Выбор родителей и метода скрещивания </div>")
        self.MutNameLbl.setFont(self.headFont)
        self.MutNameLbl.setGeometry(QtCore.QRect(0, 0, 1500, 120))
        self.MutNameLbl.setParent(self.mutLay)

        self.MNext = QtWidgets.QPushButton("Далее", self) ####!!!!
        self.MNext.setParent(self.mutLay)
        self.MNext.setGeometry(QtCore.QRect(995, 660, 500, 100))
        self.MNext.setFont(self.headFont)
        self.MNext.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.MNext.clicked.connect(self.endCycle)

        self.nothingToMutateLbl = QLabel(self)
        self.nothingToMutateLbl.setGeometry(QtCore.QRect(352, 252, 295, 295))
        self.nothingToMutateLbl.setText("<div style='color: rgb(255, 255, 255); text-align: center;'>Вами не было сгенерировано ни одного изображения :(</div>")
        self.nothingToMutateLbl.setFont(self.mainFont)
        self.nothingToMutateLbl.setWordWrap(True)
        self.nothingToMutateLbl.setParent(self.mutLay)
        self.nothingToMutateLbl.hide()

        self.mutPictNextBtn = QtWidgets.QPushButton("►", self)
        self.mutPictNextBtn.setGeometry(QtCore.QRect(690, 350, 60, 80))
        self.mutPictNextBtn.setParent(self.mutLay)
        self.mutPictNextBtn.setFont(self.mainFont)
        self.mutPictNextBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.mutPictPrevBtn = QtWidgets.QPushButton("◄", self)
        self.mutPictPrevBtn.setGeometry(QtCore.QRect(250, 350, 60, 80))
        self.mutPictPrevBtn.setParent(self.mutLay)
        self.mutPictPrevBtn.setFont(self.mainFont)
        self.mutPictPrevBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.mutPictPrevBtn.clicked.connect(self.callPrevPict(0))
        self.mutPictNextBtn.clicked.connect(self.callNextPict(0))

        self.mchangegenBtn = QtWidgets.QPushButton("Мутировать ген", self)
        self.mchangegenBtn.setGeometry(QtCore.QRect(995, 120, 500, 90))
        self.mchangegenBtn.setParent(self.mutLay)
        self.mchangegenBtn.setFont(self.mainFont)
        self.mchangegenBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.mchangegenBtn.clicked.connect(self.callFloatmutprsd)

        self.mchangeOrderBtn = QtWidgets.QPushButton("Изменить порядок", self)
        self.mchangeOrderBtn.setGeometry(QtCore.QRect(995, 220, 500, 90))
        self.mchangeOrderBtn.setParent(self.mutLay)
        self.mchangeOrderBtn.setFont(self.mainFont)
        self.mchangeOrderBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.mchangeOrderBtn.clicked.connect(self.callChaneOrderprsd)

        self.mchangePlaceBtn = QtWidgets.QPushButton("Поменять местами\nдва гена", self)
        self.mchangePlaceBtn.setGeometry(QtCore.QRect(995, 320, 500, 90))
        self.mchangePlaceBtn.setParent(self.mutLay)
        self.mchangePlaceBtn.setFont(self.mainFont)
        self.mchangePlaceBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.mchangePlaceBtn.clicked.connect(self.callChangeplacesprsd)

        self.mdeepChangeBtn = QtWidgets.QPushButton("Глобальные изменения", self)
        self.mdeepChangeBtn.setGeometry(QtCore.QRect(995, 420, 500, 90))
        self.mdeepChangeBtn.setParent(self.mutLay)
        self.mdeepChangeBtn.setFont(self.mainFont)
        self.mdeepChangeBtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.mdeepChangeBtn.clicked.connect(self.callDeepmutationprsd)

        self.mcancelMutationbtn = QtWidgets.QPushButton("Отмена изменений", self)
        self.mcancelMutationbtn.setGeometry(QtCore.QRect(995, 550, 500, 90))
        self.mcancelMutationbtn.setParent(self.mutLay)
        self.mcancelMutationbtn.setFont(self.mainFont)
        self.mcancelMutationbtn.setStyleSheet("background-color: rgb(35,109,98); color: rgb(255, 255, 255); text-align: center;")
        self.mcancelMutationbtn.clicked.connect(self.canselMutation)


        self.maintab.setTabVisible(3, False)
        self.maintab.setTabVisible(2, False)
        self.maintab.setTabVisible(1, False)
        self.maintab.setTabVisible(0, True)

    def paintEvent(self, QPaintEvent):
        if not self.GenerCanvas:
            return
        painter = QtGui.QPainter(self)
        painter.setBrush(QColor(225, 225, 225))
        if self.layout == 0:
            if self.population.individs:
                self.GNext.setEnabled(True)
            self.maintab.setTabVisible(0, True)
            painter.drawRect(995, 250, 500, 400)
            if type(self.GenerCanvas[0]) is not int:
                painter.drawImage(QtCore.QRect
                                  (950+(550-self.population.canvaSize[0])//2,
                                   250+(400-self.population.canvaSize[1])//2, 
                                   self.population.canvaSize[0],self.population.canvaSize[1]),
                                  QImage(ImageQt(self.population.individs[self.GenerCanvas[0].pictNum-1].img)))
        elif self.layout == 1:
            self.maintab.setTabVisible(0, False)
            self.maintab.setTabVisible(3, False)
            self.maintab.setTabVisible(1, True)
            text = "<div style='color: rgb(255, 255, 255); text-align: center;'>"
            for i in self.population.gradeLeft:
                if i != 0:
                    text +=  str(i) + "\t"
            text += "</div>"
            self.selgradeInfo.setText(text)
            painter.drawImage(QtCore.QRect
                                (220+(500-self.population.canvaSize[0])//2,
                                280+(400-self.population.canvaSize[1])//2, 
                                self.population.canvaSize[0],self.population.canvaSize[1]),
                                QImage(ImageQt(self.population.individs[self.GenerCanvas[0].pictNum-1].img)))
        elif self.layout == 2:
            self.maintab.setTabVisible(1, False)
            self.maintab.setTabVisible(2, True)
            painter.drawImage(QtCore.QRect
                                (110+(300-self.population.canvaSize[0])//2,
                                250+(300-self.population.canvaSize[1])//2, 
                                self.population.canvaSize[0],self.population.canvaSize[1]),
                                QImage(ImageQt(self.population.individs[self.GenerCanvas[0].pictNum-1].img)))
            painter.drawImage(QtCore.QRect
                                (620+(300-self.population.canvaSize[0])//2,
                                250+(300-self.population.canvaSize[1])//2, 
                                self.population.canvaSize[0],self.population.canvaSize[1]),
                                QImage(ImageQt(self.population.individs[self.GenerCanvas[1].pictNum-1].img)))
        elif self.layout == 3:
            self.maintab.setTabVisible(2, False)
            self.maintab.setTabVisible(3, True)
            if self.GenerCanvas[0].population.individs:
                painter.drawImage(QtCore.QRect
                                    (330 +(300-self.population.canvaSize[0])//2,
                                    250+(300-self.population.canvaSize[1])//2, 
                                    self.population.canvaSize[0],self.population.canvaSize[1]),
                                    QImage(ImageQt(self.GenerCanvas[0].population.individs[self.GenerCanvas[0].pictNum-1].img)))
            else:
                self.nothingToMutateLbl.show()


    def showSelection(self):
        self.GenerCanvas = [Canvas.Canvas(self.population, 1)]
        self.warning1.setText("<div style='color: rgb(255, 255, 255); text-align: center;'>Расставьте уникальное значение для каждого изображения, где 1 - наименее подходящее изображение, "+str(self.population.size) +" - наиболее подходящее.</div>")
        self.hboxs.addWidget(self.GenerCanvas[0])
        self.GenerCanvas[0].drawImage()

    def hideSelection(self):
        self.hboxs.removeWidget(self.GenerCanvas[0])    

    def showCrossover(self):
        self.GenerCanvas = [Canvas.Canvas(self.population, 1), Canvas.Canvas(self.population, 1)]
        self.vboxc[0].addWidget(self.GenerCanvas[0])
        self.vboxc[1].addWidget(self.GenerCanvas[1])
        self.GenerCanvas[0].drawImage()
        self.GenerCanvas[1].drawImage()

    def hideCrossover(self):
        self.vboxc[0].removeWidget(self.GenerCanvas[0])
        self.vboxc[1].removeWidget(self.GenerCanvas[1])

    def showMutation(self):
        self.GenerCanvas = [Canvas.Canvas(self.population.subPopulation, 1)]
        self.vboxm.addWidget(self.GenerCanvas[0])
        self.GenerCanvas[0].drawImage()

    def hideMutation(self):
        self.hboxs.removeWidget(self.GenerCanvas[0])

    def endCycle(self):
        if self.layout == 1:
            for i in self.population.individs:
                if i.rang == 0:
                    self.warning2.show()
                    return
        self.layout = 3
        self.population.cont = True
        self.population.prepareTOCrossover()
        while self.population.cont:
            self.countGeneration += 1
            #self.population.prepareTOCrossover()
            self.population.autoGenerating()
            self.population.removeLoosers()
        self.warning2.hide()
        self.chageLay() #последним

    def callOrderMate(self):
        self.population.orderMate(self.GenerCanvas[0].pictNum, self.GenerCanvas[1].pictNum)

    def callGenerate_1(self):
        self.population.callgenarate_1(self.GenerCanvas[0].pictNum, self.GenerCanvas[1].pictNum)
    
    def callFloatmutprsd(self):
        self.GenerCanvas[0].population.callFloatmut(self.GenerCanvas[0].pictNum - 1)

    def callChangeplacesprsd(self):
        self.GenerCanvas[0].population.callFloatmut(self.GenerCanvas[0].pictNum - 1)

    def callChaneOrderprsd(self):
        self.GenerCanvas[0].population.callChaneOrder(self.GenerCanvas[0].pictNum - 1)

    def callDeepmutationprsd(self):
        self.GenerCanvas[0].population.callDeepmutation(self.GenerCanvas[0].pictNum - 1)

    def canselMutation(self):
        if self.GenerCanvas[0].origPict:
            self.GenerCanvas[0].population.individs[self.GenerCanvas[0].pictNum - 1] = self.GenerCanvas[0].origPict
            self.GenerCanvas[0].population.individs[self.GenerCanvas[0].pictNum - 1].generateImg()

    def drawPictINCurrLay(self, canvacount, n):
        if self.layout == 1 :
            self.vboxs.removeWidget(self.GenerCanvas[canvacount])
            self.GenerCanvas[canvacount] = Canvas.Canvas( self.population, n)
            self.hboxs.addWidget(self.GenerCanvas[canvacount])
            self.setPictRang.setText(str(self.GenerCanvas[0].population.individs[self.GenerCanvas[0].pictNum - 1].rang))
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
        if self.population.canvaSize[0] != 0 and self.population.canvaSize[1] != 0:
            if self.population.size !=0:
                self.population.genetatePopulation()
                if self.GenerCanvas[0] != 0:
                    self.vboxg.removeWidget(self.GenerCanvas[0])
                self.GenerCanvas = [Canvas.Canvas(self.population, 1)]
                self.hboxg.addWidget(self.GenerCanvas[0])
                self.show()

    def chageLay(self):
        if self.layout == 1:
            for i in self.population.individs:
                if i.rang == 0:
                    self.warning2.show()
                    return
        if self.layout < 3:
            self.layout += 1
        else: self.layout = 1
        self.setAnotherLay()

    def useConfig(self):
        fromconfigFile = Configcr.Config.read()
        self.population.setcanvaSizeX(fromconfigFile[0])
        self.population.setcanvaSizeY(fromconfigFile[1])
        self.population.setMutationChance(fromconfigFile[2])
        self.population.setSize(fromconfigFile[3])
        self.population.setCircleCount(fromconfigFile[4])
        self.population.setRectCount(fromconfigFile[5])
        self.population.setLineCount(fromconfigFile[6])

    def setAnotherLay(self):
        if self.layout == 0:
            self.useConfig()
        elif self.layout == 1:
            self.setWindowTitle("Step 1: Selection")
            self.population.prepareToSelect()
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

    #def startPlay(self):
    #    for i in range(2):
    #        self.countGeneration = 0
    #        if i == 0:
    #            isssim = False
    #        else:
    #            isssim = True
    #        self.useConfig()
    #        self.population.genetatePopulation()
    #        self.population.newgeneratedIndivids = self.population.individs
    #        #self.population.savePictureFake(str(self.countGeneration), isssim)
    #        while self.countGeneration <= 1000:
    #            self.population.removeWorseFake(self.originalImg, isssim)
    #            self.population.autoGeneratingFake()
    #            if self.countGeneration % 50 == 0:
    #                self.population.savePictureFake(str(self.countGeneration), isssim)
    #            self.countGeneration += 1