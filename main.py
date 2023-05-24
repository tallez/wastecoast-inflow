# Hello ! Welcome to the Main Vision Script.
# This script aims to locate waste flowing down a river from a video feed.
# With a socket module, it has to transmit x,y + speed through internet

# A.1 Import available modules
import cv2
import numpy as np
import socket

# A.2 Import side scripts
from transform import four_point_transform
from tracker import *
from flow_speed import *

# A.3 Create and connect Socket for transmission
# Host = '192.168.1.17'
# Port = 234
# Socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Socket.connect((Host,Port))

# B. Get video feed
path_to_video = "https://yuwpxekhcyxqobbumhuc.supabase.co/storage/v1/object/public/Wastecoast/Video/Reduced.mov?t=2023-05-24T14%3A29%3A51.919Z"
# Put cv2.VideoCapture(1) to get livefeed from main camera.
try:
    Video_Feed = cv2.VideoCapture(path_to_video)
except:
    print("No video feed detected")

# C. Get video area of interest

# C.1 Delimitation of the Area

# Only a portion of the camera field of view is interesting for analysis, it has to be very still and offer a stable background for contrasting with targets
# Delimitations of the Area of interest has to be define precisely, a ruler or markers should be considered to appear on the video feed for calibration.

# For test, according to the video in ressource we will agree to the following values
# Positions in px of the corners on the video
# lt : x:252, y:800 (LeftTop)
# rt : x:1653, y:802 (RightTop)
# rb : x:1824, y:1073 (RightBottom)
# lb : x:107, y:1066 (LeftBottom)
# Represent a rectangle on the field (10x70cm)

deltaX = 2.8
deltaY = 3

lt = (252 / deltaX, 800 / deltaY)
rt = (1653 / deltaX, 802 / deltaY)
rb = (1824 / deltaX, 1073 / deltaY)
lb = (107 / deltaX, 1066 / deltaY)

Area_0f_Interest = [lt, rt, rb, lb]

# C.2 Array Markers of the Area
# Warpping the video so the transmitted positions are given according to an orthonormal coordinates system.

Affine_Markers = np.array(eval(str(Area_0f_Interest)), dtype="float32")

# D Object Detection Methods
# D.1 Creation of the Markers list and position registration

Trackers = EuclideanDistTracker()

# D.2 Filter video for movement detection

Filter_Method = cv2.createBackgroundSubtractorMOG2(
    history=100, varThreshold=40)

# E. Video Analysis
# E.1 Monitor frame count + create dataframe for flow speed analysis + Create a finalized dataformat to send

frame_count = 0
flow_frame = []
Data_Pack = []

# E.2 Core Analysis

while True:
    ret, frame = Video_Feed.read()
    frame_count = frame_count + 1
    Detections = []

    # Affine Transform of the Area of Interest

    Affine_Warped_Frame = four_point_transform(frame, Affine_Markers)

    # Movement filtering + Contours finding

    Mask = Filter_Method.apply(Affine_Warped_Frame)
    _, Mask = cv2.threshold(Mask, 100, 200, cv2.THRESH_BINARY)
    Contours, _ = cv2.findContours(
        Mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in Contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 50:
            # cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            Detections.append([x, y, w, h])

            # Demonstration need but not vital
            startpoint = (x, y)
            endpoint = (x+w, y+h)
            color = (0, 255, 0)
            thickness = 2
            Affine_Warped_frame = cv2.rectangle(
                Affine_Warped_Frame, startpoint, endpoint, color, thickness)

    # 2. Object Tracking
    boxes_ids = Trackers.update(Detections)
    for box_id in boxes_ids:

        x, y, w, h, id = box_id  # Box_ID gives detected objet size and position

    # F.Flow Speed Analysis + Transmission of Datas

    flow_datas = normalize_flow_datas(boxes_ids, frame_count)

    if len(flow_datas) > 0:
        flow_frame.append(flow_datas)

    flow_speed = flow_speed_calculus(flow_frame)

    if len(flow_datas) > 0 and flow_speed != 0:
        Data_Pack.append(box_id)
        Data_Pack.append(flow_speed)

        Signal = str(Data_Pack)
        Signal = Signal.encode('utf-8')
        # Socket.send(Signal)
        print(Signal)

        Data_Pack.clear()

    # Demonstration
    cv2.imshow('Main', frame)
    # cv2.imshow('Mask', Mask)
    cv2.imshow('Analysis', Affine_Warped_Frame)

    key = cv2.waitKey(30)
    if key == 27:
        break

Video_Feed.release()
cv2.destroyAllWindows()
