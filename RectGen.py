from Genom import _Genom_
from random import randint

class RectGen(_Genom_):
    def __init__(self):
        super().__init__()
        self.PenColor = (0,0,0)
        self.BrushColor = (0,0,0)


    def paintFigure(self, drawImg):
        drawImg.rectangle((self.startPoints[0], self.startPoints[1], self.endPoints[0], self.endPoints[1]), fill=self.BrushColor, outline=self.PenColor)
        return drawImg

    def generateGenom(self, *args):
        self.startPoints = [args[0],args[1]]
        self.endPoints = [args[2],args[3]]
        self.PenColor = (randint(0,255),randint(0,255),randint(0,255))
        self.BrushColor = (randint(0,255),randint(0,255),randint(0,255))
