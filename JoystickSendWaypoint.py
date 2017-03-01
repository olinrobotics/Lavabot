""" Code for communication between Pixhawk and Odroid. """

import rospy
from mavros_msgs.msg import RCIn
from sensor_msgs.msg import NavSatFix
from mavros_msgs.msg import WaypointList
from mavros_msgs.msg import Waypoint
from mavros_msgs.srv import WaypointPush
from mavros_msgs.srv import WaypointPull
from std_msgs.msg import Bool
import os
from Obstacles import infrared_sensor

# State
latitude = 0
longitude = 0
waypoints = []
odetect = False

# Joystick button
button = 5
lastData = -1

# Services
pull = rospy.ServiceProxy('/mavros/mission/pull',  WaypointPull)
push = rospy.ServiceProxy('/mavros/mission/push',  WaypointPush)

# Callback for RC input
def joyCallBack(data):
	global lastData
	waypoint_data = data.channels(button)
	# around 1100, 1500, or 1900
	if lastData>0 and abs(lastData - waypoint_data) > 300:
		sendWaypoint()
	lastData = waypoint_data

# Callback for GPS location
def gpsCallBack(data):
	global latitude, longitude
	latitude = data.latitude
	longitude = data.longitude

# Callback for changes to waypoints
def waypointCallBack(data):
	global waypoints
	waypoints = data.waypoints

def irSensorCallback(data):
	global odetect
	odetect = data

# Send waypoint to other Odroid
def sendWaypoint():
	print('Sending waypoint: ('+str(latitude)+', '+str(longitude)+")")
	addWaypoint(latitude, longitude)
	# TODO: send latitude/longitude to other odroid instead

# Send waypoint to Pixhawk
def addWaypoint(lat, lon):
	waypoint = Waypoint()
	waypoint.frame = 3
	waypoint.command = 16
	waypoint.is_current = 0
	waypoint.autocontinue = True
	waypoint.param1 = 0 #hold time
	waypoint.param2 = 2 #acceptance radius (m)
	waypoint.param3 = 0
	waypoint.param4 = 0
	waypoint.x_lat = lat
	waypoint.y_long = lon
	waypoint.z_alt = 0
	print("Adding waypoint: ("+str(waypoint.x_lat)+", "+str(waypoint.y_long)+")")
	oldWaypoints = waypoints[:]
	print("Old waypoints: " + str(len(oldWaypoints)))
	#result = push(oldWaypoints + [waypoint])
	#print(result)

def Obstacle_detection(lat,lon,dis):
	#This is not useful anymore
	global latitude, longitude
	while (latitude != lat) and (longitude !=lon) and infrared_sensor(dis):
		pass
	if infrared_sensor(dis) == False:
		addWaypoint(latitude, longitude)

# ROS topics
rospy.init_node('JoystickSendWaypoint')
rospy.Subscriber('/mavros/global_position/global', NavSatFix, gpsCallBack)
rospy.Subscriber('/mavros/mission/waypoints', WaypointList, waypointCallBack)
rospy.Subscriber('/mavros/rc/in', RCIn, joyCallBack)
rospy.Subscriber('/obstacle_detection',Bool,irSensorCallback)

# Test code
if __name__ == '__main__':
	r = rospy.Rate(10)
	r2 = rospy.Rate(1)
	r2.sleep()
	addWaypoint(42,42)
	Obstacle_detection(42,42,800)
	r2.sleep()
	addWaypoint(44,44)
	Obstacle_detection(44,44,800)
	r2.sleep()
	addWaypoint(46,46)
	Obstacle_detection(46,46,800)
	r2.sleep()
	addWaypoint(48,48)
	Obstacle_detection(48,48,800)
	while not rospy.is_shutdown():
		r.sleep() # wait for input
