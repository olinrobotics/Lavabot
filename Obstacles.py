'''
Key issues regardign mounting the sensor:
1. When measuring objects in motion, align the sensor so that the motion is
    in horizontal direction instead of vertical.
2. Sources of high ambient light(such as sun light) may affect measurement so
    mounting should be designed to avoid interference with direct sunlight.
code for obstacle avoidance with IR sensor
'''
import os

def infrared_sensor(max_reading):
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
    if cur_reading<max_reading:
        return True

'''infrared_sensor(800)'''
