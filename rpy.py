import numpy as np
from time import sleep,clock
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pyqtgraph as pg
import sys
from math import pi,atan2

from connect_IMU import *
from various_func import appendData,lowPass,checkAz

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

        self.inpt.readSerial()
        self.prev_t = self.inpt.timestamp
        self.rpyGyro = self.inpt.getGyro()#*(self.inpt.timestamp - 0 )
        self.accVal_LP = 0
        self.rollAcc = 0
        self.pitchAcc = 0
        self.roll_CF = 0
        self.pitch_CF = 0

        # Plot 1st time for legend to take place
        self.myplot_1.addLegend()
        
        pen1 = pg.mkPen(color=(255, 0, 0), width=2, style=QtCore.Qt.SolidLine)
        pen2 = pg.mkPen(color=(0, 0, 255), width=2, style=QtCore.Qt.SolidLine)
        pen3 = pg.mkPen(color=(0, 200, 0), width=2, style=QtCore.Qt.DashLine)

        self.myplot_1.plot(self.hrz,self.vrt[0], name = "Acc", pen=pen1,clear=True) 
        self.myplot_1.plot(self.hrz,self.vrt[1], name = "Gyro", pen=pen2,clear=False)
        self.myplot_1.plot(self.hrz,self.vrt[2], name = "Compl. Filter", pen=pen3,clear=False)

    def computeAngle(self):
        "Compute roll,pitch from gyro & acc data w/o filtering"

        self.prev_t = self.inpt.timestamp
        self.inpt.readSerial() # Read new values from IMU
        elapsed = self.inpt.timestamp - self.prev_t  # Elapsed time between 2 consecuive readings
        #print(elapsed)

        # roll,pitch from gyro
        gyroVal = self.inpt.getGyro()
        
        self.rpyGyro += gyroVal*elapsed # Indexing:  0:Roll, 1:Pitch, 2:Yaw  
    

        # roll,pitch from accelerometer
        accVal = self.inpt.getAcc()
        
        prevAccVal = self.accVal_LP      
        a_LP = 0.8 # Low Pass filter weight parameter
        self.accVal_LP = lowPass(accVal,prevAccVal,a_LP)
        
        self.rollAcc = atan2(self.accVal_LP[1],self.accVal_LP[2])*180/pi 
        self.pitchAcc = atan2(self.accVal_LP[0],self.accVal_LP[2])*180/pi
        

        # roll,pitch with Complimentary filter
        self.roll_CF += gyroVal[0]*elapsed
        self.pitch_CF += gyroVal[1]*elapsed
        
        a_CF = .85 #0.8 # Complimentary filter weight parameter
        
        self.roll_CF = (1-a_CF)*self.rollAcc + (a_CF)*self.roll_CF
        self.pitch_CF = (1-a_CF)*self.pitchAcc + (a_CF)*self.pitch_CF
        
    
    def updateGraph(self):
        "Plot and update graph"
        #t1=clock()
        
        self.computeAngle()

        self.vrt[0]=appendData(self.vrt[0],self.rollAcc)
        self.vrt[1]=appendData(self.vrt[1],checkAz(self.rpyGyro[0])) #  Update graph line
        self.vrt[2]=appendData(self.vrt[2],checkAz(self.roll_CF))
        self.vrt[3]=appendData(self.vrt[3],self.pitchAcc)
        self.vrt[4]=appendData(self.vrt[4],checkAz(self.rpyGyro[1])) #  Update graph line
        self.vrt[5]=appendData(self.vrt[5],checkAz(self.pitch_CF))
        self.vrt[6]=appendData(self.vrt[6],checkAz(self.rpyGyro[2]))
        
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







    
