import rospy
import rospkg

from sensor_msgs.msg import Image
from std_msgs.msg import String

import numpy as np
import cv2
import time

class IRVideoDetect:

    def __init__(self,cap):
        rospy.init_node('IR_Video_detect',anonymous=True)
        self.pub = rospy.Publisher('/IR_video_detect',String,queue_size=100)
        #rospy.Subscriber('/usb_camera',Image,self.video_callback)
        self.cap = cap

    def video_callback(self,data):
        pass

    def color_detect(self):
        while True:
            ret,frame = self.cap.read()
            imhsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            lower_range = np.array([125, 80, 80], dtype=np.uint8)
            upper_range = np.array([255, 255, 255], dtype=np.uint8)
            mask = cv2.inRange(imhsv,lower_range,upper_range)
            ret,thresh = cv2.threshold(mask,127,155,1)
            contours,h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            max_area = 0
            for cnt in contours:
                approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
                area = cv2.contourArea(approx)
                if area > max_area and area < 250000:
                    max_area = area
                    max_contour = cnt
            cv2.drawContours(frame,[max_contour],0,(0,255,0),2)
            if cv2.contourArea(max_contour)>15000:
                self.pub.publish('Find an Obstale')
            cv2.imshow('mask',mask)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        r = rospy.Rate(2)
        time.sleep(2)
        while not rospy.is_shutdown():
            self.color_detect()
            r.sleep

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    od = IRVideoDetect(cap)
    od.run()
