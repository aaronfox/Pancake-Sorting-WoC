from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSlot
import sys
 
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.flag = False
        global pancake_size
        pancake_size = [1,2,3,4,5]
        global indexPointer
        indexPointer = 0
        global indexFlips
        indexFlips = [3,3,1]
        self.title = "PyQt5 Drawing Rectangle"

        pybutton = QPushButton('Click me', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,32)
        pybutton.move(50, 50)  
        #self.bottom = 100
        self.top = 0
        self.left = 100
        self.width = 600
        self.height = 500
 
 
        self.InitWindow()
    
    def incrementPointer(self):
        global indexPointer
        indexPointer = indexPointer + 1

    def flip(self):
        global pancake_size
        global indexFlips   
        tempList = []
        
        x = indexFlips[indexPointer]
        print(x)
        #add pancake_size to tempList
        for e in pancake_size:
            tempList.append(e)
        
        #clear pancake_size list
        pancake_size = []

        print(tempList)
        print(pancake_size)

        #add rest of the pancakes before the flip to the end now in reverse order
        f = x
        while f >= 0:
            pancake_size.append(tempList[f])
            f -= 1
        
        print(pancake_size)
        #add to pancake_list including the latest flip
        #for x in tempList:
         #   pancake_size.append(x)
        i = x +1 
        while i < len(tempList):
            pancake_size.append(tempList[i])
            i += 1
        print(pancake_size)



    def clickMethod(self):
        self.flag = True
        print('Clicked Pyqt button.')
        #Gui shows pancakes in order
        self.update()
        #increment the pointer to get next flips
        self.incrementPointer()
        self.flip()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()  
    
    def paintEvent(self, e):
        if(self.flag):
            painter = QPainter(self)
            painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
            #painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
            painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
            j = 0
            x = 500
            #x coord, y coord,width, height
            for  i in pancake_size:
                #use a for loop here
                painter.drawRect(x, j, i*100,50)
                j = j +50
                x = 500 - ((i*100)/2)
            
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())