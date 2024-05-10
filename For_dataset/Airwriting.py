import cv2
import numpy as np
import mediapipe as mp
from enum import Enum, auto
import csv
import datetime
import glob
import copy
import os
import sys

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
 
n_collected = 0

class Mode(Enum):
    """ 
    """
    DRAW = auto()
    #ERASE = auto()
    #CLEAR = auto()
    MOVE = auto()


def draw(src, pt1, pt2):
    """ This is a function for drawing on an image.
    Args:
        src (numpy.array): Image for drawing
        pt1 (tupple): The starting point of the line to draw
        pt2 (tupple): The ending point of the line to draw
    """
    if pt1 != (-5000, -5000) and pt2[0] != (-5000, -5000):
                src = cv2.line(src, pt1, pt2, (0, 0, 255), 10)


def erase(src, point):
    """ This is a function to erase the lines in the image.
    Args:
        src (numpy.array): Image for erase the line
        point (tupple): The center point of eraser
    """
    src = cv2.circle(src, point, 100, (255, 255, 255), -1)


def clear(src):
    """ This is a function to make the image blank.
    Args:
        src (numpy.array): Image for clear
    """
    pt1 = (0, 0)
    pt2 = (width, height)
    color = (255, 255, 255)
    src = cv2.rectangle(src, pt1, pt2, color, -1)


def printMode(mode, src):
    """ This is a function to print current mode.
    Args:
        mode (Mode): mode for print
        src (numpy.array): Image for print mode
    """
    #Fill in the text printed in the previous frame.
    src = cv2.rectangle(src, (0, 0), (430, 110), (255, 255, 255), -1)
    #put text in src
    src = cv2.putText(src, mode.name, (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 1, cv2.LINE_AA)


def action(digitLength, pt1, pt2, src):
    """ This is a function to select a mode and execute it.
    Args:
        digitLength (numpy.array): Used for select a mode
        pt1 (tupple): Used for draw function
        pt2 (tupple): Used for draw function or erase function
        src (numpy.array): Used for all function to draw something.
    
    Return:
        mode (Mode): return the executed mode
    """
    if digitLength[2] // digitLength[5] < 3 and digitLength[1] // digitLength[5] > 3:
        mode = Mode.DRAW
        draw(src, pt1, pt2)
    # elif (digitLength[:5] // digitLength[5] < 3).all():
    #     mode = Mode.ERASE
    #     erase(src, pt2)
    # elif (digitLength[:5] // digitLength[5] > 2).all():
    #     mode = Mode.CLEAR
    #     clear(src)    
    else:
        mode = Mode.MOVE
    printMode(mode, src)
    
    return mode

def write_data(dir_path, data, img):
    with open(dir_path + f'{datetime.datetime.now():%Y%m%d%H%M%S}.csv' , 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['x', 'y'])
        for d in data:
            writer.writerow([d[0], d[1]])
    #cv2.imwrite(dir_path + 'test.jpg', img)
    print(str(n_collected) + " time : " + "complete writing data")

# create save directories
print("please input your name")
user_name = input()
print("What character do you collect?")
collected_char = input()

if not os.path.isdir("./collected_data/" + user_name):
    os.mkdir("./collected_data/" + user_name)
else:
    print("[warning] same user name directory exists")

if not os.path.isdir("./collected_data/" + user_name + '/' + collected_char):
    os.mkdir("./collected_data/" + user_name + '/' + collected_char)
else:
    print("[warning] same character name directory exists")

save_dir = "./collected_data/" + user_name + '/' + collected_char + '/'

# For webcam input:
cap = cv2.VideoCapture(0)
WIDTH: int = 960
HEIGHT: int = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

data_history = []
pre_mode = None
height, width = 0, 0
# src = cv2.imread('white1.png', -1)
pt1, pt2 = (-5000, -5000), (-5000, -5000)


#with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
while cap.isOpened():
    success, image = cap.read()
    #print(image.shape)
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if height != image.shape[0] or width != image.shape[1]:
        height, width = image.shape[:2]
        print(height, width)
        src = np.ones((height, width, 3), np.uint8) * 255

        
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # collect the data
            data = []
            for landmark in hand_landmarks.landmark:
                data.append((landmark.x * width, landmark.y * height))
            data = np.array(data)
            
        digitLength = np.array([[np.linalg.norm(data[i*4][:2] - data[0][:2])] for i in range(1,6)])
        digitLength = np.append(digitLength, np.linalg.norm(data[1][:2] - data[0][:2]))
        pt2 = (int(data[8, 0]), int(data[8, 1]))
        mode = action(digitLength, pt1, pt2, src)
        pt1 = pt2        

        if mode is Mode.DRAW:
            data_history.append(pt1)
        #elif mode is not Mode.DRAW and pre_mode is Mode.DRAW: #For double stroke
        #    data_history.append([-1,-1])
        
        # if mode is Mode.CLEAR:
        #     data_history.clear()

        pre_mode = mode


    blended = cv2.addWeighted(src1=image, alpha=0.7, src2=src, beta=0.3, gamma=0)
    #src[:, :, 3] = np.where(np.all(src == 255, axis=-1), 0, 255)
    cv2.imshow('MediaPipe Hands', blended)

    k = cv2.waitKey(5)
    if k == 27:         # wait for ESC key to exit
        break
    elif k == ord('p'):
        print("What character do you collect?")
        collected_char = input()
        if not os.path.isdir("./collected_data/" + user_name + '/' + collected_char):
            os.mkdir("./collected_data/" + user_name + '/' + collected_char)
        else:
            print("[warning] same character name directory exists")
        save_dir = "./collected_data/" + user_name + '/' + collected_char + '/'
        n_collected = 0
        print()
    elif k == ord('c'):
        clear(src)
        data_history.clear()
    elif k == ord('s'): # wait for 's' key to save 
        n_collected += 1
        write_data(save_dir, data_history, blended)
        clear(src)
        data_history.clear()
hands.close()
cap.release()
cv2.destroyAllWindows()


