'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2 
import numpy as np
from  numpy import interp
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################
def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect


# def detect_ArUco_details(image):

#     """
#     Purpose:
#     ---
#     This function takes the image as an argument and returns a dictionary such
#     that the id of the ArUco marker is the key and a list of details of the marker
#     is the value for each item in the dictionary. The list of details include the following
#     parameters as the items in the given order
#         [center co-ordinates, angle from the vertical, list of corner co-ordinates]
#     This order should be strictly maintained in the output

#     Input Arguments:
#     ---
#     `image` :	[ numpy array ]
#             numpy array of image returned by cv2 library
#     Returns:
#     ---
#     `ArUco_details_dict` : { dictionary }
#             dictionary containing the details regarding the ArUco marker

#     Example call:
#     ---
#     ArUco_details_dict = detect_ArUco_details(image)
#     """
#     ArUco_details_dict = {} #should be sorted in ascending order of ids
#     ArUco_corners = {}
#     ArUco_angles = {}

#     ##############	ADD YOUR CODE HERE	##############
#     arucoDict = aruco.Dictionary_get(aruco.DICT_5X5_250)
#     arucoParams = aruco.DetectorParameters_create()
#     corners, ids, rejected = aruco.detectMarkers(image, arucoDict, parameters=arucoParams)

#     for i, id in enumerate(ids):
#         ArUco_corners[id[0]] = corners[i][0]
#         center_x = abs(ArUco_corners[id[0]][0][0] + ArUco_corners[id[0]][2][0])/2
#         center_y = abs(ArUco_corners[id[0]][1][1] + ArUco_corners[id[0]][3][1])/2

#         tl_tr_center_x = (ArUco_corners[id[0]][0][0] + ArUco_corners[id[0]][1][0]) // 2
#         tl_tr_center_y = (ArUco_corners[id[0]][0][1] + ArUco_corners[id[0]][1][1]) // 2


#         if tl_tr_center_x-center_x==0 and tl_tr_center_y<center_y:
#            angle=180

#         elif  tl_tr_center_x-center_x==0 and tl_tr_center_y>center_y:
#            angle=0

#         elif  tl_tr_center_y-center_y==0 and tl_tr_center_x>center_x:
#            angle=90

#         elif  tl_tr_center_y-center_y==0 and tl_tr_center_x<center_x:
#           angle=-90

#         else:
#             deg=math.degrees(math.atan2(abs( tl_tr_center_y-center_y),abs( tl_tr_center_x-center_x)))

#             if    tl_tr_center_x > center_x and tl_tr_center_y < center_y:
#                 angle=deg-90-180

#             elif  tl_tr_center_x < center_x and  tl_tr_center_y < center_y:
#                 angle=90+deg

#             elif  tl_tr_center_x < center_x and  tl_tr_center_y > center_y:
#                 angle = -(deg-90)

#             elif  tl_tr_center_x > center_x and  tl_tr_center_y > center_y:
#                 angle=90-deg

#         # ArUco_details_dict[int(id[0])] = [[int(center_x), int(center_y)], int(angle)]
#         ArUco_details_dict[int(id[0])] = [int(center_x), int(center_y)]
#         ArUco_angles[int(id[0])] = [int(angle)]
    
#     #ArUco_details_dict = sorted(ArUco_details_dict)
    
#     ##################################################
    
#     return ArUco_details_dict, ArUco_corners, ArUco_angles


#####################################################################################

def perspective_transform(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array
    
    Example call:
    ---
    warped_image = perspective_transform(image)
    """   
    warped_image = [] 
    #################################  ADD YOUR CODE HERE  ###############################
    details,corners=task_1b.detect_ArUco_details(image)
    tl=details[1][0]
    bl=details[4][0]
    tr=details[2][0]
    br=details[3][0]
    pts=np.float32([tl,bl,tr,br])
    
    # obtain a consistent order of the points and unpack them
	# individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    maxWidth = 512
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    maxHeight = 512
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
    dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped_image = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    ######################################################################################
    return warped_image

def transform_values(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]
    
    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.
    
    Example call:
    ---
    scene_parameters = transform_values(image)
    """   
    scene_parameters = [0, 0, 0]
    #################################  ADD YOUR CODE HERE  ###############################
    print(image.shape)
    details,ArUco_corners=task_1b.detect_ArUco_details(image)
    print(details)
    c_x, c_y = details[5][0]
    angle = details[5][1]
  
    c_x = interp(c_x, [0, 511], [0.955, -0.955])
    c_y = interp(c_y, [0, 511], [-0.955, 0.955])
    scene_parameters[0] = c_x
    scene_parameters[1] = c_y

    center_x = abs(ArUco_corners[5][0][0] + ArUco_corners[5][2][0])/2
    center_y = abs(ArUco_corners[5][1][1] + ArUco_corners[5][3][1])/2

    tl_tr_center_x = (ArUco_corners[5][0][0] + ArUco_corners[5][1][0]) // 2
    tl_tr_center_y = (ArUco_corners[5][0][1] + ArUco_corners[5][1][1]) // 2



    if tl_tr_center_x-center_x == 0 and tl_tr_center_y < center_y:
        angle = 180

    elif  tl_tr_center_x-center_x == 0 and tl_tr_center_y > center_y:
        angle = 0

    elif  tl_tr_center_y-center_y == 0 and tl_tr_center_x > center_x:
        angle = 90

    elif  tl_tr_center_y-center_y == 0 and tl_tr_center_x < center_x:
        angle = -90

    else:
        if    tl_tr_center_x > center_x and tl_tr_center_y < center_y:
            angle = angle-180

        elif  tl_tr_center_x < center_x and  tl_tr_center_y < center_y:
            angle = 180-angle

        elif  tl_tr_center_x < center_x and  tl_tr_center_y > center_y:
            angle = angle-180

        elif  tl_tr_center_x > center_x and  tl_tr_center_y > center_y:
            angle = 180-angle

    scene_parameters[2] = angle
    ######################################################################################
    return scene_parameters


def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.

    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.
    
    Example call:
    ---
    set_values(scene_parameters)
    """   
    aruco_handle = sim.getObject('/aruco_5')
#################################  ADD YOUR CODE HERE  ###############################
    sim.setObjectPosition(aruco_handle,-1,[scene_parameters[0],scene_parameters[1],0.0030])
    sim.setObjectOrientation(aruco_handle,-1, [0,0,scene_parameters[2]])
######################################################################################
    return None

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    task_1b = __import__('task_1b')

#################################  ADD YOUR CODE HERE  ################################
    while(1):
        #img=cv2.imread(r"C:\Users\Adeesh Desai\Downloads\Task_3C_Resources\Task_3C_Resources\arena.jpg")
        video = cv2.VideoCapture(1, apiPreference = cv2.CAP_ANY, params = [
            cv2.CAP_PROP_FRAME_WIDTH, 1920,
            cv2.CAP_PROP_FRAME_HEIGHT, 1080
        ])
        #video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        _, frame = video.read()
        #cv2.imshow("FRAME",frame) 
        cv2.waitKey(1000)
        warped_image=perspective_transform(frame)
        scene_parameters=transform_values(warped_image)
        set_values(scene_parameters)
        
    
    # img=cv2.imread(r"D:/E-Yantra/Task3/Task_3C_Resources/Arena2.jpg")
    # cv2.imshow("Original imgage",img)
    # cv2.waitKey(0)
    # g=perspective_transform(image=img)
    # cv2.imshow("Wraped Image",g)
    # cv2.waitKey(0)
    # scene_parameters = transform_values(image=g)
    # print(scene_parameters)
#######################################################################################