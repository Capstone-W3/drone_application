#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from std_msgs.msg import String
from ardrone_autonomy.msg import Navdata


class AutoFlight():

    def __init__(self):
        self.status = ""
        self.drone_takeoff = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=10)
        self.drone_land = rospy.Publisher('ardrone/land', Empty, queue_size=10)
        self.command = rospy.Publisher('/cmd_vel', Twist, queue_size=10) 
        self.reset = rospy.Publisher('/ardrone/reset', Empty, queue_size=10)
        self.rate=rospy.Rate(10)
        self.sleep_mode= rospy.sleep(10)
        #self.Shutdown_mode = rospy.on_shutdown(self.land_drone)

    def Take_off(self):
        self.drone_takeoff.publish(Empty())
        self.sleep_mode

    def Land (self):
        self.drone_land.publish(Empty())
        self.sleep_mode

    def Reset_drone(self):
        self.reset(Empty())

    def Command_directions(self, lin_x=0,lin_y=0,lin_z=0,ang_x=0,ang_y=0,ang_z=0):
        self.Control = Twist()

        self.Control.linear.x = lin_x 
        self.Control.linear.y = lin_y
        self.Control.linear.z = lin_z
        self.Control.angular.x = ang_x
        self.Control.angular.y = ang_y
        self.Control.angular.z = ang_z
        self.command.publish(self.Control)
        self.rate.sleep()



if __name__== "__main__":

    rospy.init_node('ardrone',anonymous=True)
    drone = AutoFlight()

    forward_dist = 0
    altitude = 0
    try:
       drone.Take_off()
       rospy.sleep(1)
       drone.Command_directions(0,0,0,0,0,0)

       while not rospy.is_shutdown():

            while altitude < 40:
                drone.Command_directions(0,0,1,0,0,0)
                rospy.sleep(1)

            while forward_dist < 15:
                drone.Command_directions(1,0,0,0,0,0)
                rospy.sleep(1)

            drone.Land()           

    except rospy.ROSInterruptException:
             pass

