
import serial
import numpy as np
import sys
import subprocess

from various_func import linearMap

baudrate_user = 9600
MAX_VAL = int('0xffff',16)//2 #Maximum 16-bit value

gyroScaleFactor = {250:131, 500:65.5, 1000:32.8, 2000:16.4} # from datasheet
accScaleFactor = {2:16384, 4:8192, 8:4096, 16:2048}

GYRO_LIMIT = 250 
ACC_LIMIT = 2

# Check which port is connected to board
bashCommand = "ls /dev/ttyA*"
process = subprocess.run(bashCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
output = process.stdout
error = process.stderr
if output != '':
    port = output.strip()
else:
    print("Error in connection, board not found, see error below for debugging:\n\n",error.strip())
    sys.exit()




try:
    arduino = serial.Serial(port,timeout=1, baudrate = baudrate_user)
except:
    #Common problems : Different port name, .ino sketch not uploaded
    print("Serial connection failed\nCheck board connection or that .ino uploaded correctly")
    sys.exit()
class IMU_Data:
    # Organize data from IMU
    def __init__(self):

        inpt = np.loadtxt("calib_values.txt",dtype=int) # Load calibration values from respctive txt
        
        #Calibrate offset values, taken from results of calibrate_IMU.py
        self.accX_offset = inpt[0]
        self.accY_offset = inpt[1]
        self.accZ_offset = inpt[2]
        self.tmpr_offset = 2200 # <-Heurestic
        self.gyX_offset = inpt[3]
        self.gyY_offset = inpt[4]
        self.gyZ_offset = inpt[5]

        #Initialize values
        self.accX = 0 
        self.accY = 0 
        self.accZ = 0
        self.tmpr = 0  
        self.gyX = 0 
        self.gyY = 0 
        self.gyZ = 0 

        self.rawValue = np.zeros(7)

    def readSerial(self,silent = False): # Read Data from serial input ( Arduino )

        inpt=[]
        error_in_comm = False
        
        while(arduino.read_until().strip()!=b"S"):
            pass
        
        for i in range(7):
            try:
                inpt.append(float(arduino.read_until().strip()))
            except ValueError:
                #if unexpected character comes, try aqcuiring data again from the start
                error_in_comm = True
                if not(silent):print("ValueError occured, try again") 
                break

        if(error_in_comm):
            inpt=self.readSerial() 
        else:
            self.rawValue=inpt #return data

    
    def getAccRaw(self): #Accelerometer values after offset correction
        
        self.accX = self.rawValue[0] + self.accX_offset
        self.accY = self.rawValue[1] + self.accY_offset
        self.accZ = self.rawValue[2] + self.accZ_offset
        return np.array([self.accX, self.accY, self.accZ])
        
    def getAcc(self): #Accelerometer values after offset correction, in degrees/s
        return self.getAccRaw() / accScaleFactor[ACC_LIMIT] 
    
    def getTmprRaw(self): #Temperature values after offset correction
        return np.array([self.rawValue[3] + self.tmpr_offset])

    def getTmpr(self): #Temperature values after offset correction, in Celsius
        return linearMap(self.getTmprRaw(),85,-40,MAX_VAL,-MAX_VAL)
        
    def getGyroRaw(self): #Gyroscope values after offset correction
        
        self.gyX = self.rawValue[4] + self.gyX_offset
        self.gyY = self.rawValue[5] + self.gyY_offset
        self.gyZ = self.rawValue[6] + self.gyZ_offset
        return np.array([self.gyX, self.gyY, self.gyZ])

    def getGyro(self): #Gyroscope values after offset correction, in g
        return self.getGyroRaw() / gyroScaleFactor[GYRO_LIMIT]

    def getRawValues(self): #IMU values, without offset correction
        return np.array(self.rawValue)

    
        
    
