# Ball-Balancer

A custom 3RRS parallel manipulator that leverages CV to locate and mainpulate a ball on a 2D planar surface.

## Features:
- Low cost hardware: By leveraging edge computing the CV processing is done on a companion computer. The onboard hardware is a low cost Pi Zero 2. Frames are served over Flask, and data is received by the hardware over UDP.
- Low latency: ~75ms between frame being served and data being received back
- Resilient CV pipeline: Able to work in high noise environments. Uses a variety of techniques and optimisations, such as static and dynamic ROIs (region of interests) to reduce frame size, novel colour based filtering, ensures target is within a pre-defined HSV range to reduce false detections, and an EMA filter to maintain simplicity whilst improving performance.
- Inverse Kinematics: A robust IK class that converts target pose vectors to 3 actuator angles. 
- PID: A PID loop to calculate pose vectors taking the three (P, I & D) paramaters into account, in order to move the ball to the centre, or any arbitrary point on the plane.
- Auto-Callibration: An IMU is sampled to get orientation data, which is then fed into a basic gradient descent algorithm in order to minimise error. Setpoints can be manually defined
- Live config updating: Instead of re-deploying the code every time a paramater is chagned, a companion script running on your laptop pushes PID config paramaters over UDP, so tuning can be done in real-time, streamlining the process.

## Building

If you're interested in building the same, please point yourself towards the BUILD.md file, with comprehensive build instructions.

If you've built it already, and would like to run my firmware, please point yourself towards the FIRMWARE.md file. It serves mainly as a starting point into using my firmware, everything is not entirely documented, but my code is relatively verbose in case you need to tweak things.

If I do get time, I will eventually post this on Instructables!

## Pictures

### Without PCB:

<img width="494" height="480" alt="image" src="https://github.com/user-attachments/assets/bad48d22-7f49-42ad-bd0f-3ec8f8e3387d" />

### With PCB:

<img width="556" height="513" alt="image" src="https://github.com/user-attachments/assets/9ae4e37e-ee97-4a50-8139-41ef3794aa85" />

### My Build:

<img width="1080" height="1920" alt="image" src="https://github.com/user-attachments/assets/5ca1124a-9eb0-4f45-968c-a6496726ac98" />

Still some tuning needed, but the hardware totally works, and it even balances it fully sometimes :]

https://www.youtube.com/shorts/TCPpPW1j67o





