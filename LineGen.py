from Genom import _Genom_
from random import randint,uniform

class LineGen(_Genom_):
    def __init__(self):
        super().__init__()
        self.PenColor = (0,0,0)
        self.BrushColor = 0
        self.width = 0
        self.type = "l"

    def paintFigure(self, drawImg):
        drawImg.line((self.startPoints[0], self.startPoints[1], self.endPoints[0], self.endPoints[1]), fill=self.PenColor, width=self.width)
        return drawImg

    def generateGenom(self, *args):
        arg = [args[0],args[1],args[2],args[3]]
        for i in range(4):
            rand = randint(0,3)
            c = arg[i]
            arg[i] = arg[rand]
            arg[rand] = c
        self.startPoints = [arg[0],arg[1]]
        self.endPoints = [arg[2],arg[3]]
        self.PenColor = (randint(0,255),randint(0,255),randint(0,255))
        self.width = randint(0,15)

    def returnNewGen_1(self, neiborGen):
        newGen = LineGen()
        newGen.startPoints = self.startPoints
        newGen.endPoints = neiborGen.endPoints
        newGen.PenColor = (int((self.PenColor[0]+neiborGen.PenColor[0])/2), int((self.PenColor[1]+neiborGen.PenColor[1])/2), int((self.PenColor[2]+neiborGen.PenColor[2])/2))
        newGen.width = self.width
        if type(neiborGen) == LineGen:
            if randint(0,1) == 0:
                newGen.width = neiborGen.width
        return newGen

    def returnNewGen_2(self, neiborGen):
        newGen = LineGen()
        newGen.startPoints = neiborGen.startPoints
        newGen.endPoints = neiborGen.endPoints
        newGen.PenColor = self.PenColor
        newGen.width = self.width
        if type(neiborGen) == LineGen:
            if randint(0,1) == 0:
                newGen.width = neiborGen.width
        return newGen

    def returnNewGen_3(self, neiborGen):
        newGen = LineGen()
        newGen.startPoints = [neiborGen.startPoints[0], self.startPoints[1]]
        newGen.endPoints = [self.endPoints[0], neiborGen.endPoints[1]]
        newGen.PenColor = neiborGen.PenColor
        newGen.width = self.width
        if type(neiborGen) == LineGen:
            if randint(0,1) == 0:
                newGen.width = neiborGen.width
        return newGen

    def returnNewGen_blend(self, neiborGen):
        newGen = LineGen()
        coef = uniform(0, 1.5)
        for i in range(2):
            value = int(((1+coef)*self.startPoints[i] + (1-coef)*neiborGen.startPoints[i])/2)
            if value < 0:
                value = 0
            newGen.startPoints[i] = value
        for i in range(2):
            value = int(((1+coef)*self.endPoints[i] + (1-coef)*neiborGen.endPoints[i])/2)
            if value < 0:
                value = 0
            newGen.endPoints[i] = value
        value = []
        for i in range(3):
            value.append(int(((1+coef)*self.PenColor[i] + (1-coef)*neiborGen.PenColor[i])/2))
            if value[i] < 0:
                value[i] = 0
            elif value[i] > 255:
                value[i] = 255
        newGen.PenColor = (value[0], value[1], value[2])
        return newGen

    def returnNewGen_sharerand(self, neiborGen, randomGen):
        newGen = LineGen()
        coef = uniform(0, 2)
        for i in range(2):
            value = int(abs(((1+coef)*self.startPoints[i] + (1-coef)*(neiborGen.startPoints[i] + randomGen.startPoints[i])/2)/2))
            newGen.startPoints[i] = value
        for i in range(2):
            value = int(abs(((1+coef)*self.endPoints[i] + (1-coef)*(neiborGen.endPoints[i] + randomGen.endPoints[i])/2)/2))
            newGen.endPoints[i] = value
        value = []
        for i in range(3):
            value.append(int(abs(((1+coef)*self.PenColor[i] + (1-coef)*(neiborGen.BrushColor[i] + randomGen.BrushColor[i])/2)/2)))
            if value[i] > 255:
                value[i] = abs(510 - value[i])
        newGen.BrushColor = (value[0], value[1], value[2])
        return newGen