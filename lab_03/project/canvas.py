from PyQt5 import QtWidgets, QtGui

class Canvas(QtWidgets.QWidget):

    def __init__(self, parent, sizeLabel):

        super().__init__(parent)

        self.painter = QtGui.QPainter()

        self.lineColor = None
        self.canvasColor = None

        self.setLineColor()
        self.setCanvasColor()

        self.lines = []
        self.spectrs = []
        self.sizeLabel = sizeLabel

    def setLineColor(self, color = QtGui.QColor(0, 0, 0)):
        self.lineColor = color

    def setCanvasColor(self, color = QtGui.QColor(255, 255, 255)):
        self.canvasColor = color

    def setSizeLabel(self):

        width = self.width()
        heigt = self.height()

        self.sizeLabel.setText("Текущий размер: {}, {}".format(width, heigt))

    @staticmethod
    def getQColor(color):
        return QtGui.QColor(color[0], color[1], color[2], color[3])
    
    def paintEvent(self, event: QtGui.QPaintEvent):

        self.setSizeLabel()
        
        self.painter.begin(self)

        self.painter.fillRect(0, 0, self.width(), self.height(), self.canvasColor)

        if self.lines:
            for line in self.lines:
                self.drawLine(line)
                
        if self.spectrs:
            for spectr in self.spectrs:
                self.drawSpectr(spectr)

        self.painter.end()

    def drawSpectr(self, spectr:list):

        for line in spectr:
            self.drawLine(line)

    def drawLine(self, points: list):

        if points[-1] == "libFunc":

            color = self.canvasColor
            self.painter.setPen(QtGui.QPen(color, 1))

            self.painter.drawLine(points[0][0], points[0][1],
                                  points[1][0], points[1][1])

            color = self.getQColor(points[2])
            self.painter.setPen(QtGui.QPen(color, 1))

            self.painter.drawLine(points[0][0], points[0][1],
                                  points[1][0], points[1][1])
            
        else:
            for point in points:
                color = self.canvasColor
                self.painter.setPen(QtGui.QPen(color, 1))
                
                self.painter.drawPoint(point[0], point[1])


                color = self.getQColor(point[2])
                print(point[2], color.getRgb())
                self.painter.setPen(QtGui.QPen(color, 1))
                
                self.painter.drawPoint(point[0], point[1])

    def clean(self):

        self.setLineColor()
        self.setCanvasColor()
        
        self.lines = []
        self.spectrs = []

        self.update()
