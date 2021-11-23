#!/usr/bin/env python

import rospy
import serial
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('command', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    s = serial.Serial('/dev/rfcomm1', 115200, timeout=0.01)
    while not rospy.is_shutdown():
        command = ""
        command = s.read()
        if command != "":
            pub.publish(command)
            print(command)
            print(type(command))
    s.close()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
