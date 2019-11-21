import numpy as np
from time import clock,sleep
from connect_IMU import *

MAX_VAL = int('0xffff',16)//2

def main():

    numOfSamples = 300
    inpt=IMU_Data()

    print("Please place IMU still on a flat surface, Z facing up")
    sleep(3)
    print("Calibration starting...")
    
    data=np.zeros((numOfSamples,7))

    for i in range(numOfSamples):
        inpt.readSerial(True)
        data[i]=inpt.getRawValues()
    
    calbVal=np.zeros(7)
    
    np.median(data,axis=0 , out=calbVal) # Median value => "Cancel" outliers + converge to mean value for large sample size
    

    print("Calibration finished\n")
    
    s="""\nCalibration offset values for %d samples:
              Acc X : %d
              Acc Y : %d
              Acc Z : %d
              Gyro X  : %d
              Gyro Y  : %d
              Gyro Z  : %d"""
    
    print(s % (numOfSamples,-calbVal[0],-calbVal[1],(MAX_VAL/2 - calbVal[2]),-calbVal[4],-calbVal[5],-calbVal[6]))


if __name__ == '__main__':
    main()
