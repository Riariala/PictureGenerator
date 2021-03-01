import sys
import random
from tkinter import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QCoreApplication, Qt
import random


class Individ():
     
    def __init__(self):
        self.genom = []
        self.fit = 0
        self.attraction = 0
        self.seed = 10
        self.generetCount = 1
        self.oldGen = None

    def changeAttraction(val):
       self.attraction = val

    def createNewGenom(self):
        self.genom.append([]) #точки
        #random.seed(self.seed, version=2)
        for i in range(35):
            x = random.randint(26,1024)
            y = random.randint(1,699)
            colorR = random.randint(0,255)
            colorG = random.randint(0,255)
            colorB = random.randint(0,255)
            transp = random.randint(0,255)
            self.genom[0].append([x,y, colorR, colorG, colorB, transp])
        self.genom.append([]) #линии <Объект> = QLine(<X1>, <Y1>, <X2>, <Y2>)
        for i in range(5):
            x1 = random.randint(-170,1025)
            x2 = random.randint(25,1025)
            y1 = random.randint(-100,700)
            y2 = random.randint(0,700)
            colorR = random.randint(0,255)
            colorG = random.randint(0,255)
            colorB = random.randint(0,255)
            transp = random.randint(0,255)
            self.genom[1].append([x1,y1,x2,y2, colorR, colorG, colorB, transp])
        self.genom.append([]) #круги drawEllipse(<X>, <Y>, <Ширина>, <Высота>)
        for i in range(45):
            x = random.randint(-170,500)
            y = random.randint(-100,350)
            width = random.randint(1,1025)
            height = random.randint(1,700)
            colorR = random.randint(0,255)
            colorG = random.randint(0,255)
            colorB = random.randint(0,255)  
            colorInsR = random.randint(0,255)
            colorInsG = random.randint(0,255)
            colorInsB = random.randint(0,255)
            transp = random.randint(0,255)
            self.genom[2].append([x,y,width,height, colorR, colorG, colorB, colorInsR, colorInsG, colorInsB, transp])
        self.genom.append([]) #арки drawArc(<X>, <Y>, <Ширина>, <Высота>, <Начальный угол>, <Угол>)
        for i in range(0):
            x = random.randint(-170,1025)
            y = random.randint(-100,700)
            width = random.randint(1,1025)
            height = random.randint(1,700)
            stArc = random.randint(0,360) 
            endArc = random.randint(0,360) 
            colorR = random.randint(0,255)
            colorG = random.randint(0,255)
            colorB = random.randint(0,255)
            transp = random.randint(0,255)
            self.genom[3].append([x,y,width,height,stArc, endArc, colorR, colorG, colorB, transp])
        self.genom.append([]) #квадраты
        for i in range(5):
            x = random.randint(-170,1024)
            y = random.randint(-100,699)
            width = random.randint(1,1025)
            height = random.randint(1,720)
            colorR = random.randint(0,255)
            colorG = random.randint(0,255)
            colorB = random.randint(0,255)  
            colorInsR = random.randint(0,255)
            colorInsG = random.randint(0,255)
            colorInsB = random.randint(0,255)
            transp = random.randint(0,255)
            self.genom[4].append([x,y,width,height, colorR, colorG, colorB, colorInsR, colorInsG, colorInsB, transp])
        self.genom.append([]) #полигоны
        self.genom.append([]) #текст

    def partition(self, low, high):  
        pivot = self.oldGen[(low + high) // 2].fit
        i = low - 1
        j = high + 1
        while True:
            i += 1
            while self.oldGen[i].fit < pivot:
                i += 1
            j -= 1
            while self.oldGen[j].fit > pivot:
                j -= 1
            if i >= j:
                return j
            self.oldGen[i], self.oldGen[j] = self.oldGen[j], self.oldGen[i]

    def sortBest(self):
        def _quick_sort(low, high):
            if low < high:
                split_index = self.partition(low, high)
                _quick_sort(low, split_index)
                _quick_sort(split_index + 1, high)
        _quick_sort(0, len(self.oldGen) - 1)


    def newGeneration(self, oldGen):
        self.oldGen = oldGen
        self.sortBest()
        for i in range(20):
            print(self.oldGen[i].fit)
        self.generetCount = self.oldGen[0].generetCount + 1


class Interface(QWidget):
    
    def __init__(self):
        super().__init__()
        self.pictNum = 0
        self.menuSlot = 0
        self.oldPopulation = []
        self.population = []
        self.populationIdentify()
        self.initUI()

    def populationIdentify(self):
        self.population = []
        for i in range(20):
            self.population.append(Individ())
            self.population[i].createNewGenom()

    def initUI(self):
        self.setGeometry(50, 50, 1350, 700)
        self.setWindowTitle('Генерация изображений')
        self.qp = QPainter()
        #self.setWindowIcon(QIcon('web.png')) - иконка приложения
        exitB = QPushButton('X', self)
        exitB.resize(25, 25)
        exitB.move(1310, 15)
        exitB.clicked.connect(QCoreApplication.instance().quit)
        prevPicB = QPushButton('<', self)
        prevPicB.resize(25, 700)
        prevPicB.move(0, 0)
        nextPicB = QPushButton('>', self)
        nextPicB.resize(25, 700)
        nextPicB.move(1025, 0)
        nextPicB.clicked.connect(self.nextPressed)
        prevPicB.clicked.connect(self.prevPressed)
        self.eval = QLabel("<div style ='color: #ff0000; fontsize: 2400px' >152</div>")
        self.eval.move(1070, 50)
        if (self.menuSlot ==0):
            self.firstMenu()
        elif (self.menuSlot ==1):
            self.secondMenu()
        self.secondMenu()
        
        self.show()

    def paintEvent(self, event):
        
        self.qp.begin(self)

        self.clearCanvas()
        if (self.menuSlot==1):
            self.drawPicture()
        self.drawBcground()

        self.qp.end()
        self.initUI()

    def drawBcground(self):
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        self.qp.setPen(col)

        self.qp.setBrush(QColor(150, 150, 170))
        self.qp.drawRect(0, 0, 25, 700)

        self.qp.setBrush(QColor(150, 150, 170))
        self.qp.drawRect(1025, 0, 25, 700)

        self.qp.setBrush(QColor(220, 220, 250))
        self.qp.drawRect(1050, 0, 300, 700)

    def drawPicture(self):
        shapeind = 0
        countElem = len(self.population[self.pictNum].genom[shapeind]) #точкам
        for j in range(countElem):
            self.qp.setPen(QColor(self.population[self.pictNum].genom[shapeind][j][2], self.population[self.pictNum].genom[shapeind][j][3], self.population[self.pictNum].genom[shapeind][j][4], self.population[self.pictNum].genom[shapeind][j][5]))
            self.qp.drawPoint(self.population[self.pictNum].genom[shapeind][j][0], self.population[self.pictNum].genom[shapeind][j][1])
        shapeind = 1
        countElem = len(self.population[self.pictNum].genom[shapeind]) #линиям
        for j in range(countElem):
            self.qp.setPen(QColor(self.population[self.pictNum].genom[shapeind][j][4], self.population[self.pictNum].genom[shapeind][j][5], self.population[self.pictNum].genom[shapeind][j][6], self.population[self.pictNum].genom[shapeind][j][7]))
            self.qp.drawLine(self.population[self.pictNum].genom[shapeind][j][0], self.population[self.pictNum].genom[shapeind][j][1], self.population[self.pictNum].genom[shapeind][j][2],self.population[self.pictNum].genom[shapeind][j][3]) 
        shapeind = 2
        countElem = len(self.population[self.pictNum].genom[shapeind]) #круг
        for j in range(countElem):
            self.qp.setBrush(QColor(self.population[self.pictNum].genom[shapeind][j][7], self.population[self.pictNum].genom[shapeind][j][8], self.population[self.pictNum].genom[shapeind][j][9], self.population[self.pictNum].genom[shapeind][j][10]))
            self.qp.setPen(QColor(self.population[self.pictNum].genom[shapeind][j][4], self.population[self.pictNum].genom[shapeind][j][5], self.population[self.pictNum].genom[shapeind][j][6], self.population[self.pictNum].genom[shapeind][j][10]))
            self.qp.drawEllipse(self.population[self.pictNum].genom[shapeind][j][0], self.population[self.pictNum].genom[shapeind][j][1], self.population[self.pictNum].genom[shapeind][j][2],self.population[self.pictNum].genom[shapeind][j][3])
        shapeind = 3
        countElem = len(self.population[self.pictNum].genom[shapeind]) #дуга
        for j in range(countElem):
            self.qp.setPen(QColor(self.population[self.pictNum].genom[shapeind][j][6], self.population[self.pictNum].genom[shapeind][j][7], self.population[self.pictNum].genom[shapeind][j][8], self.population[self.pictNum].genom[shapeind][j][9]))
            self.qp.drawArc(self.population[self.pictNum].genom[shapeind][j][0], self.population[self.pictNum].genom[shapeind][j][1], self.population[self.pictNum].genom[shapeind][j][2],self.population[self.pictNum].genom[shapeind][j][3], self.population[self.pictNum].genom[shapeind][j][4], self.population[self.pictNum].genom[shapeind][j][5])
        shapeind = 4
        countElem = len(self.population[self.pictNum].genom[shapeind]) #квадрат
        for j in range(countElem):
            self.qp.setBrush(QColor(self.population[self.pictNum].genom[shapeind][j][7], self.population[self.pictNum].genom[shapeind][j][8], self.population[self.pictNum].genom[shapeind][j][9], self.population[self.pictNum].genom[shapeind][j][10]))
            self.qp.setPen(QColor(self.population[self.pictNum].genom[shapeind][j][4], self.population[self.pictNum].genom[shapeind][j][5], self.population[self.pictNum].genom[shapeind][j][6], self.population[self.pictNum].genom[shapeind][j][10]))
            self.qp.drawRect(self.population[self.pictNum].genom[shapeind][j][0], self.population[self.pictNum].genom[shapeind][j][1], self.population[self.pictNum].genom[shapeind][j][2],self.population[self.pictNum].genom[shapeind][j][3])


    def clearCanvas(self):
        self.qp.setBrush(QColor(255, 255, 255))
        self.qp.drawRect(25, 0, 1000, 700)

    def firstMenu(self):
        readyB = QPushButton('Генерировать', self)
        readyB.resize(200, 50)
        readyB.move(1100, 520)
        readyB.clicked.connect(self.genPressed)

    def secondMenu(self):
        readyB = QPushButton('Готово', self)
        readyB.resize(200, 50)
        readyB.move(1100, 610)
        readyB.clicked.connect(self.readyPressed)
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(1070, 150, 230, 30)
        sld.valueChanged[int].connect(self.changeValue)
        

    def changeValue(self, value):
        self.eval.setText("<div style ='color: #ff0000' >"+str(value)+"</div>")
        self.population[self.pictNum].fit = value

    def nextPressed(self):
        if (self.pictNum < 19): #здесь кол-во картинок
            self.pictNum +=1
        else: 
            self.pictNum = 1
        self.update()

    def prevPressed(self):
        if (self.pictNum > 0): #здесь кол-во картинок
            self.pictNum -= 1
        else: 
            self.pictNum = 19
        self.update()

    def readyPressed(self):
        if self.menuSlot < 1:
            self.menuSlot += 1
        else:
            self.menuSlot = 0
        self.update()

    def genPressed(self):
        self.menuSlot = 0
        self.oldPopulation = self.population
        self.population = []
        for i in range(20):
            self.population.append(Individ())
            self.population[i].newGeneration(self.oldPopulation)

        for i in self.population:
            print(i.fit)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    interface = Interface()
    sys.exit(app.exec_())
