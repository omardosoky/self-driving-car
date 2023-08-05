import cv2
from detect_lane import *
#https://172.28.132.243:8080/videofeed

video = cv2.VideoCapture("https://172.28.134.:8080/videofeed")
listOfsterringangles=[]
listOfsterringangles.append(0)

while(1):
    check,frame = video.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    laneLines=Line_detection(frame,np.array([60, 40, 40])
    ,np.array([150, 255, 255]))

    Straighted=average_slope_intercept(frame,laneLines)
    laneLinesImage = LineDrawing(frame, Straighted)
    
    newSteering_Angle = computeSteeringAngle(laneLinesImage,Straighted)
    listOfsterringangles.append(newSteering_Angle)
    stabilized_angle = stabilizeSteeringAngle(listOfsterringangles[-2], listOfsterringangles[-1], 2)
    #final_img=display_heading_line(frame, stabilized_angle)

    print(stabilized_angle)
    #Isolated=region_of_interest(laneLinesImage)
    cv2.imshow("image",laneLinesImage)
    cv2.waitKey(1)

