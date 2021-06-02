import Individ

class Population(object):
    
    def __init__(self):
        self.size = 0
        #self.newIndivids = []
        self.subPopulation = []
        self.individs = []
        self.canvaSize = [0,0] #[x,y]
        self.countFigure = [0,0,0] #[circle, rect, line]
        self.oldIndivids = []
        #self.cloneIndivid = 0

    def genetatePopulation(self):
        self.individs = []
        for i in range(self.size):
            self.individs.append(Individ.Individ(self.canvaSize[0],self.canvaSize[1]))
            self.individs[i].generateIndivid(self.countFigure)
            #print(self.individs[i].sizeX)
        self.subPopulation = Population()
        self.subPopulation.canvaSize = self.canvaSize
        self.subPopulation.countFigure = self.countFigure
        self.subPopulation.size = self.size
    
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
       
    def crossover_1(self, par1, par2):
        individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
        individ.generateByCrossover_1(self.individs[par1-1],self.individs[par2-1])
        self.subPopulation.individs.append(individ)

    def crossover_2(self, par1, par2):
        individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
        individ.generateByCrossover_2(self.individs[par1-1],self.individs[par2-1])
        self.subPopulation.individs.append(individ)

    def crossover_3(self, par1, par2):
        individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
        individ.generateByCrossover_3(self.individs[par1-1],self.individs[par2-1])
        self.subPopulation.individs.append(individ)

    def prepareToSelect(self):
        for i in self.subPopulation.individs:
            self.individs.append(i)
        self.subPopulation = Population()
        self.subPopulation.canvaSize = self.canvaSize
        self.subPopulation.countFigure = self.countFigure
        self.subPopulation.size = self.size

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