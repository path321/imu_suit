import numpy as np
from time import clock,sleep
import connect_IMU
from textwrap import dedent

MAX_VAL = int('0xffff',16)//2

def main():

    numOfSamples = 1000
    values=np.zeros(7)
    testCal=connect_IMU.IMU_Data()

    print("Please place IMU still on a flat surface, Z facing up")
    sleep(3)
    print("Calibration starting...")
    
    sumVal=np.zeros(7)
    
    for i in range(numOfSamples):
        testCal.readSerial(True)
        values = testCal.getRawValues()
        sumVal = sumVal + values #element-wise addition, because of Numpy arrays
        
    mean = sumVal / numOfSamples

    print("Calibration finished\n")
    
    s="""\nCalibration offset values for %d samples:
              Acc X : %d
              Acc Y : %d
              Acc Z : %d
              Gyro X  : %d
              Gyro Y  : %d
              Gyro Z  : %d"""
    
    print(s % (numOfSamples,-mean[0],-mean[1],-(MAX_VAL/2 - mean[2]),-mean[4],-mean[5],-mean[6]))


if __name__ == '__main__':
    main()
