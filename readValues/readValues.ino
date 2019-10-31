#include<Wire.h>

const int MPU=0x68;
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;
double pitch,roll;
int baudrate = 9600;


void setup(){

Wire.begin();
Wire.beginTransmission(MPU);
Wire.write(0x6B);
Wire.write(0);
Wire.endTransmission(true);
Serial.begin(baudrate);

}

void loop(){

Wire.beginTransmission(MPU);
Wire.write(0x3B);
Wire.endTransmission(false);
Wire.requestFrom(MPU,14,true);


//read accel data
AcX=(Wire.read()<<8|Wire.read()) ;
AcY=(Wire.read()<<8|Wire.read()) ;
AcZ=(Wire.read()<<8|Wire.read());

//read temperature data
Tmp=(Wire.read()<<8|Wire.read()) ;

//read gyro data
GyX=(Wire.read()<<8|Wire.read()) ;
GyY=(Wire.read()<<8|Wire.read()) ;
GyZ=(Wire.read()<<8|Wire.read()) ;

//send the data out the serial port
Serial.println('S'); // 'Start' character
Serial.println(AcX);
Serial.println(AcY);
Serial.println(AcZ);
Serial.println(Tmp);
Serial.println(GyX);
Serial.println(GyY);
Serial.println(GyZ);

//delay(333);

}
