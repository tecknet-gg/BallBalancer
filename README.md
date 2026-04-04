## Overview

A project where I make a cool 3RRS parallel manipulator, and throw a camera underneath and get it to balance a ball. It uses Computer Vision (CV) to locate the ball on the platform, and then the location and velocity vector will be used to calculate the pose of the platform (using Inverse Kinematics) to then push the ball back to the centre. 

I manily made this project since it seemed cool when I saw a couple of people who had made them on YouTube (https://www.youtube.com/watch?v=v4F-cGDGiEw&t=235s), and I (being masochistic), like using PID, so here we are!

The hardware for the most part is done, and the .step file can be found in the hardware folder. Firmware is still in the very early stages, and the balancing software is yet to be written.

<img width="796" height="734" alt="image" src="https://github.com/user-attachments/assets/40b6c01d-f442-48ae-8e6a-e566a7ac4e0d" />

With the custom PCB:

<img width="718" height="670" alt="image" src="https://github.com/user-attachments/assets/cd2735b8-0ac9-483a-8a33-02f9bc2c490b" />


