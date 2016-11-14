import rospy
import wiringpi
from Waypoints import *
from sensors_msgs.msg import Range

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(37,1)

'''make the rover stop immediately '''
def stop_motor():
    clear_waypoints

'''return whether the IR sensor has found the obstacle '''
def find_obstacle(data):
    while getdistance(data) > min_distance:
        pass
    else:
        print 'stop'
        stop_motor
