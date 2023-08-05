
import http
from operator import mod
import string
from tokenize import String
from flask import Flask
from flask import request
import cv2
from detect_lane import *

app = Flask(__name__)
direction = "-1"
last_angle =90
@app.route('/direction', methods = ['POST','GET'])
def sendDirection():
    global direction
    global last_angle

    getDirection()
    if(last_angle < 70 ):
        return '1' #right
    elif(last_angle > 120):
        return '2' # left
    else:
        return '0' #forward

    
def getDirection():
    video = cv2.VideoCapture("https://192.168.120.223:8080/videofeed")
    listOfsterringangles=[]
    listOfsterringangles.append(0)  
    check,frame = video.read()
    laneLines=Line_detection(frame,np.array([60, 40, 40])
    ,np.array([150, 255, 255]))

    Straighted=average_slope_intercept(frame,laneLines)
    laneLinesImage = LineDrawing(frame, Straighted)
    
    newSteering_Angle = computeSteeringAngle(laneLinesImage,Straighted)
    listOfsterringangles.append(newSteering_Angle)
    stabilized_angle = stabilizeSteeringAngle(listOfsterringangles[-2], listOfsterringangles[-1], 2)
    global direction
    global last_angle
    last_angle = newSteering_Angle

if __name__== "__main__":
    app.run('192.168.120.88',port =5635)
