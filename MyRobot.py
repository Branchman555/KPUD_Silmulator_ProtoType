import cv2
import random
import pandas as pd
import numpy as np
from numpy.random import randn
from scipy.stats import bernoulli
import threading
import math

from time import sleep

# calculate relative degree
def calreldeg(src_deg, tar_deg):
    rel_deg = tar_deg - src_deg
    if rel_deg > 180:
        rel_deg -= 360
    elif rel_deg < -180:
        rel_deg += 360
    return rel_deg


BACKGROUND_PATH = './images/bg.jpg'

def stt():
    img = cv2.imread(BACKGROUND_PATH)
    while 1:
        cv2.imshow('default', img)
        cv2.waitKey(30)

class SimulWindow:
    __default_width = 512
    __default_height = 512
    __default_x = 400
    __default_y = 400
    __default_version = 0.1
    __default_background = cv2.imread(BACKGROUND_PATH)
    __default_win = __default_background[
                    __default_y:__default_y + __default_height,
                    __default_x:__default_x + __default_width]

    def __init__(self, name='default'):
        self.__width = SimulWindow.__default_width
        self.__height = SimulWindow.__default_height
        self.__winname = name
        #self.__img = SimulWindow.__default_win
        self.__img = cv2.imread(BACKGROUND_PATH)
        self.winstopflag = False
        cv2.namedWindow(self.__winname)
        #cv2.resizeWindow(self.__winname, (200, 200))

    def tempshow(self):
        cv2.imshow(self.__winname, self.__img)
        cv2.waitKey(50)
    def showwindow(self):
        print(self.winstopflag)
        while self.winstopflag is False:
        #while 1:
            cv2.imshow(self.__winname, self.__img)
            cv2.waitKey(50)
        print("outto!!!")
        cv2.destroyWindow('default')

    def startwindow(self):
        # thread = threading.Thread(target=Robot.sm.showwindow)
        thread = threading.Thread(target=self.showwindow)
        thread.daemon = True
        thread.start()

    def resetwindow(self):
        self.__width = SimulWindow.__default_width
        self.__height = SimulWindow.__default_height
        self.__img = SimulWindow.__default_win

    def setwindowname(self, winname):
        self.__winname = winname

    def getwindowname(self):
        return self.__winname

    def setsize(self, width, height):
        self.__width = width
        self.__height = height

    def getsize(self):
        return self.__width, self.__height


class Robot:
    __robot_num = 0
    __sm = SimulWindow()

    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__angle = 0
        self.__color = (255, 255, 255)
        self.__version = 0.1
        Robot.__robot_num += 1

    def startwindow(self):
        thread = threading.Thread(target=Robot.__sm.showwindow)
        #thread = threading.Thread(target=stt)
        thread.daemon = True
        thread.start()

    def closewindow(self):
        Robot.__sm.winstopflag = True
        cv2.destroyWindow(Robot.__sm.getwindowname())

    def showrobotnum(self):
        print(Robot.__robot_num)

    def goto(self, tar_x, tar_y):
        self.__x = tar_x
        self.__y = tar_y

    def position(self):
        return self.__x, self.__y

    def setcolor(self, bgrcode_b, bgrcode_g, bgrcode_r):
        self.__color = (bgrcode_b, bgrcode_g, bgrcode_r)

    def getcolor(self):
        return self.__color

    def setangle(self, tar_angle):
        self.__angle = tar_angle

    def getangle(self):
        return self.__angle

    def calangle(self, tar_point_x=0, tar_point_y=0):
        relative_loc = (tar_point_x - self.__x, tar_point_y - self.__y)
        resdeg = 0
        if relative_loc[0] == 0:
            if relative_loc[1] == 0:
                resdeg = 0
            elif relative_loc[1] > 0:
                resdeg = 90
            elif relative_loc[1] < 0:
                resdeg = 270
        elif relative_loc[1] == 0:
            if relative_loc[0] > 0:
                resdeg = 0
            elif relative_loc[0] < 0:
                resdeg = 180
        else:
            resdeg += math.degrees(math.atan(relative_loc[1] / relative_loc[0]))

        if relative_loc[0] > 0 and relative_loc[1] > 0:
            pass
        elif relative_loc[0] < 0 and relative_loc[1] > 0:
            resdeg += 180
        elif relative_loc[0] < 0 and relative_loc[1] < 0:
            resdeg += 180
        elif relative_loc[0] > 0 and relative_loc[1] < 0:
            resdeg += 360
        return resdeg

    def show_version(self):
        print(self.__version)


if __name__ == "__main__":
    img = cv2.imread(BACKGROUND_PATH)
    cv2.imshow('default', img)
    cv2.waitKey(30)
    myRobot1 = Robot()
    myRobot1.showrobotnum()
    myRobot2 = Robot()
    myRobot1.showrobotnum()
    myRobot2.showrobotnum()

    # sm = SimulWindow()
    # sm.startwindow()
    myRobot1.startwindow()

    myRobot3 = Robot()
    myRobot3.showrobotnum()
    sleep(4)
    #myRobot1.sm.tempshow()
    myRobot1.closewindow()
    sleep(5)
    myRobot4 = Robot()
    myRobot4.showrobotnum()




    # myRobot = Robot()
    #
    # print(myRobot.position())
    # myRobot.goto(0, 0)
    # print(myRobot.position())
    #
    # myRobot.show_version()
    #
    # print(myRobot.calangle(1, 1))
    # myRobot.setangle(myRobot.calangle(1, 1))
    #
    # print(calreldeg(myRobot.getangle(), 200))
    # myRobot.setangle(calreldeg(myRobot.getangle(), 200) + myRobot.getangle())
    #
    # print(calreldeg(myRobot.getangle(), 200))
