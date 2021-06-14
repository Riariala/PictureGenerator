import Individ
from random import randint
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
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
        self.cont = True
        self.gradeLeft = []

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
        c = 0
        for i in self.individs:
            i.rang = 0
            c+=1
            self.gradeLeft.append(c)

    def prepareTOCrossover(self):
        self.oldIndivids = self.individs

    def autoGenerating(self):
        self.newgenarateSize = 20 * self.size
        self.newgeneratedIndivids = []
        for i in self.subPopulation.individs:
            i.rang = 1
            self.newgeneratedIndivids.append(i)
        leftToGener = self.newgenarateSize - len(self.newgeneratedIndivids)
        for i in self.oldIndivids:
            print("rang",i.rang)
        while leftToGener > 0:
            allPie = (self.size + 1)/2 * self.size
            piePart1 = randint(1, allPie)
            countPieParts = 0
            print("allPie", allPie)
            for i in self.oldIndivids:
                countPieParts += i.rang
                if piePart1 <= countPieParts:
                    parent1 = i
                    break
            print("allPie-parent1.rang", allPie, parent1.rang)
            piePart2 = randint(1, (allPie-parent1.rang))
            parent2 = parent1
            for i in self.oldIndivids:
                if i == parent1 and len(self.oldIndivids) != 1:
                    continue
                else:
                    countPieParts += i.rang
                    if piePart1 <= countPieParts:
                        parent2 = i
                        break
            individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
            individ.genarate_1(parent1, parent2, self.countFigure)
            c = 10
            while c > 0 :
                generchance = randint(0, 100)
                if generchance <= self.mutationchance:
                    genermuttype = randint(1, 4)
                    if genermuttype == 1:
                        individ.floatmut()
                    elif genermuttype == 2:
                        individ.changeplaces()
                    elif genermuttype == 3:
                        individ.chaneOrder()
                    elif genermuttype == 4:
                        individ.deepmutation()
                    c -= 1
                else:
                    break
            self.newgeneratedIndivids.append(individ)
            leftToGener -= 1

    def removeLoosers(self):
        rangSum = (len(self.oldIndivids) + 1)/2  * len(self.oldIndivids)
        self.individs = []
        bord = self.size - self.startize //2 
        self.size = int(self.startize * 1.5) 
        maxbord = len(self.oldIndivids)
        if self.oldIndivids:
            for i in self.oldIndivids:
                if i.rang > bord:
                    i.survival += 1/((maxbord - i.rang +1)**2)
                    self.individs.append(i)
        rng = self.size - len(self.individs)
        halfrang = len(self.oldIndivids)/2
        if rng > 0:
            metricsList = {}
            for i in range(len(self.newgeneratedIndivids)):
                dat1 = img_as_float(self.newgeneratedIndivids[i].img)
                metricsval = 0
                for j in self.oldIndivids:
                    dat2 = img_as_float(j.img)
                    countmetr = mse(dat1, dat2)
                    print("countermetrics",countmetr)
                    if countmetr <= 0.005:
                        self.newgeneratedIndivids[i].lookslike = True
                    metricsval += countmetr * ((j.rang **2)/halfrang**2-1) / 3
                print("1",metricsval)
                if metricsval != -1:
                    metricsval *= -1
                    self.newgeneratedIndivids[i].fit = metricsval
                    print("2",metricsval)
                    metricsList[i] = metricsval
            list_keys = sorted(metricsList, key=metricsList.get)
            leftToStay = min(rng - rng//5, len(list_keys)) ##### 80% элитизм, для mse оказалось лучшим решением его увеличить
            for i in range(len(list_keys)):
                self.newgeneratedIndivids[list_keys[i]].rang = i+1
            list_keys = list(reversed(list_keys))
            for i in self.individs:
                i.rang = len(self.newgeneratedIndivids) + i.rang - bord
            alreadyin = []
            for i in range(self.newgenarateSize):
                if leftToStay > 0:
                    if self.newgeneratedIndivids[list_keys[i]].fit not in alreadyin:
                        self.individs.append(self.newgeneratedIndivids[list_keys[i]])
                        alreadyin.append(self.newgeneratedIndivids[list_keys[i]].fit)
                        leftToStay -= 1
                else:
                    break
            newindlen = len(self.newgeneratedIndivids)
            allPie = (newindlen + 1)/2 * newindlen - (2*newindlen - leftToStay + 1)/2 * leftToStay
            leftToStay = min(self.size - len(self.individs), len(list_keys))
            while leftToStay > 0:
                piePart = randint(1, allPie)
                countPieParts = 0
                for i in self.newgeneratedIndivids:
                    if (i not in self.individs) and (i.fit not in alreadyin):
                        print(i.fit, alreadyin)
                        countPieParts += i.rang
                        if piePart <= countPieParts:
                            self.individs.append(i)
                            allPie -= i.rang
                            leftToStay -= 1
                            alreadyin.append(i.fit)
                            break
            rangList = {}
            countSimilar = 0
            for i in range(len(self.individs)):
                rangList[self.individs[i].rang] = i
                if self.individs[i].lookslike:
                    countSimilar += 1
                self.individs[i].lookslike = False
                datcheck1 = img_as_float(self.individs[i].img)
                for j in range(len(self.individs)):
                    datcheck2 = img_as_float(self.individs[j].img)
                    countmetrch = mse(datcheck1, datcheck2)
                    print("countmetrch", countmetrch)
                    if countmetrch != 0 and countmetrch <= 0.011:
                        self.individs[i].lookslike = True
                        break
                #self.individs[i].rang = 1
            if countSimilar >= len(self.individs) * 2/3:
                self.cont = True
            else:
                self.cont = False
            countSimilar = 0
            for i in self.individs:
                if i.lookslike:
                    countSimilar += 1
            if countSimilar >= len(self.individs) / 2:
                self.cont = True
            list_keys = list(rangList.keys())
            list_keys.sort()
            for i in range(len(list_keys)):
                self.individs[rangList[list_keys[i]]].rang = i + 1
        self.oldIndivids = self.individs

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
            if n != self.individs[pictInd].rang:
                if n in self.gradeLeft:
                    self.gradeLeft.append(self.individs[pictInd].rang)
                    self.gradeLeft.remove(n)
                    self.individs[pictInd].rang = n
                    self.gradeLeft.sort()

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

    def orderMate(self, parent1, parent2):
        individ = Individ.Individ(self.canvaSize[0], self.canvaSize[1])
        individ.orderMate(self.individs[parent1-1], self.individs[parent2-1],self.countFigure)
        self.subPopulation.individs.append(individ)

    def  callgenarate_1(self, parent1,parent2):
        individ = Individ.Individ(self.canvaSize[0], self.canvaSize[1])
        individ.genarate_1(self.individs[parent1-1],self.individs[parent2-1], self.countFigure)
        self.subPopulation.individs.append(individ)

    def callFloatmut(self, individIndex):
        self.individs[individIndex].floatmut()

    def callChangeplaces(self, individIndex):
        self.individs[individIndex].changeplaces()

    def callChaneOrder(self, individIndex):
        self.individs[individIndex].chaneOrder()

    def callDeepmutation(self, individIndex):
        self.individs[individIndex].deepmutation()


    #def autoGeneratingFake(self):
    #    self.newgeneratedIndivids = []
    #    leftToGener = self.newgenarateSize
    #    while leftToGener > 0:
    #        allPie = (self.size + 1)/2 * self.size
    #        piePart1 = randint(1, allPie)
    #        countPieParts = 0
    #        for i in self.oldIndivids:
    #            countPieParts += i.rang
    #            if piePart1 <= countPieParts:
    #                parent1 = i
    #                break
    #        piePart2 = randint(1, (allPie-parent1.rang-1))
    #        parent2 = parent1
    #        for i in self.oldIndivids:
    #            if i == parent1 and len(self.oldIndivids) != 1:
    #                pass
    #            else:
    #                countPieParts += i.rang
    #                if piePart1 <= countPieParts:
    #                    parent2 = i
    #                    break
    #        genertype = randint(1, 1)
    #        individ = Individ.Individ(self.canvaSize[0],self.canvaSize[1])
    #        if genertype == 1:
    #            individ.genarate_1(parent1,parent2, self.countFigure)
    #        c = 10
    #        while c > 0 :
    #            generchance = randint(0, 100)
    #            if generchance <= self.mutationchance:
    #                genermuttype = randint(1, 5)
    #                if genermuttype == 1:
    #                    individ.floatmut()
    #                elif genermuttype == 2:
    #                    individ.changeplaces()
    #                elif genermuttype == 3:
    #                    individ.chaneOrder()
    #                else:
    #                    individ.deepmutation()
    #                c -= 1
    #            else:
    #                break
    #        self.newgeneratedIndivids.append(individ)
    #        leftToGener -= 1
    #    for i in self.individs:
    #        self.newgeneratedIndivids.append(i)

    #def removeWorseFake(self, origimg, isssim: bool):
    #    self.individs = []
    #    if self.size > 0:
    #        metricsList = {}
    #        for i in range(len(self.newgeneratedIndivids)):
    #            dat1 = img_as_float(self.newgeneratedIndivids[i].img)
    #            dat2 = img_as_float(origimg)
    #            if isssim:
    #                countmetr = ssim(dat1,dat2, multichannel=True)
    #            else:
    #                countmetr = mse(dat1,dat2) * (-1)
    #            print("countermetrics",countmetr)
    #            metricsList[countmetr] = i
    #        list_keys = list(metricsList.keys())
    #        list_keys.sort()
    #        if isssim:
    #            leftToStay = min((self.size+9)//10, len(list_keys)) #####
    #        else:
    #            leftToStay = min(self.size//2, len(list_keys)) #####
    #        for i in range(len(list_keys)):
    #            self.newgeneratedIndivids[metricsList[list_keys[i]]].rang = i+1
    #        list_keys = list(reversed(list_keys))
    #        rangList = {}
    #        for i in range(leftToStay):
    #            self.individs.append(self.newgeneratedIndivids[metricsList[list_keys[i]]])
    #            rangList[self.individs[len(self.individs)-1].rang] = i
    #        newindlen = len(self.newgeneratedIndivids)
    #        allPie = (newindlen + 1)/2 * newindlen - (2*newindlen - leftToStay + 1)/2 * leftToStay
    #        leftToStay = self.size - leftToStay
    #        while leftToStay > 0:
    #            piePart = randint(1, allPie)
    #            countPieParts = 0
    #            for i in self.newgeneratedIndivids:
    #                if i not in self.individs:
    #                    countPieParts += i.rang
    #                    if piePart <= countPieParts:
    #                        self.individs.append(i)
    #                        allPie -= i.rang
    #                        rangList[i.rang] = len(self.individs)-1
    #                        leftToStay -= 1
    #                        break
    #        list_keys = list(rangList.keys())
    #        list_keys.sort()
    #        for i in range(len(list_keys)):
    #            self.individs[rangList[list_keys[i]]].rang = i+1
    #    self.oldIndivids = self.individs


    #def savePictureFake(self, iternum: str, isssim):
    #    if isssim:
    #        folder = "ssim"
    #    else:
    #        folder = "mse"
    #    if not os.path.isdir("savedpict"):
    #        os.mkdir("savedpict")
    #    if not os.path.isdir("savedpict//" + folder):
    #        os.mkdir("savedpict//"+ folder)
    #    folder += "//"
    #    if not os.path.isdir("savedpict//" + folder + iternum):
    #        os.mkdir("savedpict//"+ folder + iternum)
    #    for i in self.individs:
    #        name = str(i.rang)
    #        if not name:
    #            name = "untitled"
    #        count = 0
    #        for address, dirs, files in os.walk("savedpict//"+ folder +iternum):
    #            nameaddition = ".jpg"
    #            while (name + nameaddition) in files:
    #                count += 1
    #                nameaddition = "(" + str(count) +").jpg"
    #        if count != 0:
    #            name += nameaddition
    #        else:
    #            name += ".jpg"
    #        savename = "savedpict//"+ folder + iternum + "//" + name
    #        i.img.save(savename)