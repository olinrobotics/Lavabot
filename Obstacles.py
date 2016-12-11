import rospy
import wiringpi
from Waypoints import *
from sensors_msgs.msg import Range
from Guided import *
from OdroidToPixhark import *

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(37,1)
min_distance = 100

'''stop the rover by setting and pushing a waypoint at the current location'''
def stop_motor(lat,lon,alt=DEFAULT_ALT):
    stoppoint = Waypoints.gps_callback()
    Guided.set_guided_waypoint(stoppoint.lat,stoppoint.lon,stoppoint.alt)

'''sense obstacle with IR sensor'''
def find_obstacle():
    while wiringpi.analogRead(0) > min_distance:
        pass
    else:
        print 'stop'
        stop_motor()
