import numpy as np
from time import sleep,clock
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph as pg
import sys


from connect_IMU import *
from various_func import appendData,checkAz

UiName = 'windowQt_2.ui' # Put the name of respective .ui file (QtDesigner)

class MyGraph(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
                
        pg.setConfigOption('background', 'w')
        super(MyGraph,self).__init__(parent)
        uic.loadUi(UiName,self) # load Qt window

        numOfPoints = 500 #Graph points
        listPlot = [self.myplot_1,self.myplot_2,self.myplot_3]
        for i in range(3):
            listPlot[i].plotItem.showGrid(True,True)
            listPlot[i].setLabel('left', 'degrees', color='black', size=50)
            listPlot[i].setLabel('bottom', 'samples', color='black', size=50)
            listPlot[i].setXRange(0, numOfPoints, padding=0.03) # Fixed Axis
            listPlot[i].setYRange(-180, 180, padding=0.08)

            
        self.hrz = np.arange(numOfPoints) # abscissa
        self.vrt = np.zeros([7,numOfPoints]) # ordinate
        self.inpt = IMU_Data()

        # Plot 1st time for legend to take place
        self.myplot_1.addLegend()
        
        pen1 = pg.mkPen(color=(255, 0, 0), width=2, style=QtCore.Qt.SolidLine)
        pen2 = pg.mkPen(color=(0, 0, 255), width=2, style=QtCore.Qt.SolidLine)
        pen3 = pg.mkPen(color=(0, 200, 0), width=2, style=QtCore.Qt.DashLine)

        self.myplot_1.plot(self.hrz,self.vrt[0], name = "Acc", pen=pen1,clear=True) 
        self.myplot_1.plot(self.hrz,self.vrt[1], name = "Gyro", pen=pen2,clear=False)
        self.myplot_1.plot(self.hrz,self.vrt[2], name = "Compl. Filter", pen=pen3,clear=False)
        
    
    def updateGraph(self):
        "Plot and update graph"
        #t1=clock()
        
        self.inpt.computeAngle()

        self.vrt[0]=appendData(self.vrt[0],self.inpt.rpAcc[0])
        self.vrt[1]=appendData(self.vrt[1],checkAz(self.inpt.rpyGyro[0],180)) #  Update graph line
        self.vrt[2]=appendData(self.vrt[2],checkAz(self.inpt.rp_CF[0],180))
        self.vrt[3]=appendData(self.vrt[3],self.inpt.rpAcc[1])
        self.vrt[4]=appendData(self.vrt[4],checkAz(self.inpt.rpyGyro[1],90)) #  Update graph line
        self.vrt[5]=appendData(self.vrt[5],checkAz(self.inpt.rp_CF[1],90))
        self.vrt[6]=appendData(self.vrt[6],checkAz(self.inpt.rpyGyro[2],180))
        
        pen1 = pg.mkPen(color=(255, 0, 0), width=2, style=QtCore.Qt.SolidLine)
        pen2 = pg.mkPen(color=(0, 0, 255), width=2, style=QtCore.Qt.SolidLine)
        pen3 = pg.mkPen(color=(0, 200, 0), width=2, style=QtCore.Qt.DashLine)

        self.myplot_1.plot(self.hrz,self.vrt[0], pen=pen1,clear=True) #Plot graph
        self.myplot_1.plot(self.hrz,self.vrt[1], pen=pen2,clear=False)
        self.myplot_1.plot(self.hrz,self.vrt[2], pen=pen3,clear=False)
        self.myplot_2.plot(self.hrz,self.vrt[3], pen=pen1,clear=True) #Plot graph
        self.myplot_2.plot(self.hrz,self.vrt[4], pen=pen2,clear=False)
        self.myplot_2.plot(self.hrz,self.vrt[5], pen=pen3,clear=False)
        self.myplot_3.plot(self.hrz,self.vrt[6], pen=pen2,clear=True)
        
        #print("updateGraph took %.01f ms"%((clock()-self.t1)*1000)) #Uncomment for plot speed check

        QtCore.QTimer.singleShot(1, self.updateGraph) #quckly update plot


def main():

    app = QtWidgets.QApplication(sys.argv)
   
    form = MyGraph()
    form.show()
    form.updateGraph()
    
    app.exec_()


if __name__ == '__main__':
    main()







    
