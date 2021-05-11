from Genom import _Genom_
from random import randint

class CircleGen(_Genom_):
    def __init__(self):
        super().__init__()
        self.PenColor = (0,0,0)
        self.BrushColor = (0,0,0)


    def paintFigure(self, drawImg):
        drawImg.ellipse((self.startPoints[0], self.startPoints[1], self.endPoints[0], self.endPoints[1]), fill=self.BrushColor, outline=self.PenColor)
        return drawImg

    def generateGenom(self, *args):
        self.startPoints = [args[0],args[1]]
        self.endPoints = [args[2],args[3]]
        self.PenColor = (randint(0,255),randint(0,255),randint(0,255))
        self.BrushColor = (randint(0,255),randint(0,255),randint(0,255))

    def returnNewGen(self, neiborGen):
        newGen = CircleGen()
        newGen.startPoints = self.startPoints
        newGen.endPoints = neiborGen.endPoints
        newGen.PenColor = (int((self.PenColor[0]+neiborGen.PenColor[0])/2), int((self.PenColor[1]+neiborGen.PenColor[1])/2), int((self.PenColor[2]+neiborGen.PenColor[2])/2))
        newGen.BrushColor = (int((self.BrushColor[0]+neiborGen.BrushColor[0])/2), int((self.BrushColor[1]+neiborGen.BrushColor[1])/2), int((self.BrushColor[2]+neiborGen.BrushColor[2])/2))
        print(newGen.startPoints, newGen.endPoints, newGen.BrushColor)
        return newGen

