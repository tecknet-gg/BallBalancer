A project where I make a cool 3RRS parallel manipulator, and throw a camera underneath and get it to balance a ball. It uses Computer Vision (CV) to locate the ball on the platform, and then the location and velocity vector will be used to calculate the pose of the platform (using Inverse Kinematics) to then push the ball back to the centre. 

I manily made this project since it seemed cool when I saw a couple of people who had made them on YouTube (https://www.youtube.com/watch?v=v4F-cGDGiEw&t=235s), and I (being masochistic), like using PID, so here we are!

The hardware for the most part is done, and the .step file can be found in the hardware folder. Firmware is still in the very early stages, and the balancing software is yet to be written.

<img width="796" height="734" alt="image" src="https://github.com/user-attachments/assets/40b6c01d-f442-48ae-8e6a-e566a7ac4e0d" />

Here's the BOM:

| Component             | Function             | Quantity | Price (unit*qty) | Source                                                                                                                                                                     |
| --------------------- | -------------------- | -------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Raspberry Pi Zero 2 W | Microcontroller      | 1        | £14.15           | https://shop.pimoroni.com/products/raspberry-pi-zero-2-w?variant=42101934587987                                                                                            |
| Pi Camera             | Camera               | 1        | £7               | https://www.amazon.co.uk/dp/B0BZVP3SQW                                                                                                                                     |
| Pi Zero Accessories   | Assorted Accessories | 1        | £8               | https://shop.pimoroni.com/products/zero-adaptor-kit?variant=10462230279 & https://shop.pimoroni.com/products/camera-cable-raspberry-pi-zero-edition?variant=32092803891283 |
| Tie Rod               | Joint                | 10       | £6.99            | https://www.amazon.co.uk/dp/B0DCNGSK9S/?coliid=IMXWIUSGWOUHA&colid=3NYE67N1E05KC&psc=1                                                                                     |
| M3/M4 Assortment      | Strcutural           | ~        | £6.64            | https://www.amazon.co.uk/dp/B0DG2PHL25/?coliid=I26YB3K78HFTZQ&colid=3NYE67N1E05KC&psc=1                                                                                    |
| DS3218MG              | Servos               | 3        | £29.99           | https://www.amazon.co.uk/dp/B0CY2FVZZM/?coliid=I2RXC2YMY9KN9T&colid=3NYE67N1E05KC&th=1                                                                                     |
| PCA9685               | Servo Driver         | 1        | £4.99            | https://www.amazon.co.uk/dp/B0BKZC1XWR/?coliid=I37WT66U57CC7J&colid=3NYE67N1E05KC&psc=1                                                                                    |
| Power Supply          | Power                | 1        | £16.99           | https://tinyurl.com/2cr9nb7n                                                                                                                                               |
| Shoulder Bolts        | Pin Joints           |          | £4.99            | https://www.amazon.co.uk/dp/B0FDQB24SP?ref=ppx_yo2ov_dt_b_fed_asin_title                                                                                                   |
| PLA                   | Printing Material    | 1        | £13.99           | https://www.amazon.co.uk/dp/B0CD79M1NV?ref=ppx_yo2ov_dt_b_fed_asin_title                                                                                                   |
| 20mm Acrylic Disc     | Platform Disc        | 1        | £3.49            | https://www.amazon.co.uk/dp/B0DJVB82TY/?coliid=I2NBRJSN1CBSC1&colid=3NYE67N1E05KC&psc=1                                                                                    |
| 18AWG Wire            | Wire                 | 2        | £2.90            | https://www.amazon.co.uk/dp/B0CZRGH4CT/?coliid=I36BQ0C4MRSHG2&colid=3NYE67N1E05KC&psc=1                                                                                    |

