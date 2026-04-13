The firmware is all written in python (3.13).

## Deploying and Tuning

1. Setup the Pi Zero 2 W for SSH (the setup is a bit convoluted).
2. Create a remote interpreter using your IDE of choice (easiest in PyCharm, but VSCode obviously works too).
3. Install dependencies (check imports)
4. Deploy the code to a tmp directory on the Pi Zero 2 using SSH. 
5. Run the balancer.py script on the platform. Note the IP it starts serving the frames too.
6. Set that as the target IP on the mac.py and configupdater.py scripts.
7. Set the url to to "https://nameofyourpi.local:5000/raw_feed". Example: "https://pizero2.local:5000/raw_feed"
8. In liveconfig.json, set offsets to 0.0 for all three servos. Keep PID values as is, you can tune from there.
9. In cvconfig.json, set hsvLow to [0,0,0], hsvHigh to [255,255,255] and threshold to 0.
10. Redeploy all files.
11. Run the configupdater.py script on your computer (not the balancer). Make sure you're not using the remote interpreter.
12. Run the balancer.py script on the balancer. When the Flask route has finished initialising, run the mac.py script on your computer (lke the configupdater.py).
13. Open the route displayed by the flask intialisation script from the balancer.py script, and append "/raw_stream" to the end to view the camera stream. Similarly, open the route displayed by the the flask intialisation script from the mac.py script and append "processed" to the end to view the processed stream.
14. Redefine the static RoI (region of interest) by tweaking the vertBar and horizBar if needed. If your hardware and camera is the same, it should be fine as is.
15. Rerun the mac.py script.
16. Place a ball in frame and try to achieve a lock on the ball. Try and reduce noise in the frame to achieve this. Look at the HSV readout from the balancer.py script. Set the hsvLow and hsvHigh values in the cvconfig.py script to rougly +/- 40-50 of these values. You can be more strict with this if you like. Set the threshold percentage to ~0.6. That is how much it has to be within range to be accepted. When you have a more consistent lock, tune these values to be more strict. By the end of it, you want a threshold of 0.7 - 0.8 to prevent it from loosing the ball.
17. If you cannot achieve a lock at all, tune the parameters (dp, minDist, param1, param2, minRadius and maxRadius). I would leave dp and param 1 as is. minDist isn't too important. Make param2 lower so it accepts more eliptical shapes. minRadius and maxRadius can be made more forgiving by reducing and increasing them respectively. If you have managed to achieve lock, you might want to tune the minDist and minRadius and maxRadius in particular to be more accurate, along with param2 for circularity. I go a bit more into depth of the CV pipeline on my [blog](https://tecknet.dev/blog/cv-pipeline/) post if you'd like to know more.
18. If needed tune the dynamic RoI size in the winSize variable in mac.py. This controls how large the frame is after a lock is achieved. A larger size means more pixels to process, but more accuracy and lower likelihood of loosing the ball. A lower size reduces compute time, but if the ball is moving fast, it can loose lock.
19. With that you can start tuning the PID values. They can be found in the livceconfig.json. I won't explain how to tune PID, but its the same as any PID system would be tuned.

And with that you should be done! If you have any questions about the code, feel free to contact me at hattijeevan@gmail.com or via discord if thats your thing (tecknet.gg).
