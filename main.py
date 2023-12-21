#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author:Dong Time:2021/4/12
import math

import cv2
import mediapipe as mp
import time

from HandTrackingMoudle import handDetector
from MacVolumeControl import mac_set_volume, get_system_volume

########################
wCam, hCam = 640, 480
########################

# 输入的视频，“0”为打开摄像头
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
pLength = 0
cLength = 0
lastLength = 0
detector = handDetector()  # 创建对象
vol = int(get_system_volume())  # 当前系统声音
# 调节音量的步长
volStep = 10
# 怕耳朵聋了设置阙值
maxVol = 80
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()  # 静音
# volume.GetMasterVolumeLevel()  # 获取最大音量值
# volRange = volume.GetVolumeRange()  # 获取音量范围
# print(volRange)
# minVol = volRange[0]
# maxVol = volRange[1]
while True:
    sucess, img = cap.read()
    # 检测手
    img = detector.findHands(img)
    # 检测手的标志，并返回标志点坐标
    lmList = detector.findPosition(img, personDraw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        # 计算食指和大拇指指尖坐标，并绘制点、连线
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        cLength = math.hypot(x2 - x1, y2 - y1)
        ranLength = abs(cLength - pLength)
        # 两个拇指间距离
        # print('cLength:', cLength)
        # print('lastLength:', lastLength)

        print('vol:', vol)
        diff = abs(ranLength - lastLength)
        print(diff)
        # 改变距离大于10才会改变音量
        if diff >= 10:
            print('ranLength:', ranLength)
            print('lastLength:', lastLength)
            if ranLength > lastLength:
                print('增大')
                change_vol = vol + volStep
                if change_vol < maxVol:
                    mac_set_volume(change_vol)
                    vol = change_vol
                else:
                    print('已经最大了')
                    mac_set_volume(maxVol)
                lastLength = ranLength
            else:
                print('减小')
                change_vol = vol - volStep
                if change_vol > 0:
                    mac_set_volume(change_vol)
                    lastLength = ranLength
                    vol = change_vol
                # elif change_vol>maxVol:

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # 画面镜像反转
    img = cv2.flip(img, 1)
    cv2.putText(img, "FPS:" + str(int(fps)), (20, 30), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 2)

    # cv2.imshow("Image", img)
    #
    # 记录每一帧的长度
    # 检查是否按下了 'q' 键，如果是则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
