from Genom import _Genom_

class LineGen(_Genom_):
    def __init__(self):
        super().__init__()
        self.BrushColor = 0
        self.width = 0

    def paintFigure(self, drawImg, gens, maxX, maxY):
        self.PenColor = (int(gens[4] * 255), int(gens[5] *255), int(gens[6]*255))
        self.startPoints = [int(gens[0] * maxX), int(gens[1] * maxY)]
        self.endPoints = [int(gens[2] * maxX), int(gens[3] * maxY)]
        self.width = int(gens[7] * 20)
        if self.startPoints[0] > self.endPoints[0]:
            b = self.startPoints[0]
            self.startPoints[0] = self.endPoints[0]
            self.endPoints[0] = b
        if self.startPoints[1] > self.endPoints[1]:
            b = self.startPoints[1]
            self.startPoints[1] = self.endPoints[1]
            self.endPoints[1] = b
        drawImg.line((self.startPoints[0], self.startPoints[1], self.endPoints[0], self.endPoints[1]), fill=self.PenColor, width=self.width)
        return drawImg