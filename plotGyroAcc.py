import numpy as np
from time import sleep,clock
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph as pg
import sys

import connect_IMU

UiName = 'windowQt.ui' # Put the name of respective .ui file (QtDesigner)

class MyGraph_3_2(QtWidgets.QMainWindow):

    def __init__(self,axisInfo,parent=None):
        
        pg.setConfigOption('background', 'w')
        super(MyGraph_3_2,self).__init__(parent)
        uic.loadUi(UiName,self) # load Qt window
        self.listPlot=[self.myplot_1,self.myplot_2,self.myplot_3,self.myplot_4,self.myplot_5,self.myplot_6]

        for i in range(6):  #Config plot
            self.listPlot[i].plotItem.showGrid(True, True)
            self.listPlot[i].setLabel('left', axisInfo[i%3][0] , color=axisInfo[i%3][1], size=50)
            self.listPlot[i].setLabel('bottom', 'samples' , color=axisInfo[i%3][1], size=50)
            
        numOfPoints = 500 #Graph points
        self.hrz = np.arange(numOfPoints)
        self.vrt = np.zeros([6,numOfPoints])
        self.numOfPoints=numOfPoints
        self.inpt = connect_IMU.IMU_Data()
        self.values=[None for i in range(6)]
        self.axisInfo=axisInfo
        
    def appendData(self,myList,val): #Update the graph line with new data
        
        myList=np.append(myList,val)
        myList=myList[-self.numOfPoints:]
        return myList
    
    def updateGraph(self):
        #t1=clock()
        
        self.inpt.readSerial() #Read new values from IMU
        
        self.values[:3] =  self.inpt.getAcc() # or self.inpt.getAccRaw() for 16-bit value
        self.values[3:] =  self.inpt.getGyro() #self.inpt.getGyroRaw() for 16-bit value

        for i in range(6):
            self.vrt[i] = self.appendData(self.vrt[i],self.values[i]) #  Update graph line
    
        penList = ['r','g','b']

        if self.chkbox.isChecked():
            for i in range(6):
                self.listPlot[i].plot(self.hrz,self.vrt[i],pen=self.axisInfo[i%3][1][0],clear=True)
            self.lcdNumber.display(self.inpt.getTmpr())


        #print("updateGraph took %.01f ms"%((clock()-t1)*1000)) #Uncomment for plot speed check

        QtCore.QTimer.singleShot(1, self.updateGraph) #quckly update plot


        
            
def main():

    axisConf=[['X','red'],['Y','green'],['Z','blue']] #Settings for plot axes

    app = QtWidgets.QApplication(sys.argv)
   
    form = MyGraph_3_2(axisConf)
    form.show()
    form.updateGraph()
    
    app.exec_()


if __name__ == '__main__':
    main()





    
