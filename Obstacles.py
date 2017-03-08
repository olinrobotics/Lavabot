'''
Key issues regardign mounting the sensor:
1. When measuring objects in motion, align the sensor so that the motion is
    in horizontal direction instead of vertical.
2. Sources of high ambient light(such as sun light) may affect measurement so
    mounting should be designed to avoid interference with direct sunlight.
code for obstacle avoidance with IR sensor
'''
import rospy
import rospkg

from std_msgs.msg import Bool

import os

class Obstacle_detection:

    def __init__(self):
        self.range = 800
        rospy.init_node('Obstacle_detect',anonymous=True)
        self.pub = rospy.Publisher('/obstacle_detection',Bool,queue_size=100)
        print 'Obstacle Detection is Running'

    def infrared_sensing(self):
        #Integrate with JoystickSendWaypoint
        data = open("../sys/class/saradc/saradc_ch1")
        cur_reading = int(data.read())
        data.close
        if cur_reading<self.range:
            self.pub.publish(True)
        else:
            self.pub.publish(False)

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            self.infrared_sensing()
            r.sleep

if __name__ == '__main__':
    od = Obstacle_detection()
    od.run()
