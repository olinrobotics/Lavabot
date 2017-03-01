''' This script is a GUI to display Odroid information for Lavabot, including:
Video from camera ?, 
altitude, 
perceived GPS location, 
current behavior'''

from Tkinter import * # GUI module
import rospy
from sensor_msgs.msg import NavSatFix
from mavros_msgs.msg import WaypointList
from mavros_msgs.msg import Waypoint
from std_msgs.msg import String, Float64, Float64MultiArray
import os


def gpsCallBack(msg):
	GPS_pos.set('lat: '+str(msg.latitude)+', long: '+str(msg.longitude))
def waypointCallBack(msg):
	pass 
def altCallBack(msg):
	altitude.set(msg.data)

rospy.init_node('OdroidGUI')
rospy.Subscriber('/mavros/global_position/global', NavSatFix, gpsCallBack)
rospy.Subscriber('/mavros/mission/waypoints', WaypointList, waypointCallBack)
rospy.Subscriber('/mavros/global_position/rel_alt', Float64, altCallBack)
root = Tk()
root.title("Odroid GUI")

mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

behavior = StringVar()
GPS_pos = StringVar()
altitude = StringVar()

behavior.set('ready')
GPS_pos.set('30, 20')
altitude.set('10')


def update(*args):
	pass

Label(mainframe, text="altitude").grid(column=1, row=1, sticky=W)
Label(mainframe, textvariable=altitude).grid(column=2, row=1, sticky=(W, E))
Label(mainframe, text="GPS position").grid(column=1, row=2, sticky=W)
Label(mainframe, textvariable=GPS_pos).grid(column=2, row=2, sticky=(W, E))
Label(mainframe, text="Current Behavior").grid(column=1, row=3, sticky=W)
Label(mainframe, textvariable=behavior).grid(column=2, row=3, sticky=(W, E))

Button(mainframe, text="Update", command=update).grid(column=3, row=4, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)


root.bind('<Return>', update)

root.mainloop()


# feet_entry.focus()
# feet_entry = Entry(mainframe, width=7, textvariable=feet)
# feet_entry.grid(column=2, row=1, sticky=(W, E))
# def calculate(*args):
#     try:
#         value = float(feet.get())
#         meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
#     except ValueError:
#         pass