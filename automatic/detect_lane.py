import cv2
import math
import numpy as np

def computeSteeringAngle(frame, laneLines):
    """ Find the steering angle based on lane line coordinate
        We assume that camera is calibrated to point to dead center
    """
    if len(laneLines) == 0:
        print('No lane lines detected, do nothing')
        #MAKE CAR STOP?
        return -90

    # Get middle line in case of detecting single lane
    height, width, _ = frame.shape
    if len(laneLines) == 1:
        print('Only detected one lane line, just follow it. ', laneLines[0])
        x1, _, x2, _ = laneLines[0][0]
        x_offset = x2 - x1
    else:   # get middle line in case of detecting two lanes
        _, _, left_x2, _ = laneLines[0][0]
        _, _, right_x2, _ = laneLines[1][0]
        cameraMidOffsetPercent = 0.00 # 0.0 means car pointing to center, -0.03: car is centered to left, +0.03 means car pointing to right
        mid = int(width / 2 * (1 + cameraMidOffsetPercent))
        x_offset = (left_x2 + right_x2) / 2 - mid

    # find the steering angle, which is angle between navigation direction to end of center line
    y_offset = int(height / 2)

    angleToMidRadian = math.atan(x_offset / y_offset)  # angle (in radian) to center vertical line
    angleToMidDeg = int(angleToMidRadian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
    steeringAngle = angleToMidDeg + 90  # this is the steering angle needed by picar front wheel

    print('new steering angle: ', steeringAngle)
    return steeringAngle

def stabilizeSteeringAngle(currSteeringAngle, newSteeringAngle, numOfLaneLines, maxAngleDeviationTwoLines=5, maxAngleDeviationOneLane=1):
    """
    Using last steering angle to stabilize the steering angle
    This can be improved to use last N angles, etc
    if new angle is too different from current angle, only turn by maxAngleDeviation degrees
    """
    if numOfLaneLines == 2 :
        # if both lane lines detected, then we can deviate more
        maxAngleDeviation = maxAngleDeviationTwoLines
    else :
        # if only one lane detected, don't deviate too much
        maxAngleDeviation = maxAngleDeviationOneLane
    
    angleDeviation = newSteeringAngle - currSteeringAngle
    if abs(angleDeviation) > maxAngleDeviation:
        stabilizedSteeringAngle = int(currSteeringAngle + maxAngleDeviation * angleDeviation / abs(angleDeviation))
    else:
        stabilizedSteeringAngle = newSteeringAngle
    print('Proposed angle: ',newSteeringAngle, ', stabilized angle: ' ,stabilizedSteeringAngle)
    return stabilizedSteeringAngle

def displayHeadingLine(frame, steeringAngle, lineColor=(0, 0, 255), lineWidth=15):
    headingImage = np.zeros_like(frame)
    height, width, _ = frame.shape

    # figure out the heading line from steering angle
    # heading line (x1,y1) is always center bottom of the screen
    # (x2, y2) requires a bit of trigonometry

    # Note: the steering angle of:(adjust boundaries based on car performance)
    # 0-89 degree: turn left
    # 90 degree: going straight
    # 91-180 degree: turn right 
    steeringAngleRadian = steeringAngle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steeringAngleRadian))
    y2 = int(height / 2)

    cv2.line(headingImage, (x1, y1), (x2, y2), lineColor, lineWidth)
    headingImage = cv2.addWeighted(frame, 0.8, headingImage, 1, 1)

    return headingImage

def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=5 ):
    heading_image = np.zeros_like(frame)
    height, width, _ = frame.shape

    # figure out the heading line from steering angle
    # heading line (x1,y1) is always center bottom of the screen
    # (x2, y2) requires a bit of trigonometry

    # Note: the steering angle of:
    # 0-89 degree: turn left
    # 90 degree: going straight
    # 91-180 degree: turn right 
    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)

    cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)
    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)

    return heading_image


def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if line_segments is None:
        return lane_lines

    height, width, _ = frame.shape
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))

    return lane_lines




def region_of_interest(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)

    # only focus bottom half of the screen
    polygon = np.array([[
        (0, height * 1 / 2),
        (width, height * 1 / 2),
        (width, height),
        (0, height),
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)
    return cropped_edges



def canny_edge(frame, lowerColor, upperColor):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerColor, upperColor)
    edges = cv2.Canny(mask, 200, 400)
    Isolated=region_of_interest(edges)

    return Isolated



def houghLines(croppedEdges):
   
    rho = 1  # distance precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
    minThreshold = 10  # minimal of votes
    lineSegments = cv2.HoughLinesP(croppedEdges, rho, angle, minThreshold, np.array([]), minLineLength=8, maxLineGap=4)

    return lineSegments






def Line_detection(frame, lowerColor, upperColor):
    edges = canny_edge(frame, lowerColor, upperColor)
    croppedEdges = edges
    lineSegments = houghLines(croppedEdges)
   

    return lineSegments

def LineDrawing(frame, lines, lineColor = (0,255,0), lineWidth = 20):
    lineImage = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(lineImage, (x1, y1), (x2, y2), lineColor, lineWidth)
    lineImage = cv2.addWeighted(frame, 0.8, lineImage, 1, 1)
    return lineImage


