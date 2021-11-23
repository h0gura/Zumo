#!/usr/bin/env python

import rospy
#from std_msgs.msg import String
from geometry_msgs.msg import Twist

import pygame
from pygame.locals import *
import time


class joyconController:
    def __init__(self):
        # initilize ros_node
        rospy.init_node('joycon_node', anonymous=True)
        self.twist_pub = rospy.Publisher('command', Twist, queue_size=10)
        rospy.Timer(rospy.Duration(0.5), self.timerCallback)

        # joy-con
        pygame.joystick.init()
        try:
            self.joystick0 = pygame.joystick.Joystick(0)
            self.joystick0.init()
            print("initialize successfully!")
        except pygame.error:
            print("joystick is not connected")
        

        pygame.init()
        self.joystick_x = 0
        self.joystick_y = 0

        self.coef_linearx = 1
        self.coef_angularz = 1

        self.twist = Twist()
        self.twist.linear.x = 0.0
        self.twist.linear.y = 0.0
        self.twist.linear.z = 0.0
        self.twist.angular.x = 0.0
        self.twist.angular.y = 0.0
        self.twist.angular.z = 0.0

        self.twist_pub.publish(self.twist)


    def timerCallback(self, event):
        #command = ""
        eventlist = pygame.event.get()

        for e in eventlist:
            if e.type == QUIT:
                return
            if e.type == pygame.locals.JOYBUTTONDOWN:
                #print(e.buttono)
                if e.button == 2:   # forward
                    #command = "f"
                    self.twist.linear.x = 1
                elif e.button == 1: # backward
                    #command = "b"
                    self.twist.linear.x = -1
                elif e.button == 0: # left
                    #command = "l"
                    self.twist.linear.y = 1
                elif e.button == 3: # right 
                    #command = "r"
                    self.twist.linear.y = -1
            elif e.type == pygame.locals.JOYHATMOTION:
                self.joystick_x, self.joystick_y = self.joystick0.get_hat(0)
                self.twist.linear.x = -1 * self.joystick_x
                self.twist.linear.y = -1 * self.joystick_y
                print(self.joystick_x, self.joystick_y)

        #if command != "":
        #    self.twist_pub.publish(command)
        #    print(command)
        #    print(type(command))

        self.twist_pub.publish(self.twist)
        print(self.twist)

if __name__ == '__main__':
    try:
        jc = joyconController()
        rospy.spin()
    except pygame.error:
        print("Cannot find Joy-Con")
    except rospy.ROSInterruptException:
        print("something error")
        pass
