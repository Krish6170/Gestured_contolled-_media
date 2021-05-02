import cv2
import time
import math
import numpy as np
import mediapipe as mp
import tensorflow_core.python.ops.distributions.util
from hand_dectector import detector
import pyautogui as p
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def one_indexfinger_touch(image, lst1):
    x1, y1 = lst1[8]
    x2, y2 = lst1[4]
    length = math.hypot((x1 - x2), (y1 - y2))
    print(length)
    cv2.putText(image, str(length), (200, 200), 2, 3, [0, 255, 255, 3])
    cv2.line(image, (x1, y1), (x2, y2), [0, 255, 255])
    return length


# ///////////////////////////////////////////////////////////////////////////////
def player(play):
    left = 0
    top = 650
    width = 1800
    height = 430
    x, y = p.locateCenterOnScreen(play, region=(left, top, width, height))
    p.click(x, y)
    p.moveRel(-39, 2)

def pauser(pause):
    left = 0
    top = 650
    width = 1800
    height = 430
    x, y = p.locateCenterOnScreen(pause, region=(left, top, width, height))
    p.click(x, y)
    p.moveRel(-39,2)

def forward():
    p.press("right")
def backward():
    p.press("left")


# ////////////////////////////////////////////////////////////////////////////////
def gesture_detection(lst, gestures):
    finger_tips = [4, 8, 12, 16, 20]
    if lst:

        if lst[20][1] < lst[0][1]:
            Of = []
            if lst[4][0] < lst[3][0]:
                Of.append(1)
            else:
                Of.append(0)

            for i in finger_tips[1:5]:
                if lst[i][1] < lst[i - 2][1]:
                    Of.append(1)
                else:
                    Of.append(0)
            # prediction
            for key, value in gestures.items():
                if value == Of:
                    return key


# ///////////////////////////////////////////////////////////

def gesture_recog():
    play = "C:\coding_stuff\proopcv\play.png"
    pause = "C:\coding_stuff\proopcv\pause.PNG"

    p_time = 0
    c_time = 0
    vid = cv2.VideoCapture(0)
    hand=detector(min_detection_confidence=.8)
    gestures={"Confirm": [1,1,1,1,1],"Pause":[0,1,1,1,1],"Volume":[1,1,0,0,1],"Forward":[0,1,1,0,0],"Backward":[0,1,0,0,0],"Play":[0,0,0,0,0]}
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    while True:

        success, image = vid.read()
        image=hand.detect(image,1)
        lst = hand.track_landmark_list(image)
        #5 to confirm or stop [1 1 1 1 1 ]
        #4 to pause [0 1 1 1 1]
        #3 to adjust volume [1 1 0 0 1]
        #2 to forward [0 1 1 0 0]
        #1 to backward[0 1 0 0 0]
        #0 to play [0 0 0 0 0]

        if gesture_detection(lst,gestures)=="Play":
            try:
                player(play)
            except:
                print("played")
        elif gesture_detection(lst,gestures)=="Volume":
            if hand.results.multi_hand_landmarks:

                if len(hand.results.multi_hand_landmarks)==1:
                    # 5 finger to control volume

                    length=one_indexfinger_touch(image,lst)
                    vol=np.interp(int(length),[100,250],[-63.5,0])

                    if int(length)>100:
                        volume.SetMasterVolumeLevel(int(vol),None)

            print("volume")


        elif gesture_detection(lst,gestures)=="Pause":
            try:
                pauser(pause)
            except:
                print("paused")
        elif gesture_detection(lst,gestures)=="Forward":
            try:
                forward()
            except:
                print("forward")
        elif gesture_detection(lst,gestures)=="Backward":
            try:
                backward()
            except:
                print("backward")
        elif gesture_detection(lst, gestures) == "Confirm":
            print("confirm")




        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(image, str(int(fps)), (78, 80), cv2.FONT_HERSHEY_PLAIN, 3, [0, 255, 0], 3)

        cv2.imshow("image", image)

        if cv2.waitKey(1) & 0xFF == ord("k"):
            break

if __name__ == '__main__':
    gesture_recog()
