import rospy
from sensor_msgs.msg import NavSatFix

latitude = 0;
longitude = 0;

rospy.Subscriber('/global_position/global', NavSatFix, gpsCallBack)

def gpsCallBack(data):
        latitude = data.latitude
        longitude = data.longitude
	print 'gps position = ' + str(latitude) + ', ' + str(longitude)

def sendWaypointToGroundVehicle()
	pixhawkToPixhawk(latitude, longitude)

def pixhawkToPixhawk(latitude, longitude)
	# This is another task


