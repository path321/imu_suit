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

    # Median value => "Cancel" outliers + converge 
    # to mean value for large sample size
    np.median(data,axis=0 , out=calbVal)     

    print("Calibration finished\n")
    
    s="""\nCalibration offset values for %d samples:
              Acc X : %d
              Acc Y : %d
              Acc Z : %d
              Gyro X  : %d
              Gyro Y  : %d
              Gyro Z  : %d\n\n"""

    out = [-calbVal[0],-calbVal[1],(MAX_VAL/ACC_LIMIT - calbVal[2]),-calbVal[4],-calbVal[5],-calbVal[6]]
    print(s % (numOfSamples,out[0],out[1],out[2],out[3],out[4],out[5]))

    while(True):
        ans=input("Save to file y/n ?  ")
        if(ans=='y'):
            print("New values passed to calibration file")
            np.savetxt("calib_values.txt",out,fmt="%d")
            break
        elif(ans=='n'):
            print("Old values kept, new values not passed to calibration file")
            break
        else:
            print("Wrong input, answer with 'y' or 'n'")

        
    


if __name__ == '__main__':
    main()
