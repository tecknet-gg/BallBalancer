import threading

import cv2 as cv
import numpy as np
from picamera2 import Picamera2
import cv2 as cv
import numpy as np
import math
import time


prevCircle = None

class BallTracker:
    def __init__(self,camecoordinates,lock): #provide coordinates and lock for reading variable safely (will be multithreaded)
        self.coordinates = None
        self.cam.configure(self.cam.create_preview_configuration(main={"size": (640, 480)}))
        self.cam.start()
        self.prevCircle = None

        time.sleep(1)
    def locateBall(self, frame): #to call from PID loop
        return self.coordinates,frame
    def dist(self,x1,x2,y1,y2):
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)
    def findCircle(self,frame):
        pass

    def display(self):
        while True:
            frame = self.cam.capture_array()

            greyFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            blurFrame = cv.GaussianBlur(greyFrame, (19, 19), 0)
            circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, dp=1.2, param1=100, minRadius=50, maxRadius=150)
            chosen = None
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for circle in circles[0, :]:
                    if chosen is None:
                        chosen = circle
                    elif prevCircle is not None:
                        #pick whichever circle is closer to previous position
                        if self.dist(circle[0], circle[1], prevCircle[0], prevCircle[1]) < self.dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]):
                            chosen = circle

                if chosen is not None:
                    cv.circle(frame, (chosen[0], chosen[1]), 1, (255, 0, 0), 3)
                    cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (0, 255, 0), 3)
                    prevCircle = (chosen[0], chosen[1])
            else:
                cv.putText(frame, "No ball detected", (30, 50),
                           cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

            cv.imshow("Video", frame)


if __name__ == "__main__":
    coordinates = [None, None]
    lock = threading.Lock()
    tracker = BallTracker(coordinates,lock)
    tracker.display()