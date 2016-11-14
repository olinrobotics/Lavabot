---
title: Troubleshooting
layout: template
filename: troubleshooting
---

# Index
*[My motors are not responding to the transmitter commands](#my_motors_are_not_responding_to_the_transmitter_commands)*

*[My motors are obeying the transmitter commands, but they're acting strangely.](#my_motors_are_obeying_the_transmitter commands,_but_they're_acting_strangely)*

*[I can't even arm my rover because my motors go beserk whenever I try.]()*

*[I can't disarm my rover.]()*

### My motors are not responding to the transmitter commands.

Double check the robot. Is it armed? If not, please disengage all safeties and arm the robot before proceeding.

Double check your RC channel mapping, following [these instructions.](http://ardupilot.org/copter/docs/common-radio-control-calibration.html) Olin College uses controller configuration 2, as do most American controllers. You may need to [remap the controls](http://ardupilot.org/copter/docs/common-rcmap.html#common-rcmap) if your RC channels don't correspond to the right configuration in Mission Planner.

If your RC channels are mapped to the correct configuration, check that the battery is plugged in, the robot is on and the power cable leading to the Pixhawk has not slipped out. You should check for loose wires and other anomalous occurences at this time. 

Now check your power supply. Has your emergency switch flipped, cutting current to the motors? Has your fuse blown, cutting current to the motors? Does anything feel warm to the touch? If any component feels hot, turn your robot off immediately and disconnect the battery. You may have an electrical short.

### My motors are obeying the transmitter commands, but they're acting strangely.

Double check your RC channel mapping, following [these instructions.](http://ardupilot.org/copter/docs/common-radio-control-calibration.html) Olin College uses controller configuration 2, as do most American controllers. You may need to [remap the controls](http://ardupilot.org/copter/docs/common-rcmap.html#common-rcmap) if your RC channels don't correspond to the right configuration in Mission Planner.

Now check your motor controller. Olin College uses the [Sabertooth 2x12](https://www.dimensionengineering.com/datasheets/Sabertooth2x12.pdf), which has 6 DIP switches that control how it is configured. 

In order, switches 1-6 should be DOWN, UP, DOWN, DOWN, DOWN, UP. This is because Sam the robot runs on lithium batteries (sw.3) using RC control (sw.1 and sw.2) and skid steering (4), with no special handling like exponential response (sw.5) or 4x sensitivity (sw.6).

One possible problem that can occur is if your controller is outputting mixed commands, like the DX8 does by default. In order to account for this problem, go to the Configuration/Standard Params page in Mission Planner. [Set SKID_STEER_IN to 0, and SKID_STEER_OUT to 1.](http://ardupilot.org/rover/docs/skid-steer-parameter-tuning.html) 
This will tell the Pixhawk that it will be receiving a mixed signal from the controller, and should be outputting an unmixed signal to the Sabertooth. If this combination doesn't work, try changing the values of SKID_STEER_IN and SKID_STEER_OUT.

To read more about motor mixing, [click here.](link)
To read more about skid steering, [click here.](http://groups.csail.mit.edu/drl/courses/cs54-2001s/skidsteer.html)
To read more about skid steer parameters and tuning, [click here.](http://ardupilot.org/rover/docs/tuning-steering-and-navigation-for-a-rover.html)
To read more about DIP switches, [click here.](https://www.dimensionengineering.com/datasheets/Sabertooth2x12.pdf)

### I can't even arm my rover because my motors go beserk whenever I try.

Before you initially turn on your rover, center both controller sticks.
Your motor controller determines the "neutral" stick configuration from your current stick position when it starts up. If your sticks are completely depressed, the rover will only be able to drive forwards.

### I can't disarm my rover.

Did you use the arm/disarm button under the "Actions" tab in Mission Planner? 
Controller disarming is not currently supported by Ardupilot for ground vehicles.

*This Github page is currently under construction. Last edited on 11/13/16.*
