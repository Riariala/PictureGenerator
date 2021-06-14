from PIL import Image, ImageDraw
import Genom
import CircleGen
import LineGen
import RectGen
from random import randint, uniform, normalvariate
from deap.tools import cxSimulatedBinaryBounded, mutPolynomialBounded
from itertools import chain
import copy
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt

class Individ(object):
    
    def __init__(self, x, y):
        self.rang = 0
        self.sizeX = x
        self.sizeY = y
        self.gen = []
        self.name = ''
        self.survival = 1
        self.fit = 1
        self.lookslike = False

    def generateImg(self):
        self.img = Image.new("RGB",  (self.sizeX,self.sizeY), "white")
        self.imgDrawn = ImageDraw.Draw(self.img)
        if self.gen:
            self.imgDrawn = self.paintIndivid(self.imgDrawn)

    def generateIndivid(self, figures):
        self.gen = []
        figersum = sum(figures)
        genrange = []
        for i in range(figures[0]):
            genrange.append(1)
        for i in range(figures[1]):
            genrange.append(2)
        for i in range(figures[2]):
            genrange.append(3)
        for i in range(figersum): #перемешиваем для смены порядка прорисовки
            rand = randint(0, figersum-1)
            c = genrange[i]
            genrange[i] = genrange[rand]
            genrange[rand] = c
        self.gen.append(genrange)
        self.gen.append([])
        for i in range(figures[0]):
            for g in range(10):                     #sX,sY,eX,eY,bR,bG,bB,pR,pG,pB
                self.gen[1].append(uniform(0,1))
        for i in range(figures[1]):
            for g in range(10):                     #sX,sY,eX,eY,bR,bG,bB,pR,pG,pB
                self.gen[1].append(uniform(0,1))
        for i in range(figures[2]):
            for g in range(8):                      #sX,sY,eX,eY,pR,pG,pB, width
                self.gen[1].append(uniform(0,1))
        self.generateImg()

    def copyIndivid(self):
        newIndivid = Individ(self.sizeX,self.sizeY)
        newIndivid.gen = copy.deepcopy(self.gen)
        return newIndivid

    def setName(self,text):
        if len(text) <= 25:
            self.name = text
        else:
            self.name = text[:25]

    def paintIndivid(self, drawImg):
        draws = drawImg
        pointer = 0
        for i in self.gen[0]:
            msv = []
            if i == 1:
                for k in range(10):
                    msv.append(self.gen[1][pointer+k])
                draws = CircleGen.CircleGen().paintFigure(drawImg, msv, self.sizeX, self.sizeY)
                pointer += 10
            if i == 2:
                for k in range(10):
                    msv.append(self.gen[1][pointer+k])
                draws = RectGen.RectGen().paintFigure(drawImg, msv, self.sizeX, self.sizeY)
                pointer += 10
            if i == 3:
                for k in range(8):
                    msv.append(self.gen[1][pointer+k])
                draws = LineGen.LineGen().paintFigure(drawImg, msv, self.sizeX, self.sizeY)
                pointer += 8
            drawImg = draws
        return drawImg

    def mateTypeOrder(self, parent1, parent2, countFigure):
        lenthgen = len(parent1.gen[0])
        order = [0 for i in range(lenthgen)]
        for i in range(lenthgen):
            if parent1.gen[0][i] == parent2.gen[0][i]:
                order[i] = parent1.gen[0][i]
        leftmass = []
        for i in range(3):
            leftmass.append(countFigure[i] - order.count(i+1))
        for i in range(lenthgen):
            if order[i] == 0:
                wchone = randint(1,2)
                if wchone == 1:
                    if leftmass[parent1.gen[0][i]-1] != 0:
                        order[i] = parent1.gen[0][i]
                        leftmass[parent1.gen[0][i]-1] -= 1
                    elif leftmass[parent2.gen[0][i]-1] != 0:
                        order[i] = parent2.gen[0][i]
                        leftmass[parent2.gen[0][i]-1] -= 1
                elif wchone == 2:
                    if leftmass[parent2.gen[0][i]-1] != 0:
                        order[i] = parent2.gen[0][i]
                        leftmass[parent2.gen[0][i]-1] -= 1
                    elif leftmass[parent1.gen[0][i]-1] != 0:
                        order[i] = parent1.gen[0][i]
                        leftmass[parent1.gen[0][i]-1] -= 1
                if order[i] == 0:
                    for j in range(len(leftmass)):
                        if leftmass[j] != 0:
                            order[i] = j + 1 
                            leftmass[j] -= 1
        return order

    def orderMate(self, parent1, parent2, countFigure):
        self.gen.append(self.mateTypeOrder(parent1, parent2, countFigure))
        self.gen.append(parent1.gen[1]) 
        self.generateImg()

    def genarate_1(self, parent1, parent2,countFigure):
        self.gen.append(self.mateTypeOrder(parent1, parent2, countFigure))
        newones = cxSimulatedBinaryBounded(parent1.gen[1], parent2.gen[1], uniform(15,20), 0, 1)
        self.gen.append(newones[randint(0,1)])
        self.generateImg()

    def floatmut(self):
        randomgen = randint(0, len(self.gen[1])-1)
        self.gen[1][randomgen] = abs(normalvariate(self.gen[1][randomgen], uniform(0.000005, 0.25)))
        if self.gen[1][randomgen] > 1:
            self.gen[1][randomgen] = 2 - self.gen[1][randomgen]
        self.generateImg()

    def changeplaces(self):
        randomgen1 = randint(0, len(self.gen[1])-1)
        randomgen2 = randint(0, len(self.gen[1])-1)
        b = self.gen[1][randomgen1]
        self.gen[1][randomgen1] = self.gen[1][randomgen2]
        self.gen[1][randomgen2] = b
        self.generateImg()

    def chaneOrder(self):
        randomgen1 = randint(0, len(self.gen[0])-1)
        randomgen2 = randint(0, len(self.gen[0])-1)
        b = self.gen[0][randomgen1]
        self.gen[0][randomgen1] = self.gen[0][randomgen2]
        self.gen[0][randomgen2] = b
        self.generateImg()

    def deepmutation(self):
        self.chaneOrder()
        returned = mutPolynomialBounded(self.gen[1], 20, 0, 1, 0.5)
        self.gen[1] = returned[0]