import Individ
from random import randint
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage import data, img_as_float
import os

class Population(object):
    
    def __init__(self):
        self.size = 0
        self.startize = 0
        self.newgenarateSize = self.size * 15
        self.subPopulation = []
        self.individs = []
        self.newgeneratedIndivids = []
        self.canvaSize = [0,0]
        self.countFigure = [0,0,0] #[circle, rect, line]
        self.oldIndivids = []
        self.mutationchance = 10
        #self.indexImgToShow = 0

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
        self.subPopulation = Population()
        self.subPopulation.canvaSize = self.canvaSize
        self.subPopulation.countFigure = self.countFigure
        self.subPopulation.size = self.size

    def prepareTOCrossover(self):
        self.oldIndivids = self.individs

    def autoGenerating(self):
        for i in self.subPopulation.individs:
            self.newgeneratedIndivids.append(i)
        leftToGener = self.newgenarateSize - len(self.newgeneratedIndivids)
        while leftToGener > 0:
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
            genertype = randint(1, 6)
            individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
            if genertype ==1:
                individ.generateByCrossover_1(parent1,parent2)
            elif genertype ==2:
                individ.generateByCrossover_2(parent1,parent2)
            elif genertype ==3:
                individ.generateByCrossover_3(parent1,parent2)
            elif genertype ==4:
                individ.generateByCrossover_4(parent1,parent2)
            elif genertype ==5:
                individ.generateByCrossover_share(parent1,parent2)
            elif genertype ==6:
                individ.generateByCrossover_blend(parent1,parent2)
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
            leftToGener -= 1

    def removeLoosers(self):
        self.individs = []
        bord = self.size - self.startize //2 
        self.size = int(self.startize * 1.5) 
        for i in self.oldIndivids:
            if i.rang > bord:
                self.individs.append(i)
        rng = self.size-len(self.individs)
        subpoplen  = len(self.subPopulation.individs)
        for i in range(min(rng, subpoplen)):
            self.individs.append(self.subPopulation.individs[i])
        rng = self.size-len(self.individs)
        if rng > 0:
            metricsList = {}
            for i in range(len(self.newgeneratedIndivids)):
                dat1 = img_as_float(self.newgeneratedIndivids[i].img)
                metricsval = 0
                for j in self.oldIndivids:
                    dat2 = img_as_float(j.img)
                    countmetr = ssim(dat1,dat2, multichannel=True)
                    print("countermetrics",countmetr)
                    if countmetr > 0.95: 
                        metricsval = (self.size + 1)/2 * self.size #если будет слишком высокая степень схожестис одним из предыдущих элементов, то после сортировки и реверсирования масива, элемент окажется в конце
                        break
                    metricsval += countmetr / j.rang
                metricsval /= (self.size + 1)/2 * self.size # 0 <= metrixval <= 1
                metricsList[metricsval] = i
            list_keys = list(metricsList.keys())
            list_keys.sort()
            list_keys = list(reversed(list_keys))
            #leftToStay = min((self.size+9)//10, len(list_keys))
            for i in range(min(self.size, len(list_keys))):
                self.individs.append(self.newgeneratedIndivids[metricsList[list_keys[i]]])
        for i in self.individs:
            i.rang = 0

    def countMetrics(self, imgData1, imgData2):
        value = 0
        for i in range(len(imgData1)):
            value +=  ((
                (abs(imgData2[i][0] - imgData1[i][0])/255)**2 +
                (abs(imgData2[i][1] - imgData1[i][1])/255)**2 +
                (abs(imgData2[i][2] - imgData1[i][2])/255)**2)/3) **(1/2) # 0 <= value <= 1
        return value/(self.canvaSize[0]*self.canvaSize[1])
       
    def crossover_share(self, par1, par2):
        individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
        individ.generateByCrossover_share(self.individs[par1-1],self.individs[par2-1])
        self.subPopulation.individs.append(individ)

    def crossover_blend(self, par1, par2):
        individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
        individ.generateByCrossover_blend(self.individs[par1-1],self.individs[par2-1])
        self.subPopulation.individs.append(individ)

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
            if n <= 30:
                self.size = n
            else: self.size = 30
        self.startize = self.size
        self.newgenarateSize = self.size * 2

    def setcanvaSizeX(self, text):
        if text.isdigit():
            n = int(text)
            if n >= 300: ###
                n = 300
            self.canvaSize[0] = n

    def setRang(self, text, pictInd):
        if text.isdigit():
            n = int(text)
            if n > self.size: 
                n = 0
            self.individs[pictInd].rang = n
        print(self.size)
        print("ln ",len(self.individs))

    def setcanvaSizeY(self, text):
        if text.isdigit():
            n = int(text)
            if n >= 300: ###
                n = 300
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
            if n > 400: ###
                n = 400
            self.countFigure[2] = n

    def setMutationChance(self,text):
        if text.isdigit():
            n = int(text)
            if n > 100: 
                n = 100
            self.mutationchance = n


    def autoGeneratingFake(self):
        self.newgeneratedIndivids = []
        leftToGener = self.newgenarateSize
        while leftToGener > 0:
            allPie = (self.size + 1)/2 * self.size
            piePart1 = randint(1, allPie)
            countPieParts = 0
            #print(allPie, piePart1, len(self.oldIndivids))
            for i in self.oldIndivids:
                countPieParts += i.rang
                if piePart1 <= countPieParts:
                    parent1 = i
                    break
            piePart2 = randint(1, (allPie-parent1.rang-1))
            #print(allPie, piePart1, len(self.oldIndivids))
            parent2 = parent1
            for i in self.oldIndivids:
                if i == parent1 and len(self.oldIndivids) != 1:
                    pass
                else:
                    countPieParts += i.rang
                    if piePart1 <= countPieParts:
                        parent2 = i
                        break
            genertype = randint(1, 4)
            individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
            #if genertype ==1:
            #    individ.generateByCrossover_1(parent1,parent2)
            #elif genertype ==2:
            #    individ.generateByCrossover_2(parent1,parent2) 
            #elif genertype ==3:
            #    individ.generateByCrossover_3(parent1,parent2)
            #elif genertype ==4:
            #    individ.generateByCrossover_4(parent1,parent2)
            #elif genertype ==5:
            #    individ.generateByCrossover_share(parent1,parent2)
            #elif genertype ==6:
            #    individ.generateByCrossover_blend(parent1,parent2)

            if genertype == 1:
                individ.generateByCrossover_share(parent1,parent2) #строит одну фигуру на весь холст
            elif genertype == 2:
                individ.generateByCrossover_blend(parent1,parent2) #как гвоздями прибивает в верхний левый угол + постепенно уменьшает фигуры
            elif genertype == 3:
                individ.generateByCrossover_shareblend(parent1,parent2) #тоже строит одну фигуру на весь холст
            elif genertype == 4:
                individ.generateByCrossover_sharerand(parent1,parent2) #делает вообще все черным
            c = 10
            while c > 0 :
                generchance = randint(0, 100)
                if generchance <= self.mutationchance:
                    genermuttype = randint(1, 3)
                    if genermuttype == 1:
                        individ.changeOrderfunc()
                    elif genermuttype == 2:
                        individ.changeColorfunc()
                    elif genermuttype == 3:
                        individ.changePosfunc()
                    c -= 1
                else:
                    break
            self.newgeneratedIndivids.append(individ)
            leftToGener -= 1
        for i in self.individs:
            self.newgeneratedIndivids.append(i)

    def removeWorseFake(self, origimg):
        self.individs = []
        if self.size > 0:
            metricsList = {}
            for i in range(len(self.newgeneratedIndivids)):
                dat1 = img_as_float(self.newgeneratedIndivids[i].img)
                dat2 = img_as_float(origimg)
                countmetr = ssim(dat1,dat2, multichannel=True)
                print("countermetrics",countmetr)
                metricsList[countmetr] = i
            list_keys = list(metricsList.keys())
            list_keys.sort()
            leftToStay = min((self.size+9)//10, len(list_keys))
            for i in range(len(list_keys)):
                self.newgeneratedIndivids[metricsList[list_keys[i]]].rang = i+1
            list_keys = list(reversed(list_keys))
            rangList = {}
            for i in range(leftToStay):
                self.individs.append(self.newgeneratedIndivids[metricsList[list_keys[i]]])
                rangList[self.individs[len(self.individs)-1].rang] = i
            newindlen = len(self.newgeneratedIndivids)
            allPie = (newindlen + 1)/2 * newindlen - (2*newindlen - leftToStay + 1)/2 * leftToStay
            leftToStay = self.size - leftToStay
            while leftToStay > 0:
                piePart = randint(1, allPie)
                countPieParts = 0
                for i in self.newgeneratedIndivids:
                    if i not in self.individs:
                        countPieParts += i.rang
                        if piePart <= countPieParts:
                            self.individs.append(i)
                            allPie -= i.rang
                            rangList[i.rang] = len(self.individs)-1
                            leftToStay -= 1
                            break
            list_keys = list(rangList.keys())
            list_keys.sort()
            for i in range(len(list_keys)):
                self.individs[rangList[list_keys[i]]].rang = i+1
        self.oldIndivids = self.individs


    def savePictureFake(self, iternum: str):
        if not os.path.isdir("savedpict"):
            os.mkdir("savedpict")
        if not os.path.isdir("savedpict//"+iternum):
            os.mkdir("savedpict//"+iternum)
        for i in self.individs:
            name = str(i.rang)
            if not name:
                name = "untitled"
            count = 0
            for address, dirs, files in os.walk("savedpict//"+iternum):
                nameaddition = ".jpg"
                while (name + nameaddition) in files:
                    count += 1
                    nameaddition = "(" + str(count) +").jpg"
            if count != 0:
                name += nameaddition
            else:
                name += ".jpg"
            savename = "savedpict//"+ iternum + "//" + name
            i.img.save(savename)