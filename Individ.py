from PIL import Image, ImageDraw
import Genom
import CircleGen
import LineGen
import RectGen
from random import randint

class Individ(object):
    
    def __init__(self, x, y):
        self.sizeX = x
        self.sizeY = y
        self.gen = []
        self.fit = 0

        #self.createIndivid()

    def generateIndivid(self, figures):  #Как установить порядок? Перемешиванием? (как вариант.... а потом передавать порядок "генетически"?)
        self.gen = []
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

        for i in range(len(self.gen)): #перемешиваем для смены порядка прорисовки
            rand = randint(0,len(self.gen)-1)
            c = self.gen[i]
            self.gen[i] = self.gen[rand]
            self.gen[rand] = c

    def paintIndivid(self, drawImg):
        draws = drawImg
        for i in self.gen:
            print(i.startPoints, i.endPoints)
            draws = i.paintFigure(drawImg)
            drawImg = draws

        return drawImg