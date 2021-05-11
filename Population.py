import Individ

class Population(object):
    
    def __init__(self):
        self.size = 0
        self.individs = []
        self.canvaSize = [0,0] #[x,y]
        self.countFigure = [0,0,0] #[circle, rect, line]
        self.oldIndivids = []

    def genetatePopulation(self):
        self.individs = []
        for i in range(self.size):
            self.individs.append(Individ.Individ(self.canvaSize[0],self.canvaSize[1]))
            self.individs[i].generateIndivid(self.countFigure)
            print(self.individs[i].sizeX)
    
    def setFitToIndivid(self, fitVal, pictind):
         self.individs[pictind].fit = fitVal

    def prepareTOCrossover(self):
        self.oldIndivids = self.individs
        self.individs = []
        sm = 0
        for i in self.oldIndivids:
            sm += i.fit
        mid = int(sm/self.size)
        for i in self.oldIndivids:
            if i.fit > mid:
                self.individs.append(i)
       
    def crossover(self, par1, par2):
        print(par1,par2 )
        individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
        individ.generateByCrossover(self.individs[par1-1],self.individs[par2-1])
        self.individs.append(individ)

    def setSize(self, text):
        if text.isdigit():
            n = int(text)
            if n < 20:
                self.size = n
            else: self.size = 20
        print(self.size)

    def setcanvaSizeX(self, text):
        if text.isdigit():
            n = int(text)
            if n >= 250: ###
                n = 250
            self.canvaSize[0] = n
        print(self.canvaSize)

    def setcanvaSizeY(self, text):
        if text.isdigit():
            n = int(text)
            if n >= 250: ###
                n = 250
            self.canvaSize[1] = n
        print(self.canvaSize)

    def setCircleCount(self, text):
        if text.isdigit():
            n = int(text)
            if n > 100: ###
                n = 100
            self.countFigure[0] = n
        print(self.countFigure)

    def setRectCount(self, text):
        if text.isdigit():
            n = int(text)
            if n > 100: ###
                n = 100
            self.countFigure[1] = n
        print(self.countFigure)

    def setLineCount(self, text):
        if text.isdigit():
            n = int(text)
            if n > 100: ###
                n = 100
            self.countFigure[2] = n
        print(self.countFigure)


