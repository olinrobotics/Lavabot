import rospy
import wiringpi
from Waypoints import *
from sensors_msgs.msg import Range

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(37,1)
min_distance = 100

'''stop the rover by setting and pushing a waypoint at the current location'''
def stop_motor():
    stoppoint = gps_callback()
    make_global_waypoint(stoppoint.latitude,stoppoint.longitude)
    push_waypoints

'''sense obstacle with IR sensor'''
def find_obstacle():
    while wiringpi.analogRead(0) > min_distance:
        pass
    else:
        print 'stop'
        stop_motor();
