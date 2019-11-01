IMU GUI

A graphical interface for exploring MPU-6050 capabilities and generally IMUs performance, through data plot and 
data processing algorithms

Written in Python 3.5

Used in project: 
- 6 DoF IMU ( 3-axis gyroscope + 3-axis accelerometer ) MPU-6050
- Arduino Uno
- PC host

Software Requirements:
- Python 3.5
- Numpy
- PySerial
- PyQt5
- Pyqtgraph

Instructions:
- Connect IMU pins with Arduino board as follows:

        VCC -> 3.3 V
        GND -> GND
        SCL -> A5
        SDA -> A4
        
- Run readValues.ino to achieve Arduino - PC connections

- Optionally, run calibrate_IMU.py, in order to find offset values for your IMU. 
Then, Copy the values above appropriately to connect_IMU.py 
 
- Run plotGyroAcc.py

Run and tested in Linux Ubuntu 16

The project is currently in progress

![alt text](https://github.com/path321/imu_suit/issues/1#issue-515577957) 
