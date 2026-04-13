Here's the hardware you should have on hand:


| Component                | File Name             | Qty | Material |
| ------------------------ | --------------------- | --- | -------- |
| Base                     | basefinal.step        | 1   | PLA      |
| Electronics Shield       | shield/shieldpcb.step | 1   | PLA      |
| Bottom Leg               | bottomleg.step        | 3   | PLA      |
| Top Leg                  | topleg.step           | 3   | PLA      |
| Mount                    | mountfinal.step       | 3   | PLA      |
| Mount Clip               | mountclip.step        | 3   | PLA      |
| Feet                     | leg.step              | 6   | PLA      |
| Standoffs                | standoff.step         | 6   | PLA      |
| IMU Mount                | IMU mount v4.step     | 6   | PLA      |
| Transparent Acrylic Disc | Check BOM             | 1   | Acrylic  |
| Pi Zero 2 W              | Check BOM             | 1   | -        |
| PCA9685                  | Check BOM             | 1   | -        |
| Camera                   | Check BOM             | 1   | -        |
| Servos                   | Check BOM             | 3   | -        |
| Wires                    | Check BOM             | -   | -        |
| PCB (optional)           | Check pcb folder      | 1   | -        |
| DC Barrel Jack           | Check BOM             | 1   | -        |
| Assorted M3 Hardware     | Check BOM             | -   | -        |
| Tie Rods                 | Check BOM             | 3   | -        |
| Shoulder Bolts           | Check BOM             | 3   | -        |



## PCB Prep

If you decide to use the PCB, just mount the headers of the Pi Zero 2 on the underside of it, and for the PCA9685, desolder the stock headers, and replace with standard straight headers to mount to the PCB. There are screw holes too if you want to mount it with bolts, but its not needed. All fab files can be found in the pcb folder.

## Assembly

Mount the 6 feet on the circumference of the base using an M3 bolt. Apply hot glue to the underside of all 6 feet to act as a grip. Ensure you don't place them on the holes reserved for the standoffs.

<img width="491" height="361" alt="image" src="https://github.com/user-attachments/assets/caf2bf3e-70bb-4718-b608-859a0d073aec" />

<img width="362" height="209" alt="image" src="https://github.com/user-attachments/assets/517edf70-deaa-4a19-9a72-b3cb5c24143d" />


Then mount and secure the three servos M3 bolts and nuts.

<img width="475" height="391" alt="image" src="https://github.com/user-attachments/assets/44a82f78-1a1b-4a5a-a2ac-4d9eccb965de" />

Attach all 6 standoffs to the remaining holes on the base:

<img width="566" height="419" alt="image" src="https://github.com/user-attachments/assets/918695df-f860-4744-943d-5fc0e548bddc" />

Mount the servo horn, and attach the bottom leg to the servo horn using 2 M3 bolts/leg. You can callibrate later, but I would recommend setting all servos to 0 before using an Arduino or something, and then attach the horns.

<img width="580" height="470" alt="image" src="https://github.com/user-attachments/assets/532093f9-2688-4265-9456-ffed2c6ffb7b" />

Attach the three tops legs using a shoulder bolt, and a lock nut (two standard M3 nuts work too).

<img width="524" height="572" alt="image" src="https://github.com/user-attachments/assets/0750dbc1-92ca-40d3-83a3-a5e3d9a4b2e9" />

You can then put the shield onto the standoffs, with the corresponding hardware, be that the electronics as is, or with the PCB. Both go on the same.

<img width="516" height="520" alt="image" src="https://github.com/user-attachments/assets/4e39d407-959a-4116-bc79-0adc075a28cb" />

Affix three tie rods to the top of each three legs.

<img width="529" height="587" alt="image" src="https://github.com/user-attachments/assets/67182d63-2210-4f09-90db-47008794714a" />

Then mount the three mounts onto. Thread a bolt through it, then a nut, then feed it through the tie rod, then another nut, and out the other end of the mount, then tighten with a lock nut on the other end. It should go, bolt -> hole 1 of the mount -> nut -> tie rod -> nut -> hole 2 of the mount -> lock nut.

image

Then mount the platform onto the groove. Place the 3 mount clips upon their correspodning holes, and tighten. Et voila you should be done!

<img width="540" height="596" alt="image" src="https://github.com/user-attachments/assets/ab742215-3086-488c-a342-74838bfa361a" />


