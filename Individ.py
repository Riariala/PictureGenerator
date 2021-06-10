from PIL import Image, ImageDraw
import Genom
import CircleGen
import LineGen
import RectGen
from random import randint, uniform
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
        self.fit = 0
        self.name = ''
        self.delInd = False
        self.metrixval = 0

    def generateImg(self):
        self.img = Image.new("RGB",  (self.sizeX,self.sizeY), 'white')
        self.imgDrawn = ImageDraw.Draw(self.img)
        if self.gen:
            self.imgDrawn = self.paintIndivid(self.imgDrawn)

    def generateCoord(self):
        x1 = randint(0,self.sizeX)
        x2 = randint(0,self.sizeX)
        if x1>x2:
            stx = x2 
            enx = x1
        else:
            stx = x1 
            enx = x2
        y1 = randint(0,self.sizeY)
        y2 = randint(0,self.sizeY)
        if y1>y2:
            sty = y2 
            eny = y1
        else:
            sty = y1 
            eny = y2
        return [stx,sty,enx,eny]

    def generateIndivid(self, figures):
        self.gen = []
        figersum = sum(figures)
        self.gen.append([i for i in range(1, figersum+1)])
        count = 0
        for i in range(len(figures)):
            for j in range(figures[i]):
                if i == 0:
                    self.gen.append(CircleGen.CircleGen())
                elif i == 1:
                    self.gen.append(RectGen.RectGen())
                elif i == 2:
                    self.gen.append(LineGen.LineGen())
                coord = self.generateCoord()
                lent = len(self.gen) - 1
                if lent >= 0:
                    self.gen[lent].generateGenom(coord[0],coord[1],coord[2],coord[3])
        for i in range(figersum): #перемешиваем для смены порядка прорисовки
            rand = randint(0, figersum-1)
            c = self.gen[0][i]
            self.gen[0][i] = self.gen[0][rand]
            self.gen[0][rand] = c
        self.generateImg()

    def copyIndivid(self):
        newIndivid = Individ(self.sizeX,self.sizeY)
        newIndivid.gen = copy.deepcopy(self.gen)
        return newIndivid

    def orderlyCrossing(self, par1, par2):
        leng = len(par1.gen[0])
        self.gen.append([0 for i in range(leng)])
        lenpart = leng//2
        firstHalf = randint(0, (leng-lenpart))
        for i in range(firstHalf, firstHalf+lenpart):
            self.gen[0][i] = par2.gen[0][i]
        for i in chain(range(firstHalf), range(firstHalf+lenpart, leng)):
            if par1.gen[0][i] in self.gen[0]: 
                self.gen[0][i] = par2.gen[0][i]
            else: 
                self.gen[0][i] = par1.gen[0][i]

    def generateByCrossover_shareblend(self, parent1, parent2):
        self.orderlyCrossing(parent1, parent2)
        genlen = len(parent2.gen)
        for i in range(1, genlen):
            randomgen = randint(1, (genlen-1))
            self.gen.append(parent1.gen[i].returnNewGen_blend(parent2.gen[randomgen]))
            if self.gen[i].startPoints[0] > self.sizeX:
                self.gen[i].startPoints[0] = abs(2* self.sizeX - self.gen[i].startPoints[0])
            if self.gen[i].startPoints[1] > self.sizeY:
                self.gen[i].startPoints[1] = abs(2* self.sizeY - self.gen[i].startPoints[1])
            if self.gen[i].endPoints[0] > self.sizeX:
                self.gen[i].endPoints[0] = abs(2 * self.sizeX - self.gen[i].endPoints[0])
            if self.gen[i].endPoints[1] > self.sizeY:
                self.gen[i].endPoints[1] = abs(2 * self.sizeY - self.gen[i].endPoints[1])

            if self.gen[i].startPoints[0] > self.gen[i].endPoints[0]:
                b = self.gen[i].startPoints[0]
                self.gen[i].startPoints[0] =  self.gen[i].endPoints[0]
                self.gen[i].endPoints[0] = b
            if self.gen[i].startPoints[1] > self.gen[i].endPoints[1]:
                b = self.gen[i].startPoints[1]
                self.gen[i].startPoints[1] =  self.gen[i].endPoints[1]
                self.gen[i].endPoints[1] = b
        self.generateImg()

    def generateByCrossover_sharerand(self, parent1, parent2):
        self.orderlyCrossing(parent1, parent2)
        genlen = len(parent1.gen)
        for i in range(1, genlen):
            randomgen = randint(1, genlen-1)
            self.gen.append(parent1.gen[i].returnNewGen_sharerand(parent2.gen[i], parent2.gen[randomgen]))
            if self.gen[i].startPoints[0] > self.gen[i].endPoints[0]:
                b = self.gen[i].startPoints[0]
                self.gen[i].startPoints[0] =  self.gen[i].endPoints[0]
                self.gen[i].endPoints[0] = b
            if self.gen[i].startPoints[1] > self.gen[i].endPoints[1]:
                b = self.gen[i].startPoints[1]
                self.gen[i].startPoints[1] =  self.gen[i].endPoints[1]
                self.gen[i].endPoints[1] = b
        self.generateImg()

    def generateByCrossover_share(self, parent1, parent2):
        self.orderlyCrossing(parent1, parent2)
        genlen = len(parent1.gen)
        for i in range(1, genlen):
            self.gen.append(parent1.gen[i].returnNewGen_1(parent2.gen[i]))
            randomgen = randint(1, genlen-1)
            randomel = randint(1, 10)
            coef = uniform(0.5, 1.5)
            self.gen[i].startPoints[0] = parent2.gen[randomgen].startPoints[1]
            if randomel==1:
                if type(parent2.gen[randomgen].startPoints[0]) is int:
                    self.gen[i].startPoints[0] = parent2.gen[randomgen].startPoints[1]
            elif randomel==2:
                if type(parent2.gen[randomgen].startPoints[1]) is int:
                    self.gen[i].startPoints[1] = parent2.gen[randomgen].startPoints[0]
            elif randomel==3:
                self.gen[i].endPoints[0] = parent2.gen[randomgen].endPoints[1]
            elif randomel==4:
                self.gen[i].endPoints[1] = parent2.gen[randomgen].endPoints[0]
            elif randomel==5:
                if type(i) != LineGen:
                    self.gen[i].BrushColor = parent2.gen[randomgen].PenColor
                else:
                    self.gen[i].PenColor = parent2.gen[randomgen].PenColor
            elif randomel == 6:
                self.gen[i].startPoints[0] = int(abs(((1+coef) * parent2.gen[randomgen].startPoints[0] 
                                                  + (1 - coef) * parent2.gen[i].startPoints[0])/2))
                if self.gen[i].startPoints[0] > self.sizeX:
                    self.gen[i].startPoints[0] = int(abs(2 * self.sizeX - self.gen[i].startPoints[0]))
            elif randomel == 7:
                self.gen[i].startPoints[1] = int(abs(((1+coef) * parent2.gen[randomgen].startPoints[1]
                                                  + (1 - coef) * parent2.gen[i].startPoints[1])/2))
                if self.gen[i].startPoints[1] > self.sizeY:
                    self.gen[i].startPoints[1] = int(abs(2 * self.sizeY - self.gen[i].startPoints[1]))
            elif randomel == 8:
                self.gen[i].endPoints[0] = int(abs(((1+coef) * parent2.gen[randomgen].endPoints[0]
                                                 + (1 - coef) * parent2.gen[i].endPoints[0])/2))
                if self.gen[i].endPoints[0] > self.sizeX:
                    self.gen[i].endPoints[0] = int(abs(2 * self.sizeX - self.gen[i].endPoints[0]))
            elif randomel == 9:
                self.gen[i].endPoints[1] = int(abs(((1+coef) * parent2.gen[randomgen].endPoints[1]
                                                     + (1 - coef) * parent2.gen[i].endPoints[1])/2))
                if self.gen[i].endPoints[1] > self.sizeY:
                    self.gen[i].endPoints[1] = int(abs(2 * self.sizeY - self.gen[i].endPoints[1]))
            if self.gen[i].startPoints[0] > self.gen[i].endPoints[0]:
                b = self.gen[i].startPoints[0]
                self.gen[i].startPoints[0] =  self.gen[i].endPoints[0]
                self.gen[i].endPoints[0] = b
            if self.gen[i].startPoints[1] > self.gen[i].endPoints[1]:
                b = self.gen[i].startPoints[1]
                self.gen[i].startPoints[1] =  self.gen[i].endPoints[1]
                self.gen[i].endPoints[1] = b
        self.generateImg()

    def generateByCrossover_1(self, parent1, parent2):
        self.orderlyCrossing(parent1, parent2)
        for i in range(1, len(parent1.gen)):
            self.gen.append(parent1.gen[i].returnNewGen_1(parent2.gen[i]))
        self.generateImg()

    def generateByCrossover_2(self, parent1, parent2):
        self.orderlyCrossing(parent1, parent2)
        for i in range(1, len(parent1.gen)):
            self.gen.append(parent1.gen[i].returnNewGen_2(parent2.gen[i]))
        self.generateImg()

    def generateByCrossover_3(self, parent1, parent2):
        self.orderlyCrossing(parent1, parent2)
        for i in range(1, len(parent1.gen)):
            self.gen.append(parent1.gen[i].returnNewGen_3(parent2.gen[i]))
        self.generateImg()

    def generateByCrossover_4(self, parent1, parent2):
        self.orderlyCrossing(parent1, parent2)
        for i in range(1, len(parent1.gen)//2):
            self.gen.append(copy.deepcopy(parent1.gen[i]))
        for i in range(len(parent1.gen)//2, len(parent1.gen)):
            self.gen.append(copy.deepcopy(parent2.gen[i]))
        self.generateImg()

    def generateByCrossover_blend(self, parent1, parent2):
        self.orderlyCrossing(parent1, parent2)
        genlen = len(parent1.gen)
        for i in range(1, len(parent1.gen)):
            self.gen.append(parent1.gen[i].returnNewGen_blend(parent2.gen[i]))
            if self.gen[i].startPoints[0] > self.sizeX:
                self.gen[i].startPoints[0] = abs(2* self.sizeX - self.gen[i].startPoints[0])
            if self.gen[i].startPoints[1] > self.sizeY:
                self.gen[i].startPoints[1] = abs(2* self.sizeY - self.gen[i].startPoints[1])
            if self.gen[i].endPoints[0] > self.sizeX:
                self.gen[i].endPoints[0] = abs(2 * self.sizeX - self.gen[i].endPoints[0])
            if self.gen[i].endPoints[1] > self.sizeY:
                self.gen[i].endPoints[1] = abs(2 * self.sizeY - self.gen[i].endPoints[1])

            if self.gen[i].startPoints[0] > self.gen[i].endPoints[0]:
                b = self.gen[i].startPoints[0]
                self.gen[i].startPoints[0] =  self.gen[i].endPoints[0]
                self.gen[i].endPoints[0] = b
            if self.gen[i].startPoints[1] > self.gen[i].endPoints[1]:
                b = self.gen[i].startPoints[1]
                self.gen[i].startPoints[1] =  self.gen[i].endPoints[1]
                self.gen[i].endPoints[1] = b
        self.generateImg()

    def changeOrderfunc(self):
        randomgen1 = randint(0, len(self.gen[0])-1)
        randomgen2 = randint(0, len(self.gen[0])-1)
        buf = self.gen[0][randomgen1]
        self.gen[0][randomgen1] = self.gen[0][randomgen2]
        self.gen[0][randomgen2] = buf
        self.generateImg()

    def changeColorfunc(self):
        randomgen = randint(1, len(self.gen[0]))
        self.gen[randomgen].PenColor = (randint(0,255),randint(0,255),randint(0,255))
        if self.gen[randomgen].BrushColor:
            self.gen[randomgen].BrushColor = (randint(0,255),randint(0,255),randint(0,255))
        self.generateImg()

    def changePosfunc(self):
        randomgen = randint(1, len(self.gen[0]))
        coord = self.generateCoord()
        self.gen[randomgen].startPoints = [coord[0],coord[1]]
        self.gen[randomgen].endPoints = [coord[2],coord[3]]
        self.generateImg()

    def setName(self,text):
        if len(text) <= 25:
            self.name = text
        else:
            self.name = text[:25]

    def paintIndivid(self, drawImg):
        draws = drawImg
        #print(self.gen[0])
        for i in self.gen[0]:
            draws = self.gen[i].paintFigure(drawImg)
            drawImg = draws
        return drawImg
