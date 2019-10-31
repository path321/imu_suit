import serial
import numpy as np
import sys

baudrate_user = 9600
port = "/dev/ttyACM0" #Port name , check before running .py script
MAX_VAL = int('0xffff',16)//2 #Maximum 16-bit value
GYRO_LIMIT = 250 
ACC_LIMIT = 2

try:
    arduino = serial.Serial(port,timeout=1, baudrate = baudrate_user)
except:
    #Common problems : Different port name, .ino sketch not uploaded
    print("Check the port connection")
    sys.exit()
    

class IMU_Data:
    # Organize data from IMU
    def __init__(self,dataInit = np.zeros(7)):

        #Calibrate offset values, taken from results of calibrate_IMU.py
        self.accX_offset = -935
        self.accY_offset = 6972
        self.accZ_offset = 3919
        self.tmpr_offset = 2200 #Heurestic
        self.gyX_offset = -1957
        self.gyY_offset = 669
        self.gyZ_offset = 83

        #Initialize values
        self.accX = dataInit[0] 
        self.accY = dataInit[1] 
        self.accZ = dataInit[2] 
        self.tmpr = dataInit[3]  
        self.gyX = dataInit[4] 
        self.gyY = dataInit[5] 
        self.gyZ = dataInit[6] 

        self.rawValue = dataInit


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

    def linearMap(self,value,newMax,newMin,oldMax,oldMin):  #Map values to new limits
        return (value-oldMin)*(newMax-newMin)/(oldMax-oldMin)+newMin

    def getAccRaw(self): #Accelerometer values after offset correction
        
        self.accX = self.rawValue[0] + self.accX_offset
        self.accY = self.rawValue[1] + self.accY_offset
        self.accZ = self.rawValue[2] + self.accZ_offset
        return np.array([self.accX, self.accY, self.accZ])
        
    def getAcc(self): #Accelerometer values after offset correction, in degrees/s
        
        values = self.getAccRaw()
        values = values / 16394 # <==> (value + 32767)*(2-(-2))/(32767-(-32767))-2
        
        #For different limits, change variable ACC_LIMIT at start and uncomment region below instead
##    
##        for i in range(3):
##            values[i] = self.linearMap(values[i],ACC_LIMIT,-ACC_LIMIT,MAX_VAL,-MAX_VAL)
        return values

    def getTmprRaw(self): #Temperature values after offset correction
        
        self.tmpr = (self.rawValue[3] + self.tmpr_offset)
        return np.array([self.tmpr])

    def getTmpr(self): #Temperature values after offset correction, in Celsius

        value = self.getTmprRaw() 
        value = self.linearMap(value,85,-40,MAX_VAL,-MAX_VAL)
        return value
        
    def getGyroRaw(self): #Gyroscope values after offset correction
        
        self.gyX = self.rawValue[4] + self.gyX_offset
        self.gyY = self.rawValue[5] + self.gyY_offset
        self.gyZ = self.rawValue[6] + self.gyZ_offset
        return np.array([self.gyX, self.gyY, self.gyZ])

    def getGyro(self): #Gyroscope values after offset correction, in g
        
        values = self.getGyroRaw()
        values = values / 131 # <==> (value + 32767)*(250-(-250))/(32767-(-32767))-250

        #For different limits, change variable GYRO_LIMIT at start and uncomment region below
##        
##        for i in range(3):
##            values[i] = self.linearMap(values[i],GYRO_LIMIT,-GYRO_LIMIT,MAX_VAL,-MAX_VAL)
        return values

    def getRawValues(self): #IMU values, without offset correction
        return np.array(self.rawValue)

    
        
    
