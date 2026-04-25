
And thats the journal! I am done with the project for now. There is minimal tuning left to do, but I will move onto other projects for now, and come back to this in the summer. 
For full transparecny, this was copied from the Stasis YSWS. My design was approved, but I didn't submit it to the final build approval, so I didn't use any of their funds in any way.
I didn't use Hackatime for firmware, since I started the project before Stasis had Hackatime integration, I cleared this with the staff before continuing at Stasis. I hope thats fine with Horizons.

I'm not entirely sure how Horizon calculates the hours spent. The hours I logged on Stasis are 46.3h. Thanks for reading!

# April 13th 2026 - 0.5h

So I started with the initial tuning of the platform, and I've gotten it to a point where it can move a ball to what is vaguely the centre of the platform. 

I'll finish tuning later this week. Besides that I updated the GitHub with all the final scripts and the FIRMWARE.md file that documents deploying and setting up the code. Just have to write-up the build instructions.


![image](https://stasis.hackclub-assets.com/images/1776073741593-00x5na.png)

# April 4th 2026 - 0.75h

Spent some time integrating everything into the main class for the Balancer.

Here's everything that I've added:

A basic wrapper for the IK class:

![image](https://stasis.hackclub-assets.com/images/1775324217930-5bgpq6.png)

And the main balance function (the setup then the main loop it enters):


![image](https://stasis.hackclub-assets.com/images/1775324309223-dtwfid.png)
![image](https://stasis.hackclub-assets.com/images/1775324321245-7cxb60.png)

Some of the values are hard coded as I just noticed, I'll change that eventually.


# April 4th 2026 - 2h

I implemented a basic PID class with the bog standard stuff. Its a bit verbose, but it simpler to use as a standalone unit I suppose:


![image](https://stasis.hackclub-assets.com/images/1775296402853-7gkfd6.png)

I also added a very simple config updating script that pushes new config values over UDP to the balancer:


![image](https://stasis.hackclub-assets.com/images/1775296438155-ngtghp.png)


The reason I did that was because the current system works by plugging my balancer into a 6V power supply, then connecting the Pi Zero 2 to my laptop using USB Gadget mode, and controlling the Pi Zero 2 using SSH. So if I were to let the PID values live on the script that gets uploaded, I would have to re-deploy and re-initiate the entire thing, which takes a solid minute. Doing that for ever small PID change is pretty stupid, so I wrote some boilerplate code to listen for new PID values over UDP and update that live. 

I didn't mention this in yesterday's CV session, but this was mainly inspired by a similar solution I had for the CV loop, I had a simple cvconfig.json with all my HSV values, that I can tweak during run-time instead of changing a hard coded value and re-running the entire CV script.



![image](https://stasis.hackclub-assets.com/images/1775296626787-tf1hjt.png)

Now all thats really left to do is integrate all this into the main Balancer class, and start tuning!

# April 4th 2026 - 4.5h

And we are done! This session was me writing up a nice concrete CV pipeline that worked well in a variety of lighting. I don't have the snippets of code as I wrote it, so I can't show you the development process, but in words, it was mainly messing around with Blurring, the detection alg (hough or contour), the paramaters, velcoity calculation and interpolation, colour filtering and some more stuff that I'll get into. I did mess around with the networking code a bit too, but nothing major was changed, it was already reliable enough as is.

Anyways, here's the loop explained!


![image](https://stasis.hackclub-assets.com/images/1775243709207-a1nfbm.png)

Starting with some nice old globals. Most of them are self explanatory, the only weird one are emaCenter, which I'll get to later when I talk abotu EMA (estimated mean average). isLocked is a flag to see if the ball is locked. lastRawCenter, i don't know why I named it as such, but thats the last center for the ball we deteceted.


![image](https://stasis.hackclub-assets.com/images/1775243783278-cvnth8.png)

Some more globals here, I accidentally had them somewhere else in the preamble.

This is a neat little static RoI (region of interest). It basically defines a portion of my screen that the detector should be interested in. That was mainly because my frame had some other stuff that wasn't the platform in frame naturally.

![image](https://stasis.hackclub-assets.com/images/1775243810928-cbrgue.png)


Then we load some config data, namely the colour filter. 

It loads the necessary array, and also has a default fallback in case its missing. The threshold is how much to trust that range.


![image](https://stasis.hackclub-assets.com/images/1775243872986-xyo794.png)

Then we actually define the mask for the RoI using rectangles:


![image](https://stasis.hackclub-assets.com/images/1775243939470-tjg35d.png)

Then we have the code for the actual RoI to be implemented

![image](https://stasis.hackclub-assets.com/images/1775243968891-mnpq3q.png)

This runs when there is a lock, and the lastCenter is not none. It defines a small square around the last centre to further reduce the processing space. I called this the dynamic RoI. The bitwise and is then applied with the static and dynamic RoIs to come up with the final RoI, and that is the frame we will then process.

Here's somes standard prepcoessing:


![image](https://stasis.hackclub-assets.com/images/1775244092537-m779xh.png)


Just grayscaling and blurring things up.

We then apply the Hough Transform, which I landed on. Its as simple as this:

![image](https://stasis.hackclub-assets.com/images/1775244133066-629oqk.png)


I also flipped the detection flag before going into the selection process for my ideal circle.

Then we have some more novel filtering:

![image](https://stasis.hackclub-assets.com/images/1775244191169-3iprhz.png)

We extract the circle data, and then start doing some swatching on the central pixels to find the HSV values of that. Its called the orangePercent, because my blue ping pong ball shows up as orange on the NoIR camera I have instlaled right now.

Then for some pretty standard velocity calculations:

![image](https://stasis.hackclub-assets.com/images/1775244265350-z240yt.png)

We ignore those that are moving to little by setting it to zero to filter out the raw noise. I'm not completely happy with how well tuned it is, but its something that can be improved if the need be.

Now for the filter EMA for those of you unaware is just a noise filtering thingy. Estimated Mean Average, in simpler words you define a contant that tells it how much to trust new data compared to old data. Basically? Its a bit more nuanced, and theres some math, but you shoudl google it if you want to know more. It was either that or a Kalman filter, but a Kalman filter was not something I could be bothered learning, and probably overkill too, so here we are!


![image](https://stasis.hackclub-assets.com/images/1775244788634-lfedsp.png)


Pretty straightforward impleentation.

We then just put all the data in a packet, give it a kiss goodbye, and send it off and hope and pray we're not lying to our hardware :]



![image](https://stasis.hackclub-assets.com/images/1775244828963-n9tyei.png)

Anyways here are some final annotations we put on the frame, before neatly serving this via flask too so we can oogle at it while it does its thing.


![image](https://stasis.hackclub-assets.com/images/1775244867392-11dpwg.png)

Most of the routing code is the same as you saw in the earlier networking software, so I won't bother explaining that again. But here we are! Very exciting :]

Just got PID implementing, I've already done most of the unit and integration testing, so we can just implement PID, tune it and call it a day!

# April 2nd 2026 - 1.4h

For previous sessions, I've been manually setting offsets using my phone as a spirit level, but alas, we suffer no longer. I introduce - THE AUTO CALLIBRATRON 3000.

heh. Anyways its a really janky implementation. It just uses the IMU to get pitch and rol readings, and slowly approaches them by updating the offsets and gives up when its close enough :]. I had some trouble where the 0 readings of the IMU were actually kinda slanted, and I didn't want to fix that, so adding the buffer gets a good result since it stops about ~20-30 off, and that is much more flat that going to 0,0. Fun!


![image](https://stasis.hackclub-assets.com/images/1775122249476-iwlmkn.png)


![image](https://stasis.hackclub-assets.com/images/1775122258205-5a5cw6.png)


# April 1st 2026 - 4h

This was... painful. Mainly because I absolutely suck at the maths I need for it. Its slightly above what I've learnt at school, but I managed to figure it out with a bit of brute force, and hand holding from the great [George Yuanji Wang](https://www.george-yuanji-wang.xyz/blog/3rrs).



![image](https://stasis.hackclub-assets.com/images/1775042538368-9odic1.png)


![image](https://stasis.hackclub-assets.com/images/1775042548819-1tk1rv.png)


![image](https://stasis.hackclub-assets.com/images/1775042561743-a4f8g9.png)



![image](https://stasis.hackclub-assets.com/images/1775042570600-avwyhy.png)



![image](https://stasis.hackclub-assets.com/images/1775042584138-ttr3i9.png)

![image](https://stasis.hackclub-assets.com/images/1775042597425-5zrkhh.png)

After deriving the equations, it was just a matter of translating that to code, which isn't the most horrible.

I started writing up the class. The init just defines the hardware (arm lengths, platform radius etc)

![image](https://stasis.hackclub-assets.com/images/1775042645502-0vbhly.png)

The goal is for it to generate the motor angles from any given roll and pitch angle. Using the pitch and roll, I calculate the normal vector of the platform when the ball balancer is in the correct position.

With the pose vector, I then solve for coordinates of the nodes connecting the arms to the top platform. With the nodes in our local coordinate system established, you can then convert them to elbow angles, which are the angles between the top and bottom arm. Et voila! You have your motor angles. Took a lot of testing to make sure the angles it was spitting out was right, and a bit of brain wacking to realise which arm is which on my actual build. But in the end it does work! I tested it out using a loop in the main func that lets me define any pitch and roll value, and by blue-tacking a nut onto the platform to act as the normal vector so I could manually verify. 

As long as this was, it was pretty fun to work on! I'll work on auto callibration next to use the IMU. 

Heres code screenshots, I forgot to add them:
![image](https://stasis.hackclub-assets.com/images/1775042934751-4jzkr8.png)


![image](https://stasis.hackclub-assets.com/images/1775042942207-tsf4wo.png)


![image](https://stasis.hackclub-assets.com/images/1775042948707-t2v357.png)


# April 1st 2026 - 3.3h

Basically the Ball Balancer's on board Pi Zero 2, while it can run full Linux, doesn't have enough compute power to viably run a CV algorithm in real time. To get past this, I'll just use the Pi Zero to stream frames over Flask to my computer, have that process the frame, and generate coordinates, and send that back to the balancer and run the PID on before moving the ball. The roundtrip latency should be made up for by the much much faster compute times my computer can offer over the Pi Zero, or even a more powerful Pi 4 or 5. 

I had to pour over the Flask Documentation for a bit to get the hang of things (and not to mention the painful SSH setup of the Pi Zero (legit took 3 hours that I won't try and count but man is that painful)). After skimming that and some documentation on the actual camera, I was done with the networking code:


![image](https://stasis.hackclub-assets.com/images/1774986725938-5regtu.png)

I then setup the listener script on my Mac to listen for frames and stream processed frames back to the Balancer. I just used my old CV alg for the time being to get networking working:


![image](https://stasis.hackclub-assets.com/images/1774986864680-fr33re.png)

![image](https://stasis.hackclub-assets.com/images/1774986887334-bywj4m.png)

I used some cool little lock based things so I could multithread the listening processing and streaming of data :]. Totally didn't need to but yes.
![image](https://stasis.hackclub-assets.com/images/1774986900365-kp991r.png)

It works for the most part right now, and some small tweaks and we should be good to roll. Also I used UDP for the coordinate streaming. I kind realised Flask might be a bit slow, so I started switching halway through, then reaslied that using pure UDP for the frames would be painful, so I'm sticking with Flask, unless latency becmomes a bottleneck.

# March 30th 2026 - 3.5h

Finally started building out the platform! Used some of the old parts that I had lying aroudn as I got the newer ones printing:


![image](https://stasis.hackclub-assets.com/images/1774873078355-ba8aab.png)

Once the new parts came off the printer, I started assembling using those instead:


![image](https://stasis.hackclub-assets.com/images/1774873118645-j8bo8i.png)

I then started wiring and testing the elctronics using an arduino I had lying around for now instead of the Pi Zero 2 W to keep things simple for the time being:


![image](https://stasis.hackclub-assets.com/images/1774873218705-rz1svt.png)

I wrote some cheap and dirty firmware to give each arm a little jiggle around to make sure everything was sound, and it was! Did have a bit of back and forth with my printer since some of my slicer settings were a bit shady, but I had eveyrthing printed out pretty quickly.

After testing the wiring with my Arduino, I grabbed my Pi Zero and chucked that in, along with the camera. The camera enclosure is kinda annoying, which in hindsight I saw coming. I did change it in the shield for the PCB, but I probably wont use a PCB since there isn't much point anymore. I tried chipping away the plastic for a bit instead of reprinting, but in the end I just routed the CSI cable over the enclosure bit. 

Finally when the IMU mount parts came of the printbed, I wired up my IMU and mounted it to the top platoform. And with that, I'm done building. Time to go refine my firmware now. 



![image](https://stasis.hackclub-assets.com/images/1774875649918-cij605.png)

# March 22nd 2026 - 0.1h

Added all the new files to the repository (the gerber and schematics) as well as the new shield. Added instructions on how to use to assemble it with or without the PCB. And modified the BOM by getting an estimate from JLCPCB


![image](https://stasis.hackclub-assets.com/images/1774188684389-5scncx.png)


![image](https://stasis.hackclub-assets.com/images/1774188694113-tcxvwd.png)


![image](https://stasis.hackclub-assets.com/images/1774188735432-q2ccko.png)

# March 22nd 2026 - 0.4h

Pretty much just what the title says. I redid the mounting posts on the top shield to accomodate the PCB. I then just imported the .step for the actual PCB, and assembled it again, and re-placed the electronics, since I couldn't be asked to link them into the actual KiCAD render.


![image](https://stasis.hackclub-assets.com/images/1774175836931-tnzr2j.png)

Looks pretty cool if you ask me :]


![image](https://stasis.hackclub-assets.com/images/1774175860589-4o0309.png)

Just gotta modify the BOM, add the new files to the GitHub, and ammend the build instructions and we should be able to re-submit for review :]

# March 22nd 2026 - 0.5h

Just polished the layout, I realised the pin for the V+ and GND was on the wrong side, so I'd have to cross wires over to get the screw terminal. Literally as I write this, I just realised I can just wire it up to the normal pin, instead of needing the screw terminal. I am stupid. Ok lemme go fix that...

But here's what it looked like before I go to fix it:


![image](https://stasis.hackclub-assets.com/images/1774172774274-pkp9sh.png)

Ok that only took like 5 minutes to fix. The new bit of the schematic:

![image](https://stasis.hackclub-assets.com/images/1774173049500-lfea05.png)

The physical PCB of course looks much the same. I'ma go ahead and export the .step and remodel the shield.

# March 21st 2026 - 2.5h

Layed out the schematic really quickly, wasn't much to that, and imported and assigned all the necessary footrpints:


![image](https://stasis.hackclub-assets.com/images/1774129966998-xyw3sm.png)

After a quick google, I found out that to get the outline of my shield, I just needed to make a new sketch, project the geometry and export the .dxf, which I did pretty painlessly. I took that, and imported it into KiCad and started laying out my components:


![image](https://stasis.hackclub-assets.com/images/1774130475014-tf52nn.png)

I plopped my compoenents down where they needed to be, and spent some time defining the shape of the actual PCB:


![image](https://stasis.hackclub-assets.com/images/1774132819865-0k5sn9.png)

Finished the wiring too:


![image](https://stasis.hackclub-assets.com/images/1774134638485-674zds.png)

Should be done with this PCB for the most part. Just gotta add some cool silkscreen stuff that I'll do tommorow I suppose. Also gotta tweak the mounting holes on the shield to accomadate the PCB.

# March 20th 2026 - 2h

Added a mount on the platfor to clip on an IMU that I had lying around. It will be used to help with auto callibrating the platform using a gradient descent algorithm. 

The clip design is pretty basic in and of its self, it just sandwhiches the platform between two parts and is tightented with some M3 bolts.


![image](https://stasis.hackclub-assets.com/images/1774021097862-kyctvg.png)

I also wrote and tested some IMU firmware and then packaged that into a neat class that I can then import and use. Getting clean data was a bit finnicky, and choosing the correct sample rate took a bittle of fiddling before I was happy with where it was. It gets relatively clean data right now, but I see myself tweaking the paramaters slightly later on.

Here is the firmware:


![image](https://stasis.hackclub-assets.com/images/1774021371217-owp5qf.png)


Also here's the actual mount:



![image](https://stasis.hackclub-assets.com/images/1774021441452-k5lrmx.png)

Pretty basic but it should get the job done.

# March 16th 2026 - 0.5h

Got some feedback from the reviewer, and I addressed it. I've improved the GitHub repo to add some preliminary build instructions. Along with that, I also uploaded the individual component STEP files to make printing out the compoenents simpler. 

![image](https://stasis.hackclub-assets.com/images/1773688798398-domuh4.png)


Also with the wiring diagram, there was one before, but I suppose it was hidden in the depths of the repo, so I've attached it to the readme as well. Hopefully that should be enough to get this approved!


![image](https://stasis.hackclub-assets.com/images/1773688813226-orq5vk.png)

# March 9th 2026 - 2.5h

I was advised to also develop firmware for the Camera and CV before submitting it for design review, so here we are!

The code is very much untested, and I fully intend on rewriting it from scratch, but I might as well take this opportunity to familiarlise myself with OpenCV. 

I read the documentation for a bit, and and once I was somewhat familiar with it, I started looking at ball detection tutorials (https://www.youtube.com/watch?v=RaCwLrKuS1w 10/10 would recommend), and implemented this follwing the tutorial into my class, along with some camera logic. I also implemented the Camera class. Still very barebones, and I need to figure out networking, but it should (in theory) be able to display a video feed, and detect a ball. I set up some basic end points for getting ball speed and location which can then be called by the PID loop when needed. Again most of this WILL be reworked later.

I also did some intensive research into CV itself, and two popular algorithms, the Hough Transform and Contour detection. To get even more familiar with this, I implemented the former myself in python! 

Here are some pictures of the pipeline:

![image](https://stasis.hackclub-assets.com/images/1773090596631-hvk9y8.png)


![image](https://stasis.hackclub-assets.com/images/1773090604457-ghrd9q.png)


![image](https://stasis.hackclub-assets.com/images/1773090611440-9l4y1d.png)

![image](https://stasis.hackclub-assets.com/images/1773090272912-5bmnvx.png)

Heres the result on a random picture I threw together in Canva (this was Hough transform). I also did some research into Contour detection, but didn't get round to impleenting that myself. 

I also found this cool picture of how the accumulator looks:


![image](https://stasis.hackclub-assets.com/images/1773090365073-i9tvyh.png)


I tried really to implement this myself, but didn't get very far. Its something I want to revisit in my own time for sure though!

(Note: time spent implementing the algorithms was not included, but I thought it was fun to mention!)

Back to the actual firmware:

I'm using the Hough Transform right now in the code, but I'm still very much on the fence on whether I shoudl use this or the Contour detection. Contour detection is a fair amount faster, but implementing it isn't as easy, and either way, performance isn't really a bottleneck since I'm computing on my laptop. Right now I'm swaying towards Hough, but that might change later. 


![image](https://stasis.hackclub-assets.com/images/1773090491727-vbm2sv.png)


![image](https://stasis.hackclub-assets.com/images/1773090548600-e25u5n.png)

Code will be uploaded to GitHub shortly (once I figure out how to rebase my repo)!

# March 8th 2026 - 2h

And we're done! Finished assembling the model in CAD, and spent a long long time getting all the joints to play nice. The top spherical joint was particularly painful, and after trying like 3 times, I even revereted to the old mount I had on the the very first design. Somehow after importing that in and jointing it, everything was working fine. I daren't try and replace it with the actual joint, besides, ignoring the visual oddness, it should behave the same when I actual 3D print and assemble everything.


![image](https://stasis.hackclub-assets.com/images/1772983941196-2hpwrg.png)


![image](https://stasis.hackclub-assets.com/images/1772983970077-c9nnk4.png)

I ran a few motion studies to make sure everything was working fine, and it all checked out.

I spent another 20 minutes or so completing the GitHub repo and uploading all necessary files for the review. 

![image](https://stasis.hackclub-assets.com/images/1772985184416-djanzn.png)


Now time to get it reviewed 🤞,


# March 7th 2026 - 1.6h

Implemented the main firmware script in python. It will be the main balancer class. Imported my servos, and isntanstiated them. Added a bunch of helper functions and set out the basic layout of the software. 

![image](https://stasis.hackclub-assets.com/images/1772888872487-clhk4l.png)

Also made a cool little flowchart so I don't forget how this is going to work :]


![image](https://stasis.hackclub-assets.com/images/1772889143724-pcldfj.png)

While I was implementing this, I also brainstormed the idea to add an IMU to the platform to have automatic callibration. Since I would have to manually callibrate it anyways, having an automatic callibration feature would really help streamline that. I will think of adding that later on, but I want to get the project as is design reviewed ASAP.

The new code has been uploaded to the github!


# March 7th 2026 - 0.25h

The wiring is pretty simple, but its a requirement for the repository to get it past the design phase, so I quickly threw toghther this in EasyEDA:


![image](https://stasis.hackclub-assets.com/images/1772887242841-fd2z2i.png)

Based it off the documentation:


![image](https://stasis.hackclub-assets.com/images/1772887277256-it12p9.png)


Not much else to say here :]

# March 7th 2026 - 0.6h

I cleaned up an overhang that I found in the base, not entirely sure how I didn't see that before, but yeah, I fixed that so it doesn't immediately snap when I try screwing my servos in.

Additionally to save some weight, and also perhaps make wiring it a bit easier later on, I added some large cutouts to the bottom.

I ended up with this cool hexagonal pattern, and I think thats the base finalised:


![image](https://stasis.hackclub-assets.com/images/1772878718844-mmsc8q.png)

I also remade the mount since I wasn't a big fan of the stupid halo thing I had going on before:


![image](https://stasis.hackclub-assets.com/images/1772878782877-49gfwc.png)

I also modelled the other half that would sandwhich the platform in between them:



![image](https://stasis.hackclub-assets.com/images/1772878818266-e9ylqg.png)

# March 6th 2026 - 1h

Since I now have the servos on hand (still waiting on the Pi Zero 2), I started writing the firmware to control the servos. Pretty simple stuff:

Did have to do a bit of googling to get the maths for it, and after some debugging it was working fine.

![image](https://stasis.hackclub-assets.com/images/1772840908542-po4ewj.png)

I also started refactoring this into python for the actual firmware since I will definitely be writing the code in python. I mainly just coded it in arduino c so I can verify my maths on hardware and ensure everything is working fine, and I was a bit to eager to start programming, despite not having my Pi Zero just yet.

The code in python is basically a line by line translation of the C code, but I also encapsulated it all neatly into a class so its easier to use later on.


![image](https://stasis.hackclub-assets.com/images/1772841210063-fkcxj4.png)

Also added some helper functions like sweep and update offset to streamline the code later on. The code will be up on the project github once I get to that :].

# March 6th 2026 - 2h

Finished the final main compoenent of the platform, and only have to make the assembly now.

I started the session by scouting out the CAD files for the electronics I would be using. At this stage, I've decided not to make my own custom PCB for it, since there isn't much point, I'm using a PI Zero 2, and a PCA9685, and unless I want to design a breakout board for that, which I don't particularly want to do. 

Starting where all good designs start, I extruded a circle. Actually wait I projected the base, to preserve the mounting holes... then I extruded a circle. Cool!


![image](https://stasis.hackclub-assets.com/images/1772824752736-aazygn.png)


After some deliberation, I decided to shape my cutouts like this:


![image](https://stasis.hackclub-assets.com/images/1772824772620-up5ngu.png)

I layed out the electronics mentally, and then added a slot for the wiring of the servos, and the rounded everything off.

 
![image](https://stasis.hackclub-assets.com/images/1772824821179-r1uqk5.png)

Next I pulled up the datasheet for my camera, and started adding the holes for the board to sit on.


![image](https://stasis.hackclub-assets.com/images/1772824859718-0l4vwd.png)

I designed a little enclosure kind of thing around the camera:


![image](https://stasis.hackclub-assets.com/images/1772824901327-wmik9f.png)

Now I pretty much just added mounting holes for the PCA9865 board, and the Pi Zero 2:



![image](https://stasis.hackclub-assets.com/images/1772824936458-e0dz4e.png)


A few more holes for the zip ties for cable management that I will totally get around to, and we're done!

With that modelled, I started placing in the compoenents to get a vague idea of how it would look. I will finish the fully jointed and articulatable model tommorow, and with that I think we can call the design phase (at least the initial design phase finished). Just got to write some firmware for the servos (already ordered the parts), and then we can submit it to get reviewed :].

Heres the final electronics shield:
![image](https://stasis.hackclub-assets.com/images/1772825094872-qxmdn3.png)

# March 6th 2026 - 1.25h

I spent a bit of time at the start of the session brainstoriming mounting mechanisms for my platform. I didn't have the necessary tools at home to drill through the acrylic disc, so I ended up with a mount that sandwhiches the platoform between itself and another piece using and M3 screw and a nut. Pretty simple.

For the actual design of the mount, I thought I'd try out a sort of halo shaped thing. The three mounting locations would be equall spaced apart, and attached with a ring on the outer edge. The main reason I thought of making this was that it makes tuning a bit easier since it physically prevents the ball from falling off the platform. I don't think I'll keep it for the final design, but since I'd already modelled it, I suppose we're keeping it for now.

![image](https://stasis.hackclub-assets.com/images/1772780634264-xol5qb.png)

With all the core compoenents modelled again, I started with the assembly of the actual platform in CAD. I tried to be a bit more meticulous with my constraining, but I don't think everything magically fixed itself just yet.



![image](https://stasis.hackclub-assets.com/images/1772780742224-lrsyey.png)

So for the actual hardware it seems that I only need to model the shield, and perhaps do some weight optimisation for the base by adding some cutouts.

# March 5th 2026 - 2h

With the maths for the arms decided earlier, I started redesigning the entire platform. I wasn't happy with the old base, so after deliberating for a bit, I decided to stand the entire platform off the floor using some feet.

I decided to keep the old radius, and extruded it to an appropriate thickness. I imported an placed one of the servos to have a reference for the mounting holes. I decided to simplify it from the old design in the end, with two standoff things instead of the whole housing thing I had going on last time. 

I also needed to decide on the placement for the mounting holes. I needed holes for both the feet and the standoffs. With a pattern decided, I replicated it using the circular pattern. And with that the new base was modelled.

I quickly modelled some feet too, just a tapering cylinder (I suppose its a frustrum). The shorter radius circle would have some hot-glue glued on to act as a grippy grip part to dampen vibrations. I think I mentioned this in a previous journal? 

Either way, it looked something like this once I was finished with that:


![image](https://stasis.hackclub-assets.com/images/1772737174405-ahq71a.png)

Now for the interesting part, the arms. At the start, I went with the same approach as before, making a yoke style joint. After messing around with that design for a bit, I realised I didn't like where I was going with it, asthetically at least. After googling around for some inspriation, I settled with the split hinge. Each arm would form half of the hinge, and the shoulder bolt going through it would attach the two halves.

Relatively quickly, I had come with this cool design for the bottom arm.


![image](https://stasis.hackclub-assets.com/images/1772737311036-gssv43.png)

Its much simpler than any of the other arm designs I came up with, but I think its pretty elegant. 

I spent a bit more time designing and refining the top arm. Since these arms were a fair bit thicker than the other one, I couldn't just add a tie rod to the top surface or it would look very odd. I took a few approaches, extruding a cylinder from the top to be an extension of the arm going into the tie rod, and a few other such things. In the end I settled on simply tapering it up, and creating a pentagonal cutout to let me screw the tie-rod in place.

I was pretty happy with that design. 


![image](https://stasis.hackclub-assets.com/images/1772737479807-4hlpnc.png)

With the arms and base done, I have to redo the mounting, or do it for the first time, since my original was just hot-glue. I'll figure that out tommorow or over the weekend.

# March 5th 2026 - 1.5h

With the occulsion issues I noted in the first iteration, I wanted to focus a session on reviewing the geometry and getting more familiar with the platform. 

The issue that I realised was that the arms when attached to the horns were too long, and so to maintain a resaonable height above the camera, they were forced inwards ("elbows in position")  In that position, the camera was being blocked. When the arms are forced to a elbows out position, the platform is too close to the camera, and so the camera's FOV isn't great enough to capture the entire platform. 

I started researching the maths behind it, and after a while of debugging my poor algebra, and getting used to the vectors, I found out that the optimal length for the arms were around 75mm. I did this by defining a target height, and expressing that in terms of the arm lengths, and the angles between the arms and the base. I forced the angle between the base and the arm to be obtuse, and the angle between the arm and the arm to be actute to fit my target position.


![image](https://stasis.hackclub-assets.com/images/1772735263541-4mk08b.png)

I also had some fun deriving the forward kinematic equations for my platform. While for the firmware, I will need to derive the inverse kinematic equations, practing with the forward ones might help later one. They are significanly easier to derive than the inverse, so I messed around with that for a bit.


![image](https://stasis.hackclub-assets.com/images/1772735351554-98d2aa.png)

With a better familiarity with my platform and its geometry, I will set out to start the second hardware iteration later tonight, or perhaps tommorow.

# March 4th 2026 - 3.5h

I started the intial 3D modelling of my 3RRS parallel manipulator. I had already picked out components in my previous log, and so I first found 3D models for the servos that I would be using (I'll add the electronics in later). 

For inspiration, I looked at a few similar projects online during the planning, so going into it, I had a vague idea of what I wanted to model it around. 

I extruded out the base, and then placed the three servos around the base on the vertexes of an equilateral triangle. I spent a bit of time fiddling around trying to get the actual actuator part of the servo onto the corner. After I had that, I created a rigid group between the three servos and the base.


![image](https://stasis.hackclub-assets.com/images/1772624280937-01vtkl.png)


![image](https://stasis.hackclub-assets.com/images/1772624301262-28wauf.png)

With the base modelled in, I started working on the bottom leg of the manipulator. I wasn't sure what length to make it, so I settled on the arbritrary length of 90ish mm. For the actual joint, I decided to use a yoke style joint, with a shoulder bolt going through attaching it to the top arm. I also chamfered it because I thought it looked pretty cool :]. 

After that I just modelled some holes around the servo horn, and added fillets all around. I then added rigid joints between the servo horns and the arms.


![image](https://stasis.hackclub-assets.com/images/1772624464436-il8dsl.png)

The top arm was a fair amount simpler to model. I just modelled it as a cuboid, added a cutout to allow me to screw the tie rod in for the top of the second arm. After adding some fillets for good luck, I was done with that part too.


![image](https://stasis.hackclub-assets.com/images/1772624620341-e92de2.png)


![image](https://stasis.hackclub-assets.com/images/1772624637021-jof8z1.png)

I spent a bit of time after that trying to find the exact 3D model for the tie rod that I had sourced on Amazon, but after a few minutes of searching I couldn't find one, so I decided to start 3D modelling it. Turns out, my familiarity with Fusion360 was not good enough to allow me to do that :|..


![image](https://stasis.hackclub-assets.com/images/1772624711049-ama2zb.png)


![image](https://stasis.hackclub-assets.com/images/1772624722104-y90tgs.png)

After wasting a bit of time trying to figure out how to make it smooth and stuff, I gave up, and after a bit more digging on the internet, I found a decently close model.


![image](https://stasis.hackclub-assets.com/images/1772624777589-zwics2.png)

I then started modelling the mount attachment for the platform at the top of the second arm. I wasn't entirely sure how I would attach it. For this iteration, since I'm assuming I will be remodelling it after, I just assumed I would hot-glue it to the platform, so there are no mounting holes or anything. Its just a simple T-Shaped mount, with a yoke-y kind of cutout for the tie-rod to slot into.


![image](https://stasis.hackclub-assets.com/images/1772624981616-lwhz6m.png)

With that mirrored over, I quickly modelled the actual platform and attached it to the mounts.

![image](https://stasis.hackclub-assets.com/images/1772625031474-7fxvy4.png)

While messing aroudn with the joints, I realised a critical flaw in this design, the joints were "elbow in" and so it would very significantly obstruct the camera, and would mean that there wouldn't be a clear view of the platform. This wouldn't work as I would need constant view of the ball for the camera in order to detect it. When I forced the position of the arms into an "elbow out" position, the platform would be too close to the bottom, and so I doubt the camera's FOV would allow it to see the entire platform. 


![image](https://stasis.hackclub-assets.com/images/1772625259187-ue2pnl.png)

I also found out my joints were pretty broken. I'm pretty new to the entire CAD thing, and most of my projects before this have been ECAD heavy, and just used normal CAD to design enclosures, I had never used joints before. I had to learn that on the fly, and I messed up somewhere, and the entire thing breaks every once in a while. I will spend some time after this reviewing my geometry and figuring out how to properly define and contraint joints.




![image](https://stasis.hackclub-assets.com/images/1772625324945-xozgoj.png)

I did also mess around with the base, but its pretty ugly anyways, so I'll redesign the whole thing.


![image](https://stasis.hackclub-assets.com/images/1772651996318-6l608k.png)





# March 4th 2026 - 2h

I spent this session doing all the core research and making design decisions, as well as producing a BOM. The research involved deciding between what platform to use (I ended up choosing the 3RRS parallel manipulator), my choice of actuator (deliberating between servos and steppers), how the detection of the ball would work (camera vs other sensors). I then started laying out my choices for system architecture and microcontroller choices.

After I decided to use the 3RRS parallel manipulator, I spent some time getting familiar with that. With a general sense of directione established, I started hunting for parts so I could start working on the 3D model. The BOM is at the bottom of this journal.

Below you can find a project specification document I wrote. It was written for my Crest Gold Submission (A certifcate awarded in the UK). Time spent writing the journal was not included in the journal time, only time spent researching.

Also its come to my attention that the journal does seem AI generated at first glance (the headings and all that), but please do read a few paragraphs, I think its quite evident from my weird literature that it is handwritten. Thank you!


## Project  Specifications
### Abstract
The goal of the project is to design and a build a platform to test the reliability of computer vision as a suitable sensory input in a closed loop feedback system. Computer Vision requires significant hardware overhead and may be deemed less consistent than other dedicated sensors. However the flexibility and accessibility of the solution makes it an option worth investigating. The project will involve designing and building a balancing platform that utilises visual feedback to achieve stable positioning of a ball.

### 1.1 Objectives
- To design and build a 3RRS Parallel manipulator based balancing platform
- ![image](https://www.google.com/imgres?q=3rrs%20parallel%20manipulator&imgurl=https%3A%2F%2Fwww.researchgate.net%2Fpublication%2F330682713%2Ffigure%2Ffig1%2FAS%3A1086043101110357%401635944261499%2FThe-3-RRS-parallel-manipulator.jpg&imgrefurl=https%3A%2F%2Fwww.researchgate.net%2Ffigure%2FThe-3-RRS-parallel-manipulator_fig1_330682713&docid=dTmalGFcmmkVmM&tbnid=_OUDrZWx8eyaFM&vet=12ahUKEwjm8vWDkYaTAxXISUEAHZOgAc4QnPAOegQIGhAB..i&w=660&h=470&hcb=2&ved=2ahUKEwjm8vWDkYaTAxXISUEAHZOgAc4QnPAOegQIGhAB)
- ![image](https://www.google.com/imgres?q=3d%20printed%20ball%20balancer&imgurl=https%3A%2F%2Fhackster.imgix.net%2Fuploads%2Fattachments%2F1457342%2Fimage_4JQES2zCCY.png%3Fauto%3Dcompress%252Cformat%26w%3D740%26h%3D555%26fit%3Dmax&imgrefurl=https%3A%2F%2Fwww.hackster.io%2Fnews%2Fnicolas-hammje-s-ball-balancing-bot-uses-opencv-on-a-raspberry-pi-to-stop-a-ball-dead-in-its-tracks-f8748c394bde&docid=AHDAYPaPU_FkbM&tbnid=DdAyNKGYlCULWM&vet=12ahUKEwiy0ZnmkYaTAxXHUUEAHSz4Dr8QnPAOegQILhAB..i&w=740&h=416&hcb=2&ved=2ahUKEwiy0ZnmkYaTAxXHUUEAHSz4Dr8QnPAOegQILhAB)
- To integrate a camera to provide visual feedback for real time balancing
- To design and create a closed loop PID controller using the camera for input
- To refine and evaluate the performance and limitations of visual feedback in a real time closed loop system.

### 1.2 Rationale
The choice to use computer vision in this project comes from the inherent flexibility it offers compared to other approaches that are often utilised. One common alternative uses a capacitative touch screen to locate the ball. While this approach does offer a high level of reliability, it comes with hard constraints, like the difficulty of being able to find a suitably sized screen, and the fact that the code would only work with a pre-characterised ball. Not to mention the fact that the ball has to be a weighted in order to even register on the sensor in the first place. This approach clearly has its downsides, and so an alternative was sought.

Another approach I've observed is using an IR sensor array to position the ball. While this approach too offers a high level of accuracy with minimal computing overhead, the cost and complexity of implementing an array of sensors and receivers is too high.

This is reflective of many other situations where there are multiple sensors that are capable to getting the job done, but they all trade off one thing or another. This is where visual feedback comes in. It is perhaps the most important way people sense things around us. Why not utilise this with computer too? We humans are able to perform the most complex of coordination solely with our eyes. 

Many others have asked this question, and so we have seen a drastic increase in the usage of camera's as a sensor in the modern world, facial recognition being one of the most prominent examples. However one area which is still yet to be explored to its fullest, is the application of computer vision in real time, closed loop feedback systems. The reasons are primarily to do with unreliability of algorithms in detecting and characterising its targets, coupled with the high computational overhead that it poses. 

Ultimately, this project serves to explore and push the limits of computer vision as a control input. I hope to attain a better understanding of its abilities and disadvantages that will be clear during the process of this project.

### 1.3 Requirements
#### Functional Requirements
- Full addressable 3RRS platform or equivalent
- Smooth control using PID (eliminate jittering)
- Minimal mechanical backlash
- (optional) Use PCB to clean up wiring
#### Performance Requirements
- Maintain the position of the ball within $\pm5mm$ of the centre (or any arbitrary point)
- Camera processing at 12fps minimum
- Roundtrip latency of 150ms maximum
- Operate with significant disturbances applied to the ball (to be defined later)

### 1.4 Deliverables
- 3D manipulatable platform 
- Establish camera feed
- Identify ball using Computer Vision Algorithm
- Derive inverse kinematic equations
- Implement PID loop
- Integration

### 1.5 Budget
At this stage it is hard to define a set budget, as system architecture, and final component list are not finalised yet. From previous project experience, I would estimate a budget of ~£80 on the lower end. The main costs will be the 3 servos motors, the microcontroller and miscellaneous hardware (nuts, tie rods, DC/DC buck converters etc), PLA for printing parts and the microcontroller we end up choosing. Other variable costs could include PCBs if I decide to design and fabricate them to clean up the wiring of the system.

Costs will be estimated more accurately at a later stage of the this log. Cost optimisations will be done in the hardware phase and a final cost estimate will be available by the start of the Initial Fabrication stage.

### 1.6 Proposed Timeline
##### Planning Phase
Includes drafting project specifications, and preliminary deign documents outlining systems and justifying choices. Creating the initial parts list and sourcing components. 

##### Hardware Design 
Modelling the first iteration of the project in Fusion 360, as well as creating the initial schematics for the electronics.




##### Initial Fabrication 
Buying all components and fabricating parts (3D printed). Assemble all parts to make the initial platform.

##### Testing / Iteration
Test the hardware and electronics and identify errors. Making amends to design and re-fabricate. Iterate until hardware platform is to specification.

##### Write Computer Vision Algorithm
Establish video stream over serial or WiFi and create a computer vision algorithm to detect the position of the ball on a 2D plane.

##### Write PID loop
Use inputs of computer vision algorithm to run a PID loop to create endpoints for the stepper motors to move to. This will run independent of the hardware until outputs are validated.

##### Hardware-Software Integration and Tuning
Fully integrate the hardware and software components. Test initial integration and tune the PID variables. Adjust any other aspects of code to be better compatible with the hardware.

##### Final Testing and Evaluation
Test the final platform and evaluate its performance objectively. Compare it to similar projects that employ other sensor systems and evaluate the effectiveness of my solution.

## Hardware Design


## Broad Subsystems and Component Choices
### Platform
We need to create a platform that is manipulatable in at least 2 dimensions (x and y) in order to move the ball around on the platform by tilting it in the required direction.

This would mean the bare minimum required would be a simple platform connected to two actuators (servo or stepper motors). But this would introduce instability as two points of connection perpendicular to each other might not be enough to hold up the platform. This would require extra mechanical supports to keep it balanced. 

Instead of adding a extra redundant support, I am deciding to use a 3RRS (3 actuators with two revolute joints and one spherical joint) parallel manipulator instead. This uses three actuators instead of 2, providing greater structural stability, with no extra supports required. This also provides me the ability to move the platform in 3 Dimensions, allowing flexibility for any future features that I might want to add. However it does introduce significant mathematical complexity in terms of deriving the inverse kinematic equations necessary to control it.

#### Actuator Choice

The two main choices for actuators are Stepper Motors and Servos. Both of them are completely viable choices, but each have their own caveats.

#### Stepper Motors
Stepper motors are electromechanical devices that convert digital pulses into precise rotational movements. The provide high torque output, and have minimal backlash, meaning when idle, it can hold a significant load on the actuator. Controlling them however becomes a pain point in my application as it has no loop control, so if it misses steps in its cycle, that can be an issue. 

Extra control hardware, like the TMC2209 drivers are required.

#### Servo Motors
Servos integrate a motor and sensor for position feedback to provide accurate rotational movement. You provide the servo an angle and it will turn to that precise angle. The downsides of Servos are that in order to provide as much torque as steppers, they become more expensive. However I think this trade off is worth it as it simplifies the control significantly since only an angle is required. 

Extra control hardware, while not necessary, is recommended. I will be using the PCA9685.

#### Decision
I have decided on using Servo Motors for their ease of use. Both solutions come in at near identical price points, making it a close competition, but the simplification of output control provided by the closed loop nature of Servos makes it a more approachable choice. I will be using DS3218 Servos, rated for 20KG, with a range of 270º, providing significant overhead.

Should I later consider using steppers, the most likely choice would be the NEMA 17, which is a popular form factor for stepper motors, often seen in 3D printer. They are easily sourced, and readily available, making it ideal for this project.

### System Design
At a glance there are two broad approaches I could take in system design. I shall outline them below, whilst considering their benefits and drawbacks.

#### Fully Self Contained System
This system would include all necessary hardware onboard, and would not communicate to any external computer to achieve the goal. This would entail that the computer vision algorithm and the PID loop would have to run on the onboard computer/microcontroller.

This would result in a fully self-contained system, however it would require significant onboard computational power to handle the computer vision at a frame rate suitable for the project. The likely choice of control computer in this situation would be a Raspberry Pi, which would increase the budget by significant amount.

#### Delegation
This system would offload the bulk of the heavy computational workload to an external computer, ideally a laptop. The laptop would then run both the computer vision algorithm to locate the ball, and the PID loop. It would then send the actuator end-points over to the onboard microcontroller, which is tasked with sending signals via its GPIO. 

This method would save significantly on costs as the onboard microcontroller could theoretically be something as cheap as a Raspberry Pi Pico (~£4). Some limitations of this include increased latency, however if a wired connection is used, the latency gains from the computer vision algorithm should compensate. 

Within this architecture there exist two marginally different implementation, regarding the manner in which the camera is dealt. One approach would be to use a USB camera connected directly to the laptop. The other approach would be connecting it to the microcontroller and streaming that to the laptop for processing. The only drawback of the first approach is that it would result in another data line between the platform and the laptop. The latter approach limits the choices of microcontroller, as it needs to be easily usable with a camera. I shall explore microcontroller choices later in this section.

#### Decision
I have decided to use the latter system architecture since it more cost effective, and more performant. It is also flexible in that should I later want to containerise the system, integrating an onboard computer like the Raspberry Pi, would be relatively trivial. 

### Microcontroller
In the current state of hobbyist electronics, we are spoilt for choice when it comes to microcontrollers, with there being a mainstream and well designed microcontroller fitting the most niche of needs. Here I will consider my choices and come to a decision regarding the same.

##### Raspberry Pi Pico/2/W
The Raspberry Pi Pico is a small, cheap, and relatively performant microcontroller. Its hardware is suited to drive three servo motors, and should have no difficulty in receiving and forwarding instructions from a laptop. I have a lot of prior experience working with this particular microcontroller, and it is a strong choice, considering its incredibly low cost. 

The only downside is the difficulty in using a camera with it. It is not immediately compatible with most cameras.

Variations of it also include WiFi, allowing for flexibility in communication methods with the laptop.

##### Raspberry Pi Zero/2/W
The Pi Zero is in between the Pi Pico and the traditional Pi in terms of performance and price. It is a step up from the Pi Pico, and runs full Linux. This means it is significantly more performant that the Pi Pico, however as we realised, without our current system architecture, onboard performance isn't vital. 

The main benefit of using the Zero is that it has an onboard port for camera input. This simplifies camera processing, as the Zero can run a simple script to receive and send over the video stream to the base station.

The only real downside is that it is more expensive than the Pi Pico, but still very reasonably priced relative to its performance (~£15). This makes the Pi Zero immediately more attractive than the Pico. Stock is however a challenge to acquire in the UK due to its popularity.

#### Raspberry Pi 3/4/5
The Pi would be the go to choice if I were to build a fully contained system. It is completely capable of running a CV algorithm, a PID loop and driving the servos with no issues. For the time being, I have chosen not to use the Pi for cost saving reasons. At ~£50 for a high performance model, it would take up a significant amount of the proposed budget. 

As mentioned before, switching from the delegated system to the self contained system would be relatively trivial. In fact it would simplify a good amount of the code, as packaging and sending the data between the platform and the computer would be made redundant. Due to this, the Pi will remain as a reserve choice, for if the goals of the project were to change.

#### Other Microcontrollers
Other microcontrollers that I considered include the ESP-32, a strong contender with the Pi Pico, and Arduino systems. The ESP-32 would be most likely to replace the Pico as it is more performant, and also incredibly cost effective. Arduino's on the other hand struggle to meet the price to performance that the other options offer, and so most Arduino boards will not be considered. However during the planning of this project, Arduino was bought by Qualcomm, and they have announced the new Arduino Uno Q, which is an attractive prospect. It offers an SBC (Single Board Computer), with performance comparable to a Pi 3, and two onboard chips, a Qualcomm based chip and an STM32. At its price point of ~£40 it is still a bit too expensive to consider, but if sourced for cheaper it could provide a very good alternative to the Pis, allowing me to run it all on-platform.

#### Decision
For the time being, I have come to the conclusion that the Pi Zero 2 W is the best option. It provides easy interfacing with cameras and high level threading capabilities, all at a low cost. The first iteration of the platform will be modelled assuming the Pi Zero 2 W as the microcontroller

### Other Hardware

#### Camera
Since the microcontroller we chose is the Pi Zero 2 W, the most suitable camera would be the Raspberry Pi Camera Module 2, with an appropriate adapter ribbon cable to let it slot into the smaller port on the Pi Zero 2.

#### Servo Motor Driver
A popular option is the the PCA9685. It can support up to 16 servos, providing plenty of overhead. The main use of a driver board is since a Pi Zero cannot provide nearly enough current to drive 3 Servos at once.

#### Power Supply
A 6V 10A power supply is required for the servos. They are rated for $2A$ stall current, so in the worst case scenario, our max draw would be $3\times2A = 6A$. A 10A power supply has plenty of overhead for this scenario. The microcontroller will be powered through micro-usb. It is possible to use the main power supply to power the microcontroller, it would just require a DC-DC Buck Converter to step down the 6V to the 5V necessary. I have a few buck converters on hand, and so this change might be made, if the power supply's voltage is stable enough.

## Budgeting

## Components

| Component             | Function             | Quantity | Price (unit*qty) | Source                                                                                                                                                                     |
| --------------------- | -------------------- | -------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Raspberry Pi Zero 2 W | Microcontroller      | 1        | £14.15           | https://shop.pimoroni.com/products/raspberry-pi-zero-2-w?variant=42101934587987                                                                                            |
| Pi Camera             | Camera               | 1        | £12              | https://shop.pimoroni.com/products/raspberry-pi-camera-module-v2?variant=19833929799                                                                                       |
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
Total Estimate: £127.97

Notes:

Pi Zero 2 W out of stock at all major UK retailers, and Amazon resellers selling well above MSRP. Will await further stock.




![image](https://stasis.hackclub-assets.com/images/1772623700692-b7qd2i.png)
