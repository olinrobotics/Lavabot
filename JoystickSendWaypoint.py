""" Code for communication between Pixhawk and Odroid."""

import rospy
from mavros_msgs.msg import RCIn
from sensor_msgs.msg import NavSatFix
from mavros_msgs.msg import WaypointList
from mavros_msgs.msg import Waypoint
from mavros_msgs.srv import WaypointPush
from mavros_msgs.srv import WaypointPull
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
import sys

# Designated ROS channels
if len(sys.argv)==3:
	thisName = sys.argv[1]
	otherName = sys.argv[2]
elif len(sys.argv)==1 or sys.argv[1]=="/mavros_sam" or sys.argv[1]=="sam":
	thisName = "/mavros_sam"
	otherName = "/mavros_frodo"
else:
	thisName = "/mavros_frodo"
	otherName = "/mavros_sam"
# We must first set the name of the node in node.launch to "mavros_sam"
# vim /opt/ros/indigo/share/mavros/launch/node.launch

# State variables
latitude = 0
longitude = 0
altitude = 0
waypoints = []
alreadyReachedWaypoint = False

# Joystick button
button = 6
lastData = -1

# Constants
WAYPOINT_TOLERANCE = .01

# Methods to send and follow waypoints
def sendWaypoint(clear=False):
	"""Send current location as a waypoint for the other Odroid.

	Keyword arguments:
	clear -- remove all waypoints from other Odroid
	"""
	location = Float64MultiArray()
	if clear:
		publish("Clearing all waypoints on "+otherName)
		location.data = [0]
	else:
		publish("Sending waypoint: ("+str(latitude)+", "+str(longitude)+")")
		location.data = [latitude, longitude]
	publishWaypoint.publish(location)

def addWaypoint(lat, lon, obstacles=False, detour=False, override=False):
	"""Send waypoint from Odroid to Pixhawk.

	Keyword arguments:
	detour -- insert waypoint at beginning of array
	override -- clear previous waypoints)
	"""
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
	waypoint.z_alt = altitude
	publish("Adding waypoint: ("+str(waypoint.x_lat)+", "+str(waypoint.y_long)+")")
	oldWaypoints = waypoints[:]
	publish("Old waypoints: " + str(len(oldWaypoints)))
	if override: result = push([waypoint])
	elif detour: result = push([waypoint]+oldWaypoints)
	else: result = push(oldWaypoints + [waypoint])
	publish("Result: " + str(result))

def reachedWaypoint():
	"""Determine whether the robot is close enough to the current waypoint."""
	if len(waypoints) == 0: return False
	dx = waypoints[0].x_lat-latitude
	dy = waypoints[0].y_long-longitude
	return dx**2+dy**2 <= WAYPOINT_TOLERANCE

def publish(text):
	"""Print message to both console and ROS topic /output."""
	print(text)
	output.publish(thisName+": \t"+text)

# Callback functions for subscribed topics
def joyCallBack(data):
	"""Callback for RC input: calls sendWaypoint function."""
	global lastData
	if len(data.channels) <= button:
		return
	waypoint_data = data.channels[button]
	if lastData == -1:
		lastData = waypoint_data
		return
	# around 1100, 1500, or 1900
	if lastData > 1200 and waypoint_data < 1200:
		sendWaypoint()
	if lastData < 1800 and waypoint_data > 1800:
		sendWaypoint(True)
	lastData = waypoint_data

def gpsCallBack(data):
	"""Callback for GPS location: updates latitude and longitude."""
	global latitude, longitude, alreadyReachedWaypoint
	latitude = data.latitude
	longitude = data.longitude
	if reachedWaypoint():
		if not alreadyReachedWaypoint:
			publish("Reached ("+str(latitude)+", "+str(longitude)+")")
			alreadyReachedWaypoint = True
	else: alreadyReachedWaypoint = False

def altCallBack(data):
	"""Callback for relative altitude: updates altitude."""
	global altitude
	altitude = data.data

def waypointCallBack(data):
	"""Callback for changes to waypoints: updates waypoints list."""
	global waypoints
	waypoints = data.waypoints

def addWaypointCallBack(data):
	"""Callback from other robot: add waypoint to end of list."""
	global waypoints
	if len(data.data)<2:
		publish("Clearing waypoints: " + str(len(waypoints)))
		waypoints = []
		result = push([])
		publish("Result: " + str(result))
	else:
		addWaypoint(*data.data)

def obstacleCallBack(data):
	"""Callback when obstacle is detected: stops the rover."""
	if thisName == "/mavros_sam":
		addWaypoint(latitude, longitude)
		publish("Obstacle detected: stopping rover")

# ROS services and topics
pull = rospy.ServiceProxy(thisName+'/mission/pull',  WaypointPull)
push = rospy.ServiceProxy(thisName+'/mission/push',  WaypointPush)
rospy.init_node('JoystickSendWaypoint_'+thisName[1:])
publishWaypoint = rospy.Publisher(otherName+'/addwaypoint', Float64MultiArray, queue_size=10)
output = rospy.Publisher('/output', String, queue_size=10)
rospy.Subscriber(thisName+'/global_position/global', NavSatFix, gpsCallBack)
rospy.Subscriber(thisName+'/global_position/rel_alt', Float64, altCallBack)
rospy.Subscriber(thisName+'/mission/waypoints', WaypointList, waypointCallBack)
rospy.Subscriber(thisName+'/rc/in', RCIn, joyCallBack)
rospy.Subscriber('/obstacle_detection', Bool, obstacleCallBack)
rospy.Subscriber(thisName+'/addwaypoint', Float64MultiArray, addWaypointCallBack)
publish("This name = " + thisName)
publish("Other name = " + otherName)

# Test code
if __name__ == '__main__':
	#r2 = rospy.Rate(1)
	#r2.sleep()
	#addWaypoint(42,42)
	#r2.sleep()
	#addWaypoint(44,44)
	#r2.sleep()
	#addWaypoint(46,46)
	#r2.sleep()
	#addWaypoint(48,48)
	r = rospy.Rate(10)
	while not rospy.is_shutdown():
		r.sleep()
