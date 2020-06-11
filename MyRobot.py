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

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
        self.__x_para = self.__default_x
        self.__y_para = self.__default_y
        self.__winname = name
        self.__img = SimulWindow.__default_win
        self.__winstopflag = True
        self.__endstayflag = False
        cv2.namedWindow(self.__winname)
        #cv2.resizeWindow(self.__winname, (200, 200))

    def writewindow(self):
        SimulWindow.__default_background[self.__y:self.__y + self.__height, self.__x:self.__x + self.__width] = self.__img.copy()

    # def getwindow(self):
    #     return self.__img

    def movewindow(self, x, y):
        self.__x_para += x
        self.__y_para += y
        if 0 < self.__x_para < BG_WIDTH - self.__width:
            self.__x += x
        if 0 < self.__y_para < BG_HEIGHT - self.__height:
            self.__y += y
        self.getwindow()

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

    def resetwindow(self):
        self.__width = SimulWindow.__default_width
        self.__height = SimulWindow.__default_height
        self.__img = SimulWindow.__default_win

    def startwindow(self):
        cv2.imshow(self.__winname, self.__img)
        print("called st_win")
        if self.__winstopflag:
            self.__winstopflag = False
            print("window start")
            thread = threading.Thread(target=self.showwindow)
            # thread = threading.Thread(target=stt)
            thread.daemon = True
            thread.start()

    def endwindow(self):
        self.__winstopflag = True
        if self.__endstayflag is False:
            self.closewindow()

    def closewindow(self):
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

    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__angle = 0
        self.__shape = "circle"
        self.__speed = 3
        #cv2.copyTo(Robot.__robotShapeTri, self.__shape)
        self.__color = BLACK
        self.__thickness = 1
        self.__drawflag = False
        self.__lineflag = False

        self.__version = 0.1
        Robot.__sm.startwindow()
        Robot.__robot_num += 1

    def endsimul(self):
        Robot.__sm.endwindow()

    def showrobotnum(self):
        print(Robot.__robot_num)

    def setshape(self, str):
        self.__shape = str

    def drawon(self):
        self.__drawflag = True
        self.__lineflag = True
        self.drawRobot()

    def drawoff(self):
        self.__drawflag = False
        self.__lineflag = False

    def dot(self, dot_size, color):
        access_img = Robot.__sm.getwindow()
        cv2.circle(access_img, (self.__x, self.__y), dot_size, color, -1)
        Robot.__sm.writewindow()

    def circle(self, circle_size):
        access_img = Robot.__sm.getwindow()
        cv2.circle(access_img, (self.__x, self.__y), circle_size, self.__color, self.__thickness)
        Robot.__sm.writewindow()

    def drawRobot(self):
        access_img = Robot.__sm.getwindow()
        cv2.circle(access_img, (self.__x, self.__y), int(self.__thickness / 2), self.__color, -1)
        if self.__drawflag:
            Robot.__sm.writewindow()


    def lineon(self):
        self.__lineflag = True

    def lineoff(self):
        self.__lineflag = False

    def setspeed(self, speed):
        self.__speed = speed

    def goto(self, tar_x, tar_y):
        bef_x = self.__x
        bef_y = self.__y
        self.__x = int(tar_x)
        self.__y = int(tar_y)
        self.drawRobot()
        if self.__drawflag:
            if self.__lineflag:
                access_img = Robot.__sm.getwindow()
                cv2.line(access_img, (bef_x, bef_y), (self.__x, self.__y), self.__color, self.__thickness)
                Robot.__sm.writewindow()

        if self.__speed:
            cv2.waitKey(50 * self.__speed)

    def forward(self, distance):
        radian = math.radians(self.__angle)
        self.goto(self.__x + int(distance * math.cos(radian)), self.__y + int(distance * math.sin(radian)))

    def position(self):
        return self.__x, self.__y

    def distance(self, node):
        return math.sqrt((self.__x - node[0])**2 + (self.__y - node[1])**2)

    def setsize(self, thickness):
        self.__thickness = thickness

    def setcolor(self, BGR_Code):
        self.__color = BGR_Code

    def getcolor(self):
        return self.__color

    def setangle(self, tar_angle):
        self.__angle = tar_angle
        #angle is Degree

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

    def diffangle(self, tar_angle):
        diff = tar_angle - self.__angle
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        return diff

    def addangle(self, angle):
        res = self.getangle() + angle
        if res >= 360:
            res -= 360
        elif res < 0:
            res += 360
        self.setangle(res)

    def show_version(self):
        print(self.__version)


def cal_line_equ(nodes):
    equation = [0]
    for i in range(len(nodes) - 1):
        if nodes[i][1] - nodes[i + 1][1] == 0:
            val_a = 0
            val_b = 1
            val_c = -1 * nodes[i][1]
        elif nodes[i][0] - nodes[i + 1][0] == 0:
            val_a = 1
            val_b = 0
            val_c = -1 * nodes[i][0]
        else:
            val_a = nodes[i][1] - nodes[i + 1][1]
            val_b = nodes[i + 1][0] - nodes[i][0]
            val_c = nodes[i][0] * nodes[i + 1][1] - nodes[i + 1][0] * nodes[i][1]
            if val_a < 0:
                val_a *= -1
                val_b *= -1
                val_c *= -1
        equation.append((val_a, val_b, val_c))
    return equation

def cal_point_line(point, line):
    d = abs(line[0] * point[0] + line[1] * point[1] + line[2])/math.sqrt(line[0]**2 + line[1]**2)
    return d

if __name__ == "__main__":

    t_GPS = Robot()
    t = Robot()
    t_GPS.setcolor(RED)
    t_GPS.drawoff()
    t.setshape("triangle")

    t.setspeed(1)
    t_GPS.setspeed(1)
    mark_radius = 20

    GPS_ERR_VAL = 20
    ANG_ERR_VAL = 1
    VEL_ERR_VAL = 0.2
    NODE_CORR = 0.8

    GPS_WEIGHT = 0.2
    ROUTE_WIDTH = 16

    nodes = [(200, 200), (100, 100), (100, 200), (200, 300), (300, 100)]

    lines = cal_line_equ(nodes)
    print(lines)

    t_GPS.setsize(ROUTE_WIDTH)

    t_GPS.setcolor(GREEN)
    for index, node in enumerate(nodes):
        t.goto(node[0], node[1])
        t_GPS.goto(node[0], node[1])
        t_GPS.drawon()
        t.drawon()
        #t.write(str(index))
        t.circle(mark_radius)

    t.drawoff()
    t_GPS.drawoff()

    t.setspeed(0)
    t_GPS.setspeed(0)

    t.setsize(4)
    t.setcolor(BLACK)
    t_GPS.setcolor(RED)
    t_GPS.setsize(1)
    t_GPS.goto(t.position()[0], t.position()[1])
    t.drawon()
    t_GPS.drawoff()

    for index, node in enumerate(nodes):
        if index == 0:
            t.drawoff()
            t_GPS.drawoff()
            t.goto(node[0], node[1])
            t_GPS.goto(node[0], node[1])
            t.drawon()
            continue

        delta = 0
        err_count = 0
        arrival_count = 0
        vision_count = 0
        vision_angle = 0

        # 초기 방향 잡아주기 및 카운트 초기화
        target_tilt = t_GPS.calangle(node[0], node[1])
        t.setangle(target_tilt + randn() * ANG_ERR_VAL)
        t_GPS.setangle(target_tilt + randn() * ANG_ERR_VAL)
        corr_angle_vis = 0
        while 1:
            # 오류와 사기가 판치는 공간의 시작
            # head = bernoulli.rvs(0.5)
            # if head is 1:
            #     rnd = random.randint(-30, 30)
            #     t.right(rnd)
            #     t_GPS.right(rnd + randn() * ANG_ERR_VAL)

            # 카운트에 맞춰서 점찍기, 랜덤 오류발생
            if err_count % 4 is 0:
                err_GPS = (t.position()[0] + randn() * GPS_ERR_VAL, t.position()[1] + randn() * GPS_ERR_VAL)
                cor_GPS = (GPS_WEIGHT * err_GPS[0] + (1 - GPS_WEIGHT) * t_GPS.position()[0],
                           GPS_WEIGHT * err_GPS[1] + (1 - GPS_WEIGHT) * t_GPS.position()[1])

                t_GPS.goto(err_GPS[0], err_GPS[1])
                t_GPS.dot(2, RED)

                t_GPS.goto(cor_GPS[0], cor_GPS[1])
                t_GPS.dot(4, BLUE)

            t_GPS.setangle(t.getangle())
            if t_GPS.distance(node) < mark_radius:
                arrival_count += 1
                if arrival_count > 3:
                    t.forward(3)
                    t_GPS.forward(3 + randn() * VEL_ERR_VAL)
                    arrival_count = 0
                    t_GPS.goto((1 - NODE_CORR) * err_GPS[0] + NODE_CORR * node[0],
                               (1 - NODE_CORR) * err_GPS[1] + NODE_CORR * node[1])
                    break
            # 오류와 사기가 판치는 공간의 끝

            # 각도 변경파트: GPS 기반
            target_tilt = t.calangle(node[0], node[1])
            print("tar_tilt : " + str(target_tilt))
            tar_angle = t.diffangle(target_tilt)
            print("tar_angle : " + str(tar_angle))
            # 랜덤 자율주행
            if vision_count > 4:
                vision_count = 0
                vision_angle = tar_angle + randn() * 20

                head = bernoulli.rvs(0.5)
                if head is 1:
                    rnd = random.randint(-30, 30)
                    vision_angle += rnd

                head = bernoulli.rvs(0.5)
                if head is 1:
                    delta = 1
                else:
                    delta = -1

            # 자율주행 각도 보정
            #corr_angle_vis = 0
            if vision_angle > 0:
                if vision_angle > 30:
                    corr_angle_vis = 15
                else:
                    corr_angle_vis = 5
            elif vision_angle < 0:
                if vision_angle < -30:
                    corr_angle_vis = -15
                else:
                    corr_angle_vis = -5
            corr_angle_vis += delta * 2

            # GPS 각도 보정
            corr_angle_gps = 0
            if tar_angle > 0:
                if tar_angle > 45:
                    corr_angle_gps = 35
                elif tar_angle > 15:
                    corr_angle_gps = 25
                else:
                    corr_angle_gps = 18
            elif tar_angle < 0:
                if tar_angle < -45:
                    corr_angle_gps = -35
                elif tar_angle < -15:
                    corr_angle_gps = -25
                else:
                    corr_angle_gps = -18

            dist_route = cal_point_line(t_GPS.position(), lines[index])
            if dist_route < ROUTE_WIDTH / 2:
                t.addangle(corr_angle_vis)
                t_GPS.addangle(corr_angle_vis + randn() * ANG_ERR_VAL)
                print("t.angle : " + str(t.getangle()))
                print("mode : vision")
            else:
                t.addangle(corr_angle_gps)
                t_GPS.addangle(corr_angle_gps + randn() * ANG_ERR_VAL)
                print("t.angle : " + str(t.getangle()))
                print("mode : GPS filter")

            # 랜덤 속도 감속
            head = bernoulli.rvs(0.1)
            if head is 1:
                t.forward(3)
                t_GPS.forward(3 + randn() * VEL_ERR_VAL)
            else:
                t.forward(9)
                t_GPS.forward(9 + randn() * VEL_ERR_VAL)

            if err_count % 20 is 0:
                # t.write(str(round(t.distance(t_GPS.position()), 2)))
                print("ED : ", str(t.distance(t_GPS.position())))
            err_count += 1
            vision_count += 1



    # myRobot1 = Robot()
    # myRobot1.setcolor(150, 0, 40)
    # #myRobot1.drawon()
    # myRobot1.goto(50, 50)
    #
    #
    # myRobot1.showrobotnum()
    # myRobot2 = Robot()
    # myRobot1.showrobotnum()
    # myRobot2.showrobotnum()
    #
    # # sm = SimulWindow()
    # # sm.startwindow()
    # myRobot3 = Robot()
    # myRobot3.showrobotnum()
    # while 1:
    #     key = cv2.waitKey(20)
        # if key == ord('a'):
        #     print('a')
        #     myRobot1.setangle(180)
        #     myRobot1.forward(50)
        # if key == ord('d'):
        #     print('d')
        #     myRobot1.setangle(0)
        #     myRobot1.forward(50)
        # if key == ord('w'):
        #     print('w')
        #     myRobot1.setangle(90)
        #     myRobot1.forward(50)
        # if key == ord('s'):
        #     print('s')
        #     myRobot1.setangle(270)
        #     myRobot1.forward(50)
        # if key == ord('x'):
        #     break

        # if key == ord('y'):
        #     myRobot1.drawon()
        #
        # if key == ord('z'):
        #     myRobot1.lineon()
        #
        # if key == ord('p'):
        #     myRobot1.lineoff()
        #
        # if key == ord('o'):
        #     myRobot1.drawoff()
    cv2.waitKey(0)
    t_GPS.endsimul()
    t.endsimul()
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
