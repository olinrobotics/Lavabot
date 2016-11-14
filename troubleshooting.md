---
title: Troubleshooting
layout: template
filename: troubleshooting
---

# Index
*[My motors are not responding to the transmitter commands](#my_motors_are_not_responding_to_the_transmitter_commands)*

*[My motors are not obeying the transmitter commands.]()*

*[My motors are obeying the transmitter commands, but they're acting strangely.]()*

*[I can't even arm my rover because my motors go beserk whenever I try.]()*

*[I can't disarm my rover.]()*

### My motors are not responding to the transmitter commands.

Double check the robot. Is it armed? If not, please disengage all safeties and arm the robot before proceeding.

Double check your RC channel mapping, following [these instructions.](http://ardupilot.org/copter/docs/common-radio-control-calibration.html) Olin College uses controller configuration 2, as do most American controllers. You may need to [remap the controls](http://ardupilot.org/copter/docs/common-rcmap.html#common-rcmap) if your RC channels don't correspond to the right configuration in Mission Planner.

If your RC channels are mapped to the correct configuration, check that the battery is plugged in, the robot is on and the power cable leading to the Pixhawk has not slipped out. You should check for loose wires and other anomalous occurences at this time. 

Now check your power supply. Has your emergency switch flipped, cutting current to the motors? Has your fuse blown, cutting current to the motors? Does anything feel warm to the touch? If any component feels hot, turn your robot off immediately and disconnect the battery. You may have an electrical short.

### My motors are not obeying the transmitter commands.

Double check your RC channel mapping, following [these instructions.](http://ardupilot.org/copter/docs/common-radio-control-calibration.html) Olin College uses controller configuration 2, as do most American controllers. You may need to [remap the controls](http://ardupilot.org/copter/docs/common-rcmap.html#common-rcmap) if your RC channels don't correspond to the right configuration in Mission Planner.

### My motors are obeying the transmitter commands, but they're acting strangely.

Double check your RC channel mapping, following [these instructions.](http://ardupilot.org/copter/docs/common-radio-control-calibration.html) Olin College uses controller configuration 2, as do most American controllers. You may need to [remap the controls](http://ardupilot.org/copter/docs/common-rcmap.html#common-rcmap) if your RC channels don't correspond to the right configuration in Mission Planner.

Now check your motor controller. Olin College uses the [Sabertooth 2x12](https://www.dimensionengineering.com/datasheets/Sabertooth2x12.pdf), which has 6 DIP switches that control how it is configured. In order, switches 1-6 should be DOWN, UP, DOWN, DOWN, DOWN, UP. This is because Sam the robot runs on lithium batteries (switch 3), with no special handling like exponential response (switch 5) or 4x sensitivity (switch 6). In addition, it should not be mixing its motor inputs.



### I can't even arm my rover because my motors go beserk whenever I try.

Before you initially turn on your rover, center both controller sticks.
Your motor controller determines the "neutral" stick configuration from your current stick position when it starts up. If your sticks are completely depressed, the rover will only be able to drive forwards.

### I can't disarm my rover.

Did you use the arm/disarm button under the "Actions" tab in Mission Planner? Controller disarming is not currently supported by Ardupilot for ground vehicles.

*This Github page is currently under construction. Last edited on 11/6/16.*
