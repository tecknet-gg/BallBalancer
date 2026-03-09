from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import threading
import time
from cv import BallTracker


class Camera:
    def __init__(self, shared, captureSize=(720, 720), fps=10, host='0.0.0.0', port=5000):
        self.cameraThread = None
        self.camera = None
        self.shared = shared
        self.captureSize = captureSize
        self.fps = fps
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self._server_started = threading.Event()

    def startStream(self):
        self.camera = Picamera2()
        config = self.camera.create_preview_configuration(main={"size": self.captureSize})
        self.camera.configure(config)
        self.camera.start()
        tracker = BallTracker()

        delay = 1 / self.fps

        self.shared["currentCoordinates"] = None
        self.shared["previousCoordinates"] = None

        def generateFrames():
            pass


if __name__ == "__main__":
    shared = {}
    camera = Camera(shared, captureSize=(1280, 720), fps=10)
    thread, cam = camera.startStream()
    print("Camera, whoo!")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Quitting.")