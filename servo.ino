#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

const int SERVO_FREQ = 50; // hz
const float MIN_PULSE_MS = 0.5; // pulse at 0
const float MAX_PULSE_MS = 2.5; // pulse at 270
const float MAX_ANGLE = 270.0; // degrees
const float PERIOD_MS = 1000.0 / SERVO_FREQ; // 20 ms
  
const float rangeMaxAngle = 60.0; // set upper constraint
const float rangeMinAngle = 15.0; // set lower constraint
  
float offset13 = 0.0; // offset for callibration
float offset14 = 0.0;
float offset15 = 0.0;
  

int angleToCount(float angle) {
	if (angle < 0) angle = 0; // redundant santiation
	if (angle > MAX_ANGLE) angle = MAX_ANGLE; // redundant santiation
  
	float pulse = MIN_PULSE_MS + (angle / MAX_ANGLE) * (MAX_PULSE_MS - MIN_PULSE_MS);
	int count = int((pulse / PERIOD_MS) * 4096.0);
	return count;
}
  
void setAngle(int channel, float angle) {
	if(angle < rangeMinAngle) angle = 360-angle;
	if(angle > rangeMaxAngle) angle = angle - (int(rangeMaxAngle/angle))*60;
	if(angle == 0) angle = rangeMinAngle;

	if(channel == 13) angle += offset13;
	if(channel == 14) angle += offset14;
	if(channel == 15) angle += offset15;

  
	angle = angleToCount(angle); //gets count
	pwm.setPWM(channel,0,angle); //pushes angle to servo
}

void testLoop() {
	for(int i=0; i<=10; i++) {
		for(int channel=13; channel<=15; channel++) {
			for(float angle=45; angle<=60;angle+=0.5) {
				setAngle(channel,angle);
				delay(1);
			}
			for(float angle=60; angle>=45; angle-=0.5) {
				setAngle(channel,angle);
				delay(1);
			}
			for(float angle=45; angle>=15; angle-=0.5) {
				setAngle(channel,angle);
				delay(1);
			}
			for(float angle=15; angle<=45; angle+=0.5) {
				setAngle(channel,angle);
				delay(1);
			}
			delay(10);
		}
	} 
	setAngle(13,45); #example usage
	setAngle(14,45);
	setAngle(15,45);
}
  
void setup() {

	Serial.begin(9600);
	pwm.begin();
	pwm.setPWMFreq(SERVO_FREQ);
	Serial.println("PCA9685 Servo Test - Channels 13/15");
  
	setAngle(13,45.0);
	setAngle(14,45.0);
	setAngle(15,45.0);
  
	delay(1000);
}
  

void loop() {
	testLoop();
}
