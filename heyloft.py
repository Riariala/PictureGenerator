#ьб пригодится потом
import sys
import random
from tkinter import *
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush

class Individ():
     
    def __init__(self):
        self.genom = []
        self.fit = 0
        self.attraction = 0

    def changeAttraction(val):
       self.attraction = val

class DrawCanvas(QWidget):

    def __init__(self):
        super().__init__()
        self.canvSizeX = 1000
        self.canvSizeY = 700
        self.diapason = 0
        self.root = Tk()
        self.root.title("Визуал")
        self.root.geometry("1350x700")
        self.readyB = Button(text="Готово", background="#000", foreground="#fff", padx="75", pady="8", font="16")
        self.prevPicB = Button(text="", background="#000", foreground="#fff", padx="5", pady="75", font="16")
        self.nextPicB = Button(text="", background="#000", foreground="#fff", padx="5", pady="75", font="16")
        self.qp = QPainter()
        #self.ready.place(x=600, y=820)
        #root.mainloop()

    def mainMenu(self):
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        self.qp.setPen(col)
        self.qp.setBrush(QColor(255, 80, 0, 160))
        self.qp.drawRect(130, 15, 90, 60)

    def drawing(self):
        #canvas = Canvas(self.root, width=self.canvSizeX, height=self.canvSizeY)
        #canvas.create_oval(50, 50, 50+30, 50+30, fill='aqua')
        self.readyB.place(x=1100, y=600)
        self.prevPicB.place(x=10, y=200)
        self.nextPicB.place(x=1030, y=200)
        self.mainMenu()
        #self.btn.pack()
        self.root.update()
        self.root.mainloop()



if __name__ == '__main__':
    DrawCanvas().drawing()
    #root = Tk()
    #root.title("GUI на Python")
    #root.geometry("1350x600")
    #DrawCanvas(root).
    #app = QApplication(sys.argv)
    #ex = Example()
    #sys.exit(app.exec_())
