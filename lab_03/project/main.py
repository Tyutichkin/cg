from PyQt5 import QtGui, QtWidgets, uic
import sys
import algorithms as alg
import matplotlib
import matplotlib.pyplot as plt
import time

from canvas import Canvas

matplotlib.use("Qt5Agg")

class UI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # download all the components
        uic.loadUi("main.ui", self)
        
        # set canvas state
        self.canvas = Canvas(self.widget, self.sizeLabel)
        self.gridLayout_6.addWidget(self.canvas, 1, 2, 7, 2)

        # connect buttons for drawing
        self.lineBut.clicked.connect(self.makeLine)
        self.spectrBut.clicked.connect(self.makeSpectr)

        # connect buttons for comparison
        self.stepBut.clicked.connect(self.stepCompare)
        self.timeBut.clicked.connect(self.timeCompare)
        
        # connect button for canvas cleaning
        self.cleanCanvasBut.clicked.connect(self.cleanCanvas)

        self.canvasColorBut.clicked.connect(self.getCanvasColor)
        self.lineColorBut.clicked.connect(self.getLineColor)

        self.cancelBut.clicked.connect(self.cancelAct)

        # trigger information
        self.exitAct.triggered.connect(self.exitProgram)
        self.progAct.triggered.connect(self.printProgInfo)
        self.authorAct.triggered.connect(self.printAuthorInfo)
    
        # list of actions
        self.actions = []
        self.show()

    @staticmethod
    def printProgInfo():
        text = "Алгоритмы построения отрезков.\n\n" \
       "Реализовать возможность построения " \
       "отрезков методами Брезенхема, Ву, ЦДА, " \
       "построение пучка отрезков и " \
       "сравнение времени и ступенчатости."
        
        msg = MessageBox("О программе",
                         text,
                         QtWidgets.QMessageBox.Information)
        
        msg.show()

    @staticmethod
    def printAuthorInfo():
        text = "Тютичкин Семен\nИУ7-45Б"
        msg = MessageBox("Об авторе",
                         text,
                         QtWidgets.QMessageBox.Information)
        
        msg.show()

    @staticmethod
    def exitProgram():
        sys.exit()

    # cancel all performed actions
    def cancelAct(self):

        if not len(self.actions):
            text = "Достигнуто исходное состояние!"
            msg = MessageBox("Предупреждение",
                             text,
                             QtWidgets.QMessageBox.Warning)
            
            msg.show()
        
            return

        if self.actions.pop() == "line":
            self.canvas.lines.pop()
        else:
            self.canvas.spectrs.pop()

        self.canvas.update()

    # get whole information to build a line
    def makeLine(self):

        begPoint, endPoint = self.getCoords()
        curAlgorithm = self.getAlgorithm()

        if begPoint and endPoint and curAlgorithm is not None:
            lineColor = (self.canvas.lineColor.getRgb()[0],
                        self.canvas.lineColor.getRgb()[1],
                        self.canvas.lineColor.getRgb()[2])

            line = alg.drawLine(curAlgorithm,
                                  begPoint,
                                  endPoint,
                                  lineColor)
            
            self.canvas.lines.append(line)
            self.actions.append("line")
            
        self.canvas.update() 

    # get whole information to build a spectr
    def makeSpectr(self):
        
        begPoint = self.getCoord()
        stepAngle = self.getAngle()
        curLen = self.getLength()
        curAlgorithm = self.getAlgorithm()

        spectr = []

        if begPoint and stepAngle and curLen and curAlgorithm is not None:
            
            lineColor = (self.canvas.lineColor.getRgb()[0],
                        self.canvas.lineColor.getRgb()[1],
                        self.canvas.lineColor.getRgb()[2])
            
            stepAngle = alg.getRadians(stepAngle)
            curAngle = 0

            while (curAngle < 2 * alg.PI):

                endPoint = [begPoint[0] + alg.getCos(curAngle) * curLen,
                            begPoint[1] + alg.getSin(curAngle) * curLen]

                line = alg.drawLine(curAlgorithm,
                                    begPoint,
                                    endPoint,
                                    lineColor)
                
                curAngle += stepAngle
                
                spectr.append(line)
                
            self.canvas.spectrs.append(spectr)
            self.actions.append("spectr")

        self.canvas.update()        

    # get angle value
    def getAngle(self):

        angle = self.angleEdit.text()

        if not len(angle):
            text = "Поле \"Угол поворота\" пустое!"
            msg = MessageBox("Ошибка",
                              text,
                              QtWidgets.QMessageBox.Critical)
        
            msg.show()

            return None

        try:
            angle = float(angle)
        except:
            text = "Некорректные данные для угла!"
            msg = MessageBox("Ошибка",
                              text,
                              QtWidgets.QMessageBox.Critical)
        
            msg.show()

            return None

        if not (0 < angle <= 360):
            text = "Значение угла должно быть в пределах (0; 360]!"
            msg = MessageBox("Ошибка",
                              text,
                              QtWidgets.QMessageBox.Critical)
        
            msg.show()

            return None

        return angle
    
    # get length value
    def getLength(self):

        length = self.lenEdit.text()

        if not len(length):
            text = "Поле \"Длина отрезка\" пустое!"
            msg = MessageBox("Ошибка",
                              text,
                              QtWidgets.QMessageBox.Critical)
        
            msg.show()

            return None

        try:
            length = float(length)
        except:
            text = "Некорректные данные для длины отрезка"
            msg = MessageBox("Ошибка",
                              text,
                              QtWidgets.QMessageBox.Critical)
        
            msg.show()

            return None
        
        if (length <= 0):
            text = "Длина отрезка должна быть больше 0."
            msg = MessageBox("Ошибка",
                              text,
                              QtWidgets.QMessageBox.Critical)
        
            msg.show()

            return None

        return length

    # get name of current algorithm
    def getAlgorithm(self):
        return self.algBox.currentIndex()
    
    # get center point for spectr
    def getCoord(self):

        x0Value = self.x0Edit.text()
        y0Value = self.y0Edit.text()

        if not (len(x0Value) and len(y0Value)):
            text = "Отсутствуют данные для центра спектра!"

            msg = MessageBox("Ошибка",
                             text,
                             QtWidgets.QMessageBox.Critical)
            msg.show()

            return None

        try:
            x0Value = float(x0Value)
            y0Value = float(y0Value)
        except:
            text = "Некорректные данные для центра спектра!"

            msg = MessageBox("Ошибка",
                             text,
                             QtWidgets.QMessageBox.Critical)
            msg.show()

            return None
        
        return [x0Value, y0Value]

    # get start and finish coords of the line
    def getCoords(self): 

        x1Value = self.x1Edit.text()
        y1Value = self.y1Edit.text()

        if not (len(x1Value) and len(y1Value)):
            text = "Отсутствуют данные для начальной координаты!"

            msg = MessageBox("Ошибка",
                             text,
                             QtWidgets.QMessageBox.Critical)
            msg.show()

            return None, None

        try:
            x1Value = float(x1Value)
            y1Value = float(y1Value)
        except:
            text = "Некорректные данные начальной координаты!"

            msg = MessageBox("Ошибка",
                             text,
                             QtWidgets.QMessageBox.Critical)
            msg.show()

            return None, None
        
        x2Value = self.x2Edit.text()
        y2Value = self.y2Edit.text()

        if not (len(x2Value) and len(y2Value)):
            text = "Отсутствуют данные для конечной координаты!"

            msg = MessageBox("Ошибка",
                             text,
                             QtWidgets.QMessageBox.Critical)
            msg.show()

            return None, None

        try:
            x2Value = float(x2Value)
            y2Value = float(y2Value)
        except:
            text = "Некорректные данные конечной координаты!"

            msg = MessageBox("Ошибка",
                             text,
                             QtWidgets.QMessageBox.Critical)
            msg.show()

            return None, None
        
        return [x1Value, y1Value], [x2Value, y2Value] 
        
    # get new canvas color
    def getCanvasColor(self):

        color = QtWidgets.QColorDialog.getColor()
        self.canvas.setCanvasColor(color)

        self.setCanvasColorBut(color)

        self.canvas.update()

    # get new line color
    def getLineColor(self):

        color = QtWidgets.QColorDialog.getColor()
        self.canvas.setLineColor(color)

        self.setLineColorBut(color)

        self.canvas.update()

    # set new canvas color
    def setLineColorBut(self, color = QtGui.QColor(0, 0, 0)):

        self.lineColorBut.setStyleSheet("background-color: rgb({}, {}, {});".format(color.getRgb()[0],
                                                                                    color.getRgb()[1],
                                                                                    color.getRgb()[2]))
    # set new canvas color
    def setCanvasColorBut(self, color = QtGui.QColor(255, 255, 255)):

        self.canvasColorBut.setStyleSheet("background-color: rgb({}, {}, {});".format(color.getRgb()[0],
                                                                                      color.getRgb()[1],
                                                                                      color.getRgb()[2]))
        
    def stepCompare(self):
        
        begPoint = self.getCoord()
        curLen = self.getLength()

        if begPoint and curLen:
        
            totalSteps = [[0] for i in range(5)]

            lineColor = (self.canvas.lineColor.getRgb()[0],
                        self.canvas.lineColor.getRgb()[1],
                        self.canvas.lineColor.getRgb()[2])
            
            stepAngle = alg.getRadians(2)
            curAngle = 0

            anglesList = [i for i in range(0, 91, 2)]

            while (curAngle < alg.PI / 2 + 0.01):

                endPoint = [begPoint[0] + alg.getCos(curAngle) * curLen,
                            begPoint[1] + alg.getSin(curAngle) * curLen]

                for i in range(5):
                    curSteps = alg.drawLine(i,
                                            begPoint,
                                            endPoint,
                                            lineColor,
                                            True)
                    
                    totalSteps[i].append(curSteps)
                
                curAngle += stepAngle
            
            totalSteps = [i[1:] for i in totalSteps]
            plt.rcParams['font.size'] = '15'
            plt.figure("Исследование ступенчатости алгоритмов построение.", figsize = (18, 10))

            # plt.subplot(2, 3, 1)
            plt.plot(anglesList, totalSteps[0], label="ЦДА")
            plt.plot(anglesList, totalSteps[1], '*', label="Брензенхем с вещественными коэффицентами")
            plt.plot(anglesList, totalSteps[2], '--', label="Брензенхем с целыми коэффицентами")
            plt.plot(anglesList, totalSteps[3], '.', label="Брензенхем с устр\nступенчатости")
            plt.plot(anglesList, totalSteps[4], '-.', label="By")
            plt.title("Исследование ступенчатости.\n{0} - длина отрезка".format(curLen))
            plt.xticks([i for i in range(0, 91, 5)])
            plt.legend()
            plt.ylabel("Количество ступенек")
            plt.xlabel("Угол в градусах")

            # plt.subplot(2, 3, 2)
            # plt.title("ЦДА")
            # plt.plot(anglesList, totalSteps[0])
            # plt.xticks([i for i in range(0, 91, 5)])
            # plt.ylabel("Количество ступенек")
            # plt.xlabel("Угол в градусах")

            # plt.subplot(2, 3, 3)
            # plt.title("BУ")
            # plt.plot(anglesList, totalSteps[4])
            # plt.xticks([i for i in range(0, 91, 5)])
            # plt.ylabel("Количество ступенек")
            # plt.xlabel("Угол в градусах")

            # plt.subplot(2, 3, 4)
            # plt.title("Брензенхем с действительными коэффицентами")
            # plt.plot(anglesList, totalSteps[1])
            # plt.xticks([i for i in range(0, 91, 5)])
            # plt.ylabel("Количество ступенек")
            # plt.xlabel("Угол в градусах")

            # plt.subplot(2, 3, 5)
            # plt.title("Брензенхем с целыми коэффицентами")
            # plt.plot(anglesList, totalSteps[2])
            # plt.xticks([i for i in range(0, 91, 5)])
            # plt.ylabel("Количество ступенек")
            # plt.xlabel("Угол в градусах")

            # plt.subplot(2, 3, 6)
            # plt.title("Брензенхем с устр. ступенчатости")
            # plt.plot(anglesList, totalSteps[3])
            # plt.xticks([i for i in range(0, 91, 5)])
            # plt.ylabel("Количество ступенек")
            # plt.xlabel("Угол в градусах")

            plt.show()
                

    def timeCompare(self):

        RUNS = 30

        begPoint = self.getCoord()
        stepAngle = self.getAngle()
        curLen = self.getLength()

        timesList = []

        if begPoint and stepAngle and curLen:
            
            lineColor = (self.canvas.lineColor.getRgb()[0],
                        self.canvas.lineColor.getRgb()[1],
                        self.canvas.lineColor.getRgb()[2])
            
            stepAngle = alg.getRadians(stepAngle)
            
            for i in range(6):
                startTime = 0
                endTime = 0
               
                for _ in range(RUNS):
                    curAngle = 0

                    while (curAngle < 2 * alg.PI):

                        endPoint = [begPoint[0] + alg.getCos(curAngle) * curLen,
                                    begPoint[1] + alg.getSin(curAngle) * curLen]

                        startTime += time.time()
                        line = alg.drawLine(i,
                                            begPoint,
                                            endPoint,
                                            lineColor)
                        endTime += time.time()
                        
                        curAngle += stepAngle
                        
                timesList.append((endTime - startTime) / RUNS)

            plt.figure(figsize = (10, 6))
            plt.rcParams['font.size'] = '15'
            plt.title("Замеры времени для построения спектров различными методами")

            positions = [i for i in range(6)]
            methods = ["ЦДА", "Брезенхем\n(float)", "Брезенхем\n(int)",
                    "Брезенхем\n(с устранением\n ступенчатости)", "Ву", "Библиотечная\nфункция"]

            plt.xticks(positions, methods)
            plt.ylabel("Время")

            plt.bar(positions, timesList, align = "center", alpha = 1)

            plt.show()
            

    def cleanCanvas(self):

        self.setLineColorBut()
        self.setCanvasColorBut()
        
        self.canvas.clean()

class MessageBox(QtWidgets.QMessageBox):

    def __init__(self, title, text, icon):
        super().__init__()

        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(icon)
        self.setFont(QtGui.QFont("Ubuntu", 15))
        self.setGeometry(300, 300, 500, 500)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)

    def show(self):
        x = self.exec_()

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    app.exec_()