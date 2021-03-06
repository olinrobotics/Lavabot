#!/usr/bin/env python
""" Sends waypoint from PixHawk to Odroid """

import rospy
from sensor_msgs.msg import NavSatFix
from mavros_msgs.msg import BatteryStatus

latitude = 0
longitude = 0
waypoint = None

def gpsCallBack(data):
	latitude = data.latitude
	longitude = data.longitude
	print 'gps position = ' + str(latitude) + ', ' + str(longitude)

def waypointCallBack(data):
	waypoint = data[0]
	print 'waypoint = ' + str(waypoint)

def sendWaypointToGroundVehicle():
	#send latitude/longitude or waypoint to pixhawk
	pass

rospy.init_node('PixhawkToOdroid')
rospy.Subscriber('/mavros/global_position/global', NavSatFix, gpsCallBack)
rospy.Subscriber('/mavros/mission/waypoints', NavSatFix, waypointCallBack)
r = rospy.Rate(1)
while not rospy.is_shutdown():
    r.sleep()
