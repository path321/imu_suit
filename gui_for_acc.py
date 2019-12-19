import numpy as np
from time import sleep,clock
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph as pg
import sys

from connect_IMU import *
from various_func import appendData

UiName = 'windowQt_2.ui' # Put the name of respective .ui file (QtDesigner)

def lowPass(now,prev,a):
    return (a*now + (1-a)*prev)

def lowPass2(now,prev,prev2):
    return (0.7*now + 0.2*prev+ 0.1*prev2)


class MyGraph(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
        
        pg.setConfigOption('background', 'w')
        super(MyGraph,self).__init__(parent)
        uic.loadUi(UiName,self) # load Qt window
        
        
        self.mainPlot.plotItem.showGrid(True,True);
        self.mainPlot.setLabel('left','X',color='red',size=50);
        self.mainPlot.setLabel('bottom','samples',color='red',size=50);

        numOfPoints = 500 #Graph points
        self.hrz = np.arange(numOfPoints) # abscissa
        self.vrt = np.zeros([3,numOfPoints]) # ordinate
        self.inpt = IMU_Data()

        self.preVal=0
        self.nowVal=0
        self.fltVal=0
        self.fltVal2=0
            
    def updateGraph(self):
        #t1=clock()
        
        self.inpt.readSerial() #Read new values from IMU
        values2print=[self.inpt.getAcc(),self.inpt.getGyro()]  # or self.inpt.getAccRaw(),self.inpt.getGyroRaw() for 16-bit value

        
        self.prevVal=self.nowVal
        self.nowVal=values2print[0][0]
        a=0.7
        self.fltVal=lowPass(self.nowVal,self.fltVal,a)
        self.fltVal2=lowPass2(values2print[0][0],self.vrt[2][-1],self.vrt[2][-2])
        
        
        self.vrt[0] = appendData(self.vrt[0],self.nowVal) #  Update graph line
        self.vrt[1] = appendData(self.vrt[1],self.fltVal)
        self.vrt[2] = appendData(self.vrt[2],self.fltVal2)  

        penList = ['r','g','b']

        pen1 = pg.mkPen(color=(255, 0, 0), width=3, style=QtCore.Qt.SolidLine)
        pen2 = pg.mkPen(color=(0, 0, 255), width=3, style=QtCore.Qt.SolidLine)
        pen3 = pg.mkPen(color=(0, 200, 0), width=2, style=QtCore.Qt.DashLine)
            
        self.mainPlot.plot(self.hrz,self.vrt[0],pen=pen1,clear=True) #Plot graph
        self.mainPlot.plot(self.hrz,self.vrt[1],pen=pen2,clear=False)
        self.mainPlot.plot(self.hrz,self.vrt[2],pen=pen3,clear=False)
        
            
        #print("updateGraph took %.01f ms"%((clock()-t1)*1000)) #Uncomment for plot speed check

        QtCore.QTimer.singleShot(1, self.updateGraph) #quckly update plot


def main():

    app = QtWidgets.QApplication(sys.argv)
   
    form = MyGraph()
    form.show()
    form.updateGraph()
    
    app.exec_()


if __name__ == '__main__':
    main()







    
