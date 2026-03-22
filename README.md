## Overview

A project where I make a cool 3RRS parallel manipulator, and throw a camera underneath and get it to balance a ball. It uses Computer Vision (CV) to locate the ball on the platform, and then the location and velocity vector will be used to calculate the pose of the platform (using Inverse Kinematics) to then push the ball back to the centre. 

I manily made this project since it seemed cool when I saw a couple of people who had made them on YouTube (https://www.youtube.com/watch?v=v4F-cGDGiEw&t=235s), and I (being masochistic), like using PID, so here we are!

The hardware for the most part is done, and the .step file can be found in the hardware folder. Firmware is still in the very early stages, and the balancing software is yet to be written.

<img width="796" height="734" alt="image" src="https://github.com/user-attachments/assets/40b6c01d-f442-48ae-8e6a-e566a7ac4e0d" />

With the custom PCB:

<img width="718" height="670" alt="image" src="https://github.com/user-attachments/assets/cd2735b8-0ac9-483a-8a33-02f9bc2c490b" />


Here's the BOM:

| Component             | Function             | Quantity | Price (unit*qty) | Source                                                                                                                                                                     |
| --------------------- | -------------------- | -------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Raspberry Pi Zero 2 W | Microcontroller      | 1        | £14.15           | https://shop.pimoroni.com/products/raspberry-pi-zero-2-w?variant=42101934587987                                                                                            |
| Pi Camera             | Camera               | 1        | £7               | https://www.amazon.co.uk/dp/B0BZVP3SQW                                                                                                                                     |
| Pi Zero Accessories   | Assorted Accessories | 1        | £8               | https://shop.pimoroni.com/products/zero-adaptor-kit?variant=10462230279 & https://shop.pimoroni.com/products/camera-cable-raspberry-pi-zero-edition?variant=32092803891283 |
| Tie Rod               | Joint                | 10       | £6.99            | https://www.amazon.co.uk/dp/B0DCNGSK9S/?coliid=IMXWIUSGWOUHA&colid=3NYE67N1E05KC&psc=1                                                                                     |
| M3/M4 Assortment      | Strcutural           | ~        | £6.64            | https://amzn.eu/d/07FYMvyj                                                                           |
| DS3218MG              | Servos               | 3        | £29.99           | https://www.amazon.co.uk/dp/B0CY2FVZZM/?coliid=I2RXC2YMY9KN9T&colid=3NYE67N1E05KC&th=1                                                                                     |
| PCA9685               | Servo Driver         | 1        | £4.99            | https://www.amazon.co.uk/dp/B0BKZC1XWR/?coliid=I37WT66U57CC7J&colid=3NYE67N1E05KC&psc=1                                                                                    |
| Power Supply          | Power                | 1        | £16.99           | https://tinyurl.com/2cr9nb7n                                                                                                                                               |
| Shoulder Bolts        | Pin Joints           |          | £4.99            | https://www.amazon.co.uk/dp/B0FDQB24SP?ref=ppx_yo2ov_dt_b_fed_asin_title                                                                                                   |
| PLA                   | Printing Material    | 1        | £13.99           | https://www.amazon.co.uk/dp/B0CD79M1NV?ref=ppx_yo2ov_dt_b_fed_asin_title                                                                                                   |
| 20mm Acrylic Disc     | Platform Disc        | 1        | £3.49            | https://www.amazon.co.uk/dp/B0DJVB82TY/?coliid=I2NBRJSN1CBSC1&colid=3NYE67N1E05KC&psc=1                                                                                    |
| 18AWG Wire            | Wire                 | 2        | £2.90            | https://www.amazon.co.uk/dp/B0CZRGH4CT/?coliid=I36BQ0C4MRSHG2&colid=3NYE67N1E05KC&psc=1                                                                                    |
| PCB             | PCB                 | 5        | £9            | JLCPCB                                                                             |

## Assembly 

You'll want to print out the files under the hardware/compoents directory in the quantities given below:

| Component | Quantity |
| --------- | -------- |
| feet      | 6        |
| standoffs | 6        |
| baseplate | 1        |
| shield    | 1        |
| bottomarm | 3        |
| toparm    | 3        |
| mount     | 3        |
| mountclip | 3        |

With that we start with the base and the feet. For my build, I will add some hotglue to the bottom of the each feet (the side with the smaller radius), to act as a grip. With that, its just a matter of attaching them around the circumference of the base plate. Take care to not atttach them to the holes meant for the standoffs. Use M3x6 or M3x8 screws. They are part of the screw assortment kit in the BOM if you do decide to buy the same. Reference the image below to attach the feet to the correct points.

<img width="796" height="734" alt="image" src="https://github.com/tecknet-gg/BallBalancer/blob/master/images/base%20with%20feet.png" />

With the feet in, you'll want to grab your three servos and place them on the mounts as such:

<img width="796" height="734" alt="image" src="https://github.com/tecknet-gg/BallBalancer/blob/master/images/attaching%20servos.png" />


Attach them using M3x10 bolt with a nut on the other end to clamp it in place. Also ensure you have attached the servo horn using the hardware given in the kit. Alternatively you can use an M3x6 bolt to attach the horn to the servo.

Then grab your six standoffs. Follow the same steps you did for the feet (except the hot glue grip), and attach them around the circumference using M3x8 bolts.

<img width="796" height="734" alt="image" src="https://github.com/tecknet-gg/BallBalancer/blob/master/images/standoffs.png" />


Now with your three bottom arms, line up the two holes on the bottom with the two on the servo horn. Using an M3x6 bolt, attach that too to the horn. You won't need a nut since the servo horn is threaded. 

<img width="796" height="734" alt="image" src="https://github.com/tecknet-gg/BallBalancer/blob/master/images/bottom%20arm.png" />


Grab the three top arms now, and attach them to the bottom arms using the M4 shoulder bolt. If you want you can use a standard M4, but I use a tie rod for my build. Secure it on the other side using a lock-nut. Alternatively you could use two nuts twisted toghther tightly with some pliers.

<img width="796" height="734" alt="image" src="https://github.com/tecknet-gg/BallBalancer/blob/master/images/top%20arm.png" />


Get your tie rods, and attach the to the top of each arm using an M3x6 or M3x8 Bolt.

<img width="796" height="734" alt="image" src="https://github.com/tecknet-gg/BallBalancer/blob/master/images/tierod.png" />


You can now attach the electronics shield part to the standoffs. Just use the same M3x8 bolts and attach the shield to the six standoffs.

<img width="796" height="734" alt="image" src="https://github.com/tecknet-gg/BallBalancer/blob/master/images/shield.png" />


For the next part, my assembly doesn't have the correct compoenent in it since I don't want to redo it since I'm pretty sure I would screw up the joints, and I really don't want to do that again, so read carefully!

The mount you printed should look something like this:

<img width="796" height="734" alt="image" src="https://github.com/tecknet-gg/BallBalancer/blob/master/images/mountpic.png" />


You'll want to grab the M3x20mm bolt, and put it through one of the holes, then attach a nut. Proceed to screw the bolt in, and thread it through one of the tie rods. When it is on the other side of the tie rod, you'll want to add another nut. Then thread it through the other hole of the mount, and out the other end. At this side, you can use another lock nut to attach it securely. Repeat this for the three mounts. Ensure that the extended bit is pointing inwards and not outwards.

Ok now we can start assembling the electronics. Place the Pi Zero 2 W on the corresponding standoffs, and do the same with the PCA9685. No bolts required. Then place the camera module in its little enclosure. Use the attach the CSI cable to the camera, and the other end to the interface on the Pi Zero 2 (note: you'll probably need another cable specifically for the Pi Zero, one with a thinner end for the Pi Zero's CSI slot, as the stock cable with the camera is intended for the full size Pis). With the three main compoenents in, you can start wiring up the PCA9685 using this diagram (in the hardware directory):


<img width="796" height="734" alt="image" src="https://github.com/tecknet-gg/BallBalancer/blob/master/hardware/wiring%20diagram.png" />
You can then attach the three servos to channels 0, 1 and 2 like in the diagram.

Finally for power, get a barrel jack to screw terminal mount, and just hot glue it somewhere onto the bottom. There's not really any mounting pounts on the screw terminal, so and I didn't really want to model in a recess specifically for that. Attach the two 18AWG wires to the screw terminals, and route it up to the PCA9685, and screw the wires into the corresponding screw terminals on the PCA9685. 

And now we can get onto mounting the platform. Grab your clear acrylic disc and the three mount clip parts. Its not on the 3D assembly, but you'll want first put some M3x6 screws through the main mount, then place the platoform in the recess, and get thread the mount clip onto the bolts, then tighten the screws. You shouldn't need a nut here, but if you end up using a longer bolt, you can. Though the piece is threaded so you shouldn't need to.

<img width="796" height="734" alt="image" src="https://github.com/tecknet-gg/BallBalancer/blob/master/images/mountclip.png" />

If you want to add the IMU mount like I will, you can print out the IMU Mount v4 file (x2), and just attach the IMU (MPU6050) to it, and attach it to the platoform as you did mounting the platform to the the top arm mount!

<img width="411" height="264" alt="image" src="https://github.com/user-attachments/assets/a725c66c-b3e7-47ee-85cd-adfd04bc9aca" />


If you happen to be using the PCB, get yourself the board, solder on the DC Barrel Jack, the Pi Zero 2 W and the PCA9685. Then print out the PCB shield instead of the other shield, and mount the PCB on, and voila. Wire up the camera the same. You can wire the IMU into the I2C extender of the PCA9685 in both cases of using the PCB and not.







