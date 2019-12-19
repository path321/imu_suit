#include<Wire.h>

const int MPU=0x68; // SIGNAL_PATH_RESET 
const int ACCEL_CONFIG = 0x1C;
const int GYRO_CONFIG = 0x1B;

int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;
double pitch,roll;
int baudrate = 9600;


void setup(){

Wire.begin();
Wire.beginTransmission(MPU);
Wire.write(0x6B);
Wire.write(0); //Reset the device
Wire.endTransmission(true);

//{Range:REG_VAL} g: 2:0x00, 4:0x08, 8:0x10, 16:0x18
Wire.beginTransmission(MPU);
Wire.write(ACCEL_CONFIG);
Wire.write(0x08);
Wire.endTransmission(true);

//{Range:REG_VAL} rad/s: 250:0x00 500:0x08 1000:0x10 2000:0x18
Wire.beginTransmission(MPU);
Wire.write(GYRO_CONFIG);
Wire.write(0x08);
Wire.endTransmission(true);



Serial.begin(baudrate);

}

void loop(){

Wire.beginTransmission(MPU);
//Start reading from ACCEL_COUT_H register
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
