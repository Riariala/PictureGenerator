from PIL import Image, ImageDraw
import Genom
import CircleGen
import LineGen
import RectGen
from random import randint
from itertools import chain

class Individ(object):
    
    def __init__(self, x, y):
        self.sizeX = x
        self.sizeY = y
        self.gen = []
        self.fit = 0
        self.name = ''
        #self.createIndivid()

    def generateIndivid(self, figures):  #Как установить порядок? Перемешиванием? (как вариант.... а потом передавать порядок "генетически"?)
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
                lent = len(self.gen) - 1
                if lent >= 0:
                    self.gen[lent].generateGenom(stx,sty,enx,eny)

        for i in range(figersum): #перемешиваем для смены порядка прорисовки
            rand = randint(0, figersum-1)
            c = self.gen[0][i]
            self.gen[0][i] = self.gen[0][rand]
            self.gen[0][rand] = c


    def orderlyCrossing(self, par1, par2):
        leng = len(par1.gen[0])
        self.gen.append([0 for i in range(leng)])
        #for i in range(leng):
        #    self.gen[0].append(0)
        lenpart = leng//2
        firstHalf = randint(0, (leng-lenpart))
        #ost = lenpart
        #for i in range(leng):
        #    k = randint(1,lenpart) * (ost*(i+1))
        #    if k > 2*lenpart:
        #        self.gen[0][i] = par2.gen[0][i]
        #        ost -=1
        #index = 0
        #for i in range(leng):
        #    while self.gen[0][index] == 0:
        #        index +=1
        #        print(index, i)
        #        if index >=leng:
        #            break
        #    if index >=leng:
        #        break
        #    if par1.gen[0][i] not in self.gen[0]:
        #        self.gen[0][index] = par1.gen[0][i]
        #        #index+=1
        #    else:
        #        continue
        for i in range(firstHalf, firstHalf+lenpart):
            self.gen[0][i] = par2.gen[0][i]
        for i in chain(range(firstHalf), range(firstHalf+lenpart, leng)):
            if par1.gen[0][i] in self.gen[0]: 
                self.gen[0][i] = par2.gen[0][i]
            else: 
                self.gen[0][i] = par1.gen[0][i]


    def generateByCrossover_1(self, parent1, Parent2):
        self.orderlyCrossing(parent1, Parent2)
        for i in range(1, len(parent1.gen)):
            self.gen.append(parent1.gen[i].returnNewGen_1(Parent2.gen[i]))

    def generateByCrossover_2(self, parent1, Parent2):
        self.orderlyCrossing(parent1, Parent2)
        for i in range(1, len(parent1.gen)):
            self.gen.append(parent1.gen[i].returnNewGen_3(Parent2.gen[i]))

    def changeOrderfunc(self):
        randomgen1 = randint(0, len(self.gen[0])-1)
        randomgen2 = randint(0, len(self.gen[0])-1)
        print(randomgen1, randomgen2)
        buf = self.gen[0][randomgen1]
        self.gen[0][randomgen1] = self.gen[0][randomgen2]
        self.gen[0][randomgen2] = buf
        print(self.gen)

    def setName(self,text):
        if len(text) <= 25:
            self.name = text
        else:
            self.name = text[:25]

    def paintIndivid(self, drawImg):
        draws = drawImg
        print(self.gen[0])
        for i in self.gen[0]:
            draws = self.gen[i].paintFigure(drawImg)
            drawImg = draws
        return drawImg
