import Individ
from random import randint
import numpy as np

class Population(object):
    
    def __init__(self):
        self.size = 0
        self.startize = 0
        self.newgenarateSize = self.size * 2
        self.subPopulation = []
        self.individs = []
        self.newgeneratedIndivids = []
        self.canvaSize = [0,0]
        self.countFigure = [0,0,0] #[circle, rect, line]
        self.oldIndivids = []
        self.mutationchance = 10

    def genetatePopulation(self):
        self.individs = []
        for i in range(self.size):
            self.individs.append(Individ.Individ(self.canvaSize[0],self.canvaSize[1]))
            self.individs[i].generateIndivid(self.countFigure)
        self.subPopulation = Population()
        self.subPopulation.canvaSize = self.canvaSize
        self.subPopulation.countFigure = self.countFigure
        self.subPopulation.size = self.size

    def prepareToSelect(self):
        for i in self.newgeneratedIndivids:
            self.individs.append(i)
        self.subPopulation = Population()
        self.subPopulation.canvaSize = self.canvaSize
        self.subPopulation.countFigure = self.countFigure
        self.subPopulation.size = self.size

    def prepareTOCrossover(self):
        self.oldIndivids = self.individs
        #self.individs = []
        #for i in self.oldIndivids:
        #    if i.delInd:
        #        self.individs.append(i)

    def autoGenerating(self):
        for i in self.subPopulation.individs:
            self.newgeneratedIndivids.append(i)
        leftToGener = self.newgenarateSize - len(self.newgeneratedIndivids)
        print(self.newgenarateSize, len(self.newgeneratedIndivids), leftToGener)
        while leftToGener > 0:
            print("141")
            allPie = (self.size + 1)/2 * self.size
            piePart1 = randint(1, allPie)
            countPieParts = 0
            for i in self.oldIndivids:
                countPieParts += i.rang
                if piePart1 <= countPieParts:
                    parent1 = i
                    break
            piePart2 = randint(1, (allPie-parent1.rang))
            for i in self.oldIndivids:
                if i == parent1 and len(self.oldIndivids) != 1:
                    continue
                countPieParts += i.rang
                if piePart1 <= countPieParts:
                    parent2 = i
                    break
            genertype = randint(1, 4)
            individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
            if genertype ==1:
                individ.generateByCrossover_1(parent1,parent2)
            elif genertype ==2:
                individ.generateByCrossover_2(parent1,parent2)
            elif genertype ==3:
                individ.generateByCrossover_3(parent1,parent2)
            elif genertype ==4:
                individ.generateByCrossover_4(parent1,parent2)
            while True:
                generchance = randint(0, 100)
                if generchance <= self.mutationchance:
                    genermuttype = randint(1, 3)
                    if genermuttype == 1:
                        individ.changeOrderfunc()
                    elif genermuttype == 2:
                        individ.changeColorfunc()
                    elif genermuttype == 3:
                        individ.changePosfunc()
                else:
                    break
            self.newgeneratedIndivids.append(individ)
            #print(individ.gen[0])
            leftToGener -= 1

    def removeLoosers(self):
        print("len ",len(self.newgeneratedIndivids))
        metrixList = []
        for i in range(len(self.newgeneratedIndivids)):
            data = list(self.newgeneratedIndivids[i].img.getdata())
            metrixval = 0
            #print(self.newgeneratedIndivids[i].gen[0])
            for j in self.oldIndivids:
                data2 = list(j.img.getdata())
                metrixval += self.countMetrix(data,data2) * j.rang
                #print(metrixval)
            metrixval /= (self.size + 1)/2 * self.size # 0 <= metrixval <= 1
            metrixList.append([metrixval,i])
            #print("metrix = ", metrixval)
        metrixList.sort()
        self.size = int(self.startize * 1.5)
        
        bord = self.startize //2
        self.individs = []
        for i in self.oldIndivids:
            if i.rang >= bord:
                self.individs.append(i)
        rng = self.size-len(self.individs)
        for i in range(rng):
            self.individs.append(self.newgeneratedIndivids[metrixList[i][1]])
            #print(self.newgeneratedIndivids[metrixList[i][1]].gen[0])


    def countMetrix(self, imgData1, imgData2):
        value = 0
        for i in range(len(imgData1)):
            value += (((abs(imgData2[i][0] - imgData1[i][0])/255)**2 +(abs(imgData2[i][1] - imgData1[i][1])/255)**2+(abs(imgData2[i][2] - imgData1[i][2])/255)**2)/3) **(1/2) # 0 <= value <= 1
        print("val", value)
        return value/(self.canvaSize[0]*self.canvaSize[1])
       
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
        self.startize = self.size
        self.newgenarateSize = self.size * 2

    def setcanvaSizeX(self, text):
        if text.isdigit():
            n = int(text)
            if n >= 250: ###
                n = 250
            self.canvaSize[0] = n

    def setRang(self, text, pictInd):
        if text.isdigit():
            n = int(text)
            if n > self.size: 
                n = 0
            self.individs[pictInd].rang = n

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

    def setMutationChance(self,text):
        if text.isdigit():
            n = int(text)
            if n > 100: 
                n = 100
            self.mutationchance = n