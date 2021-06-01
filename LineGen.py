from Genom import _Genom_
from random import randint

class LineGen(_Genom_):
    def __init__(self):
        super().__init__()
        self.PenColor = (0,0,0)
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
        return newGen

    def returnNewGen_2(self, neiborGen):
        newGen = LineGen()
        newGen.startPoints = neiborGen.startPoints
        newGen.endPoints = neiborGen.endPoints
        newGen.PenColor = self.PenColor
        return newGen

    def returnNewGen_3(self, neiborGen):
        newGen = LineGen()
        newGen.startPoints = self.startPoints
        newGen.endPoints = (self.endPoints[0], neiborGen.endPoints[1])
        newGen.PenColor = neiborGen.PenColor
        return newGen