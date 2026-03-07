import time
import math
import json
import threading
import board
import busio
from adafruit_pca9685 import PCA9685
from servo import Servo

class Balancer:
    def __init__(self, channel1 = 13, channel2 = 14, channel3 = 15):
        print("Starting balancer...")
        self.pwm = PCA9685(busio.I2C(board.SCL, board.SDA))
        self.pwm.frequency = 50
        self.servoOffsets = []

        with open("config.json", "r") as f:
            config = json.load(f)

        self.servoOffsets = [config[f"servo{i+1}offset"] for i in range(3)]
        print(self.servoOffsets)

        self.servo1 = Servo(channel1, self.servoOffsets[0], self.pwm) #setting default offsets
        self.servo2 = Servo(channel2, self.servoOffsets[1], self.pwm)
        self.servo3 = Servo(channel3, self.servoOffsets[2], self.pwm)
        self.servos = [self.servo1, self.servo2, self.servo3]

        self.setAngles([60,60,60])
        time.sleep(1)
        self.home()

        self.lock = threading.Lock()
        with self.lock:
            self.coordinates = None


    def setAngles(self, angles):
        servos = [self.servo1, self.servo2, self.servo3]
        for servo, angle in zip(servos, angles): #associate each servo with each angle
            servo.setAngle(angle)

    def setAngle(self, servoNumber, angle):
        servo = [self.servo1, self.servo2, self.servo3][servoNumber - 1]
        servo.setAngle(angle)

    def sweepServo(self, servoNumber, startAngle, endAngle, stepAngle, toStart=False, delay=0.01): #ooh default parameters
        servo = [self.servo1, self.servo2, self.servo3][servoNumber - 1]
        servo.sweep(startAngle, endAngle, stepAngle, toStart, delay)

    def sweepAll(self, startAngle, endAngle, stepAngle, toStart=False, delay=0.01): #should probaly wrap setAll and sweepAll into the single arguement functions
        self.sweepServo(1, startAngle, endAngle, stepAngle, toStart, delay)
        self.sweepServo(2, startAngle, endAngle, stepAngle, toStart, delay)
        self.sweepServo(3, startAngle, endAngle, stepAngle, toStart, delay)

    def home(self,delay=1): #going to the mathematical home position
        pass

    def manualControl(self): #send manual control commands
        while True:
            motor = int(input("Enter motor number (1-3): "))
            angle = int(input("Enter angle (-180 to 180): "))
            self.setAngle(motor, angle)

    def waveMotion(self, duration=10, steps=100, amplitude=45, offsets=[0, 0, 0]): #sine wave :]
        startTime = time.time()
        servos = [self.servo1, self.servo2, self.servo3]
        while time.time() - startTime < duration:
            for i in range(steps):
                t = i / steps * 2 * math.pi
                angles = [
                    offsets[0] + amplitude * math.sin(t),
                    offsets[1] + amplitude * math.sin(t + 2 * math.pi / 3),
                    offsets[2] + amplitude * math.sin(t + 4 * math.pi / 3)
                ]
                self.setAngles(angles)
                time.sleep(0.02)

    def idle(self):
        while True:
            time.sleep(0.01)
            print("Idling")

    def balance(self,hz=50): #main control loop
       pass

if __name__ == "__main__":
    balancer = Balancer()
    balancer.home()
    balancer.balance()