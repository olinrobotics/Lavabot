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
        self.pub = rospy.Publisher('/obstacle_detection',Bool)

    def infrared_sensing(self):
        '''
        #test if Obstacle detection works by itself
        cur_reading = 0
        while cur_reading<max_reading:
            data = open("../sys/class/saradc/saradc_ch1")
            cur_reading = int(data.read())
            print(cur_reading)
        data.close
        print('Find an obstale!')
        '''
        #Integrate with JoystickSendWaypoint
        data = open("../sys/class/saradc/saradc_ch1")
        cur_reading = int(data.read())
        data.close
        if cur_reading<self.range:
            self.pub.publish(True)
        else:
            self.pub.publish(False)

    def run(self):
        r = rospy.Rate(50)
        while not rospy.is_shutdown():
            self.infrared_sensing()
            r.sleep

if __name__ == '__main__':
    infrared_sensor(800)
