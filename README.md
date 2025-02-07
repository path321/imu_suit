## IMU Suit

A graphical interface for exploring MPU-6050 capabilities and generally IMUs performance, through data plot and 
data processing algorithms

Written in Python 3.5

#### Used in project: 
- 6 DoF IMU ( 3-axis gyroscope + 3-axis accelerometer ) MPU-6050
- Arduino board
- PC host

#### Software Requirements:
- Python 3.5+
- Numpy
- PySerial
- PyQt5
- Pyqtgraph
- arduino-cli (Optionally)

#### Instructions:
- Connect IMU pins with Arduino board as follows:

        VCC -> 3.3 V
        GND -> GND
        SCL -> A5
        SDA -> A4
        

- Optionally, run *calibrate_IMU.py*, in order to find offset values for your IMU.

- In case you have arduino-cli installed, *readValues.ino* will be uploaded to Arduino automatically. Else, upload *readValues.ino* manually to board when requested, in order to achieve Arduino - PC connection
 
- Run *IMU_GUI.py* for Accelerometer, Gyroscope and Temperature values from IMU

- Run *rpy.py* for Roll-Pitch-Yaw (Rxyz) values from IMU, as well as Complimentary Filter data fusion


Run and tested in Linux Ubuntu 16


Image from results so far: ![alt text](https://github.com/path321/imu_suit/issues/1) 
