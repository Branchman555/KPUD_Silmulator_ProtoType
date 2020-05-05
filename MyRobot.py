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

ROBOT_SHAPE_TRI = 1
ROBOT_SHAPE_CIR = 2

BACKGROUND_PATH = './images/bg_1.jpg'
BG_WIDTH = 1024
BG_HEIGHT = 1024

referenceOrigin = (126.730667, 37.342222)

class SimulWindow:
    __default_width = 512
    __default_height = 512
    __default_x = 400
    __default_y = 400
    __default_version = 0.1
    __default_background = cv2.resize(cv2.imread(BACKGROUND_PATH), (BG_WIDTH, BG_HEIGHT), interpolation=cv2.INTER_CUBIC)
    __default_win = __default_background[
                    __default_y:__default_y + __default_height,
                    __default_x:__default_x + __default_width].copy()

    def __init__(self, name='default'):
        self.__width = SimulWindow.__default_width
        self.__height = SimulWindow.__default_height
        self.__x = self.__default_x
        self.__y = self.__default_y
        self.__winname = name
        self.__img = SimulWindow.__default_win
        self.__winstopflag = True
        cv2.namedWindow(self.__winname)
        #cv2.resizeWindow(self.__winname, (200, 200))

    def tempshow(self):
        cv2.imshow(self.__winname, self.__img)
        cv2.waitKey(50)

    def writewindow(self):
        SimulWindow.__default_background[self.__y:self.__y + self.__height, self.__x:self.__x + self.__width] = self.__img.copy()

    # def getwindow(self):
    #     return self.__img

    def getwindow(self):
        self.__img = SimulWindow.__default_background[self.__y:self.__y + self.__height,
                                                        self.__x:self.__x + self.__width].copy()
        return self.__img

    def showwindow(self):
        while self.__winstopflag is False:
        #while 1:
            cv2.imshow(self.__winname, self.__img)
            cv2.waitKey(50)
        print("outto!!!")
        cv2.destroyWindow('default')

    def resetwindow(self):
        self.__width = SimulWindow.__default_width
        self.__height = SimulWindow.__default_height
        self.__img = SimulWindow.__default_win

    def startwindow(self):
        self.tempshow()
        print("called st_win")
        if self.__winstopflag:
            self.__winstopflag = False
            print("window start")
            thread = threading.Thread(target=self.showwindow)
            # thread = threading.Thread(target=stt)
            thread.daemon = True
            thread.start()

    def closewindow(self):
        self.__winstopflag = True
        cv2.destroyWindow(self.getwindowname())

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
    __robotShape = ROBOT_SHAPE_TRI

    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__angle = 0
        self.__shape = np.zeros([20,20,3])
        #cv2.copyTo(Robot.__robotShapeTri, self.__shape)
        self.__color = (255, 255, 255)
        self.__thickness = 2
        self.__drawflag = False

        self.__version = 0.1
        Robot.__sm.startwindow()
        Robot.__robot_num += 1

    def endsimul(self):
        Robot.__sm.closewindow()

    def showrobotnum(self):
        print(Robot.__robot_num)

    def drawon(self):
        self.__drawflag = True
        self.drawRobot()

    def drawoff(self):
        self.__drawflag = False

    def goto(self, tar_x, tar_y):
        bef_x = self.__x
        bef_y = self.__y
        self.__x = tar_x
        self.__y = tar_y
        self.drawRobot()
        if self.__drawflag:
            Robot.__sm.writewindow()
            access_img = Robot.__sm.getwindow()
            cv2.line(access_img, (bef_x, bef_y), (self.__x, self.__y), self.__color, self.__thickness)
            Robot.__sm.writewindow()

    def forward(self, distance):
        pass

    def position(self):
        return self.__x, self.__y

    def setcolor(self, bgrcode_b, bgrcode_g, bgrcode_r):
        self.__color = (bgrcode_b, bgrcode_g, bgrcode_r)

    def getcolor(self):
        return self.__color

    def drawRobot(self):
        access_img = Robot.__sm.getwindow()
        cv2.circle(access_img, (self.__x, self.__y), 5, self.__color, self.__thickness)

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
    myRobot1 = Robot()
    myRobot1.goto(50, 50)
    myRobot1.setcolor(150, 0, 40)
    myRobot1.drawon()
    myRobot1.showrobotnum()
    myRobot2 = Robot()
    myRobot1.showrobotnum()
    myRobot2.showrobotnum()

    # sm = SimulWindow()
    # sm.startwindow()
    myRobot3 = Robot()
    myRobot3.showrobotnum()
    x, y = myRobot1.position()
    while 1:
        key = cv2.waitKey(20)
        if key == ord('a'):
            print('a')
            x -= 10
            myRobot1.goto(x, y)
        if key == ord('d'):
            print('d')
            x += 10
            myRobot1.goto(x, y)
        if key == ord('w'):
            print('w')
            y -= 10
            myRobot1.goto(x, y)
        if key == ord('s'):
            print('s')
            y += 10
            myRobot1.goto(x, y)
        if key == ord('x'):
            break

    myRobot1.endsimul()
    sleep(1)
    #myRobot4 = Robot()
    #myRobot4.showrobotnum()




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
