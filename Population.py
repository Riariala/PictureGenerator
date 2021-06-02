import Individ

class Population(object):
    
    def __init__(self):
        self.size = 0
        self.subPopulation = []
        self.individs = []
        self.canvaSize = [0,0]
        self.countFigure = [0,0,0] #[circle, rect, line]
        self.oldIndivids = []

    def genetatePopulation(self):
        self.individs = []
        for i in range(self.size):
            self.individs.append(Individ.Individ(self.canvaSize[0],self.canvaSize[1]))
            self.individs[i].generateIndivid(self.countFigure)
        self.subPopulation = Population()
        self.subPopulation.canvaSize = self.canvaSize
        self.subPopulation.countFigure = self.countFigure
        self.subPopulation.size = self.size
    
    #def setFitToIndivid(self, fitVal, pictind):
    #     self.individs[pictind].fit = fitVal

    def prepareToSelect(self):
        for i in self.subPopulation.individs:
            self.individs.append(i)
        self.subPopulation = Population()
        self.subPopulation.canvaSize = self.canvaSize
        self.subPopulation.countFigure = self.countFigure
        self.subPopulation.size = self.size

    def prepareTOCrossover(self):
        self.oldIndivids = self.individs
        self.individs = []
        #sm = 0
        #for i in self.oldIndivids:
        #    sm += i.fit
        #mid = int(sm/self.size)
        for i in self.oldIndivids:
            if not i.delInd:
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

    def crossover_4(self, par1, par2):
        individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
        individ.generateByCrossover_4(self.individs[par1-1], self.individs[par2-1])
        self.subPopulation.individs.append(individ)

    def setSize(self, text):
        if text.isdigit():
            n = int(text)
            if n < 20:
                self.size = n
            else: self.size = 20

    def setcanvaSizeX(self, text):
        if text.isdigit():
            n = int(text)
            if n >= 250: ###
                n = 250
            self.canvaSize[0] = n

    def setcanvaSizeY(self, text):
        if text.isdigit():
            n = int(text)
            if n >= 250: ###
                n = 250
            self.canvaSize[1] = n

    def setCircleCount(self, text):
        if text.isdigit():
            n = int(text)
            if n > 100: ###
                n = 100
            self.countFigure[0] = n

    def setRectCount(self, text):
        if text.isdigit():
            n = int(text)
            if n > 100: ###
                n = 100
            self.countFigure[1] = n

    def setLineCount(self, text):
        if text.isdigit():
            n = int(text)
            if n > 100: ###
                n = 100
            self.countFigure[2] = n