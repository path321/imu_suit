import serial
import numpy as np
import sys

from time import time
from math import pi,atan2,sqrt

from various_func import linearMap,runBash,lowPass

MAX_VAL = int('0xffff',16)//2 #Maximum 16-bit value

gyroScaleFactor = {250:131, 500:65.5, 1000:32.8, 2000:16.4} # from datasheet
accScaleFactor = {2:16384, 4:8192, 8:4096, 16:2048}

GYRO_LIMIT = 500
ACC_LIMIT = 4

class ConnectBoard:
    "Connect PC host with Arduino"
    def __init__(self):

        self.__baudrate_user = 9600
        self.__cli_flag=False
        self.__nameIno = 'readValues'
        self.port = None
                
    def checkDependencies(self):
        "Check if needed packages are installed"
        dependList = ['numpy','pyserial','PyQt5','pyqtgraph']
        reqs,foo = runBash("python3 -m pip freeze")
        installed_packages = [r.split('==')[0] for r in reqs.split()]

        for pkg in dependList:
            if not pkg in installed_packages:
                print("%s package not found in host PC. Abort."%(pkg))
                sys.exit()
        
        #Check if 'arduino-cli' is installed on host
        output,error = runBash("which arduino-cli")
        if output!='':
            self.cli_flag=True # arduino-cli is installed, thus will be used below for uploading .ino on board
            # print("'arduino-cli' detected on your PC, using it to upload proper .ino files...")

    def uploadIno(self):
        "Upload .ino file to arduino board"
        if(self.cli_flag):
            out, foo= runBash("arduino-cli board list")
            out=out.split()
            self.port = out[6]
            param_fqbn = out[12]
            
            # Compile sketch
            foo,error = runBash('arduino-cli compile --fqbn '+param_fqbn+' ./'+self.__nameIno+'/') 
            if(error!=''):
                print("Error during compiling sketch with 'arduino-cli', with error :\n",error)
                self.cli_flag=False
            else:
                # Upload sketch
                foo,error = runBash("arduino-cli upload -p "+ self.port +" --fqbn "+ param_fqbn +' ./'+self.__nameIno+'/')
                if(error!=''):
                    print("Error during uploading sketch with 'arduino-cli', with error :\n",error)
                    self.cli_flag=False
                    
        if not self.cli_flag:
            print("Upload readValue.ino sketch and press 'Enter'")
            input()

    def connectSerial(self):
        "Connect serially host - board"
        try:
            ser = serial.Serial(self.port, timeout=1, baudrate = self.__baudrate_user)
        except:
            #Common problems : Different port name, .ino sketch not uploaded
            print("Serial connection failed\nCheck board connection or that .ino uploaded correctly")
            sys.exit()
        else:
            return ser


        

class IMU_Data:
    "Organize data from IMU"
    def __init__(self):

        cnct = ConnectBoard()
        cnct.checkDependencies()
        cnct.uploadIno()
        self.__ser = cnct.connectSerial()

        inpt = np.loadtxt("calib_values.txt",dtype=int) # Load calibration values from respctive txt
        
        #Calibrate offset values, taken from results of calibrate_IMU.py
        self.__accX_offset = inpt[0]
        self.__accY_offset = inpt[1]
        self.__accZ_offset = inpt[2]
        self.__tmpr_offset = 2200 # <-Heurestic
        self.__gyX_offset = inpt[3]
        self.__gyY_offset = inpt[4]
        self.__gyZ_offset = inpt[5]

        #Initialize values
        self.accX = 0 
        self.accY = 0 
        self.accZ = 0
        self.tmpr = 0  
        self.gyX = 0 
        self.gyY = 0 
        self.gyZ = 0 

        self.__num_of_data = 7 # 3 acc + 1 temp + 3 gyro
        
        self.rawValue = np.zeros(self.__num_of_data)

        self.timestamp = 0 
        self.readSerial()
        self.prev_t = self.timestamp
        self.accVal_LP = 0
        self.rpyGyro = self.getGyro() # Indexing:  0:Roll, 1:Pitch, 2:Yaw  
        self.rpAcc = np.zeros(2) # Indexing:  0:Roll, 1:Pitch
        self.rp_CF = np.zeros(2) # Indexing:  0:Roll, 1:Pitch
        
        

    def readSerial(self,silent = False):
        "Read Data from serial input ( Arduino )"
        inpt=[]
        error_in_comm = False
        
        while((self.__ser).read_until().strip()!=b"S"):
            pass
        
        for i in range(self.__num_of_data):
            try:
                inpt.append(float((self.__ser).read_until().strip()))
            except ValueError:
                #if unexpected character comes, try aqcuiring data again from the start
                error_in_comm = True
                if not(silent):print("ValueError occured, try again") 
                break

        if(error_in_comm):
            inpt=self.readSerial() 
        else:
            self.rawValue = inpt #return data
            self.timestamp = self.getTimeNow() # measure for when readSerial is called
    
    def getAccRaw(self): 
        "Accelerometer values after offset correction"
        self.accX = self.rawValue[0] + self.__accX_offset
        self.accY = self.rawValue[1] + self.__accY_offset
        self.accZ = self.rawValue[2] + self.__accZ_offset
        return np.array([self.accX, self.accY, self.accZ])
        
    def getAcc(self):
        "Accelerometer values after offset correction, in degrees/s"
        return self.getAccRaw() / accScaleFactor[ACC_LIMIT]
    
    def getTmprRaw(self):
        "Temperature values after offset correction"
        return np.array([self.rawValue[3] + self.__tmpr_offset])

    def getTmpr(self):
        "Temperature values after offset correction, in Celsius"
        return linearMap(self.getTmprRaw(),85,-40,MAX_VAL,-MAX_VAL)
        
    def getGyroRaw(self):
        "Gyroscope values after offset correction"        
        self.gyX = self.rawValue[4] + self.__gyX_offset
        self.gyY = self.rawValue[5] + self.__gyY_offset
        self.gyZ = self.rawValue[6] + self.__gyZ_offset
        return np.array([self.gyX, self.gyY, self.gyZ])

    def getGyro(self):
        "Gyroscope values after offset correction, in g"
        return self.getGyroRaw() / gyroScaleFactor[GYRO_LIMIT]

    def getRawValues(self):
        "IMU values, without offset correction"
        return np.array(self.rawValue)

    def getTimeNow(self):
        "Return the time in seconds since the epoch"
        return time()

    def computeAngle(self):
        '''Compute roll,pitch from gyro & acc data w/o filtering
        Should be called continuously for correct results'''

        self.prev_t = self.timestamp
        self.readSerial() # Read new values from IMU
        elapsed = self.timestamp - self.prev_t  # Elapsed time between 2 consecuive readings
        #print(elapsed)

        # roll,pitch from gyro
        gyroVal = self.getGyro()
        
        self.rpyGyro += gyroVal*elapsed # Indexing:  0:Roll, 1:Pitch, 2:Yaw  
    

        # roll,pitch from accelerometer
        accVal = self.getAcc()
        
        prevAccVal = self.accVal_LP      
        a_LP = 0.8 # Low Pass filter weight parameter
        self.accVal_LP = lowPass(accVal,prevAccVal,a_LP)
        
        self.rpAcc[0] = atan2(self.accVal_LP[1],self.accVal_LP[2])*180/pi 
        self.rpAcc[1] = atan2(-self.accVal_LP[0],sqrt(self.accVal_LP[1]**2 + self.accVal_LP[2]**2))*180/pi
        

        # roll,pitch with Complimentary filter
        self.rp_CF[0] += gyroVal[0]*elapsed
        self.rp_CF[1] += gyroVal[1]*elapsed
        
        a_CF = 0.95 # Complimentary filter weight parameter
        
        self.rp_CF[0] = (1-a_CF)*self.rpAcc[0] + (a_CF)*self.rp_CF[0]
        self.rp_CF[1] = (1-a_CF)*self.rpAcc[1] + (a_CF)*self.rp_CF[1]
    
    




    

        
    
