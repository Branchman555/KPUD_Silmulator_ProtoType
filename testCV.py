import turtle as tr
import cv2
import random
import pandas as pd
from numpy.random import randn
from scipy.stats import bernoulli
import math
import MyRobot

VER_ROBOT = 0.1

mark_radius = 20

GPS_ERR_VAL = 20
ANG_ERR_VAL = 1
VEL_ERR_VAL = 0.2
NODE_CORR = 0.8

GPS_WEIGHT = 0.2
ROUTE_WIDTH = 16


nodes = [(0, 0), (100, 200), (200, 100), (200, 0), (200, -200), (100, -100),
         (-200, -100), (-200, 0), (-100, 100), (0, 0)]
"""
y1-y2
x2-x1
x1y2-x2y1
"""

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

def Ang_Normalize(tar_angle):
    if tar_angle > 180:
        tar_angle -= 360
    elif tar_angle < -180:
        tar_angle += 360
    return tar_angle

def cal_point_line(point, line):
    d = abs(line[0] * point[0] + line[1] * point[1] + line[2])\
        / math.sqrt(line[0]**2 + line[1]**2)
    return d

lines = cal_line_equ(nodes)
print(lines)

t_GPS.pensize(ROUTE_WIDTH)
t_GPS.down()
t_GPS.color("green")
for index, node in enumerate(nodes):
    t.goto(node[0], node[1] - mark_radius)
    t_GPS.goto(node[0], node[1])
    t.write(str(index))
    t.down()
    t.circle(mark_radius)
    t.up()

t_GPS.up()

"""
가정 1 : 자이로 데이터는 미세한 오차만을 가지고 있다.
가정 2 : GPS데이터의 벙위 오차는 표준편차 1m의 오류를 가지고 있다.
가정 3 : 속도 데이터는 아주 미세한 오차를 가지고 있다고 가정한다. 
"""

#루프 시작

t.speed(0)
t_GPS.speed(0)
t.down()

t_GPS.color("red")
t_GPS.goto(t.position())

for index, node in enumerate(nodes):
    if index == 0:
        t.up()
        t_GPS.up()
        t.goto(node[0], node[1])
        t_GPS.goto(node[0], node[1])
        t.down()
        continue

    delta = 0
    err_count = 0
    arrival_count = 0
    vision_count = 0
    vision_angle = 0

#초기 방향 잡아주기 및 카운트 초기화
    target_tilt = t_GPS.towards(node)
    t.setheading(target_tilt)
    t.setheading(target_tilt)

    while 1:
#오류와 사기가 판치는 공간의 시작
        # head = bernoulli.rvs(0.5)
        # if head is 1:
        #     rnd = random.randint(-30, 30)
        #     t.right(rnd)
        #     t_GPS.right(rnd + randn() * ANG_ERR_VAL)

#카운트에 맞춰서 점찍기, 랜덤 오류발생
        if err_count % 5 is 0:
            err_GPS = (t.position()[0] + randn() * GPS_ERR_VAL, t.position()[1] + randn() * GPS_ERR_VAL)
            cor_GPS = (GPS_WEIGHT * err_GPS[0] + (1 - GPS_WEIGHT) * t_GPS.position()[0], GPS_WEIGHT * err_GPS[1] + (1 - GPS_WEIGHT) * t_GPS.position()[1])

            t_GPS.goto(err_GPS)
            t_GPS.dot(5, "red")

            t_GPS.goto(cor_GPS)
            t_GPS.dot(6, "blue")

        t_GPS.setheading(t.heading())
        if t_GPS.distance(node) < mark_radius:
            arrival_count += 1
            if arrival_count > 4:
                t.forward(5)
                t_GPS.forward(5 + randn() * VEL_ERR_VAL)
                arrival_count = 0
                t_GPS.goto((1 - NODE_CORR) * err_GPS[0] + NODE_CORR * node[0],
                           (1 - NODE_CORR) * err_GPS[1] + NODE_CORR * node[1])
                break
# 오류와 사기가 판치는 공간의 끝

        # 각도 변경파트: GPS 기반
        target_tilt = t_GPS.towards(node)

        tar_angle = t_GPS.heading() - target_tilt

        tar_angle = Ang_Normalize(tar_angle)

        #랜덤 자율주행
        if vision_count > 5:
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

        #자율주행 각도 보정
        corr_angle_vis = 0
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

        #GPS 각도 보정
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
            t.right(corr_angle_vis)
            t_GPS.right(corr_angle_vis + randn() * ANG_ERR_VAL)
            print("mode : vision")
        else:
            t.right(corr_angle_gps)
            t_GPS.right(corr_angle_gps + randn() * ANG_ERR_VAL)
            print("mode : GPS filter")


        # 랜덤 속도 감속
        head = bernoulli.rvs(0.1)
        if head is 1:
            t.forward(1)
            t_GPS.forward(1 + randn() * VEL_ERR_VAL)
        else:
            t.forward(3)
            t_GPS.forward(3 + randn() * VEL_ERR_VAL)

        if err_count % 20 is 0:
            t.write(str(round(t.distance(t_GPS.position()), 2)))
            print("ED : ", str(t.distance(t_GPS.position())))
        err_count += 1
        vision_count += 1

tr.done()