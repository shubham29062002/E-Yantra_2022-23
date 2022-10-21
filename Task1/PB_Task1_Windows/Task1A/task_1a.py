'''
*******************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*******************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
def fun(lower_limit,upper_limit,maze_image):

    

    hsv_frame = cv2.cvtColor(maze_image, cv2.COLOR_BGR2HSV)
    low = np.array(lower_limit)
    high = np.array(upper_limit)
    or_mask = cv2.inRange(hsv_frame, low,high)
    img = cv2.bitwise_and(maze_image, maze_image, mask=or_mask)


    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    Main_list=[]
    for contour in contours:

          approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
          cv2.drawContours(img, approx, -1, (255, 255, 255), 4)

          M = cv2.moments(contour)
          if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])

          # List=[]
          if len(approx) == 3:
               Main_list.append(['Triangle',[x,y]])

          elif len(approx) == 4:
              Main_list.append(['Square',[x,y]])

          else:
               Main_list.append(['Circle',[x,y]])


          # Main_list.append(List)


    return Main_list





##############################################################

def detect_traffic_signals(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present
	
	Example call:
	---
	traffic_signals = detect_traffic_signals(maze_image)
	"""    
	traffic_signals = []

	##############	ADD YOUR CODE HERE	##############
	hsv_frame = cv2.cvtColor(maze_image, cv2.COLOR_BGR2HSV)
	low_red = np.array([0, 70, 50])
	high_red = np.array([10,255,255])
	or_mask = cv2.inRange(hsv_frame, low_red,high_red)
	img = cv2.bitwise_and(maze_image,maze_image, mask=or_mask)



	imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	list=[]
	Numbers=['7','6','5','4','3','2','1']
	Alphabets=['A','B','C','D','E','F','G']
	for contour in contours:
			approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
			cv2.drawContours(img, approx, -1, (255, 255, 255), 4)


			M = cv2.moments(contour)
			if M['m00'] != 0.0:
				x = int(M['m10']/M['m00'])
				y = int(M['m01']/M['m00'])
				
				a=-1
				for i in range(700,0,-100):
					a+=1

					b=-1
					for j in range(100,800,100):
						b+=1

						if(j==x and i==y):
								list.append(Alphabets[b]+Numbers[a])


				list.sort()

				traffic_signals = list
	##################################################
	
	return traffic_signals
	

def detect_horizontal_roads_under_construction(maze_image):
	
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing horizontal links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links
	
	Example call:
	---
	horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
	"""    
	horizontal_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	Numbers=['7','6','5','4','3','2','1']
	Numbers.reverse()
	Alphabets=['A','B','C','D','E','F','G']

	a=-1
	for i in range(100,700,100):
		a+=1
		b=0
		for j in range(200,800,100):
			b+=1
			bgr_list=maze_image[j,i+50]
			if bgr_list[0]==255 and bgr_list[1]==255 and bgr_list[2]==255:
				str=Alphabets[a]+Numbers[b]+'-'+Alphabets[a+1]+Numbers[b]
				horizontal_roads_under_construction.append(str)

	##################################################
	
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing vertical links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links
	
	Example call:
	---
	vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
	"""    
	vertical_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############

	Numbers=['7','6','5','4','3','2','1']
	Numbers.reverse()
	Alphabets=['A','B','C','D','E','F','G']

	a=-1
	for i in range(100,800,100):
		a+=1
		b=0
		for j in range(200,700,100):
			b+=1
			bgr_list=maze_image[j+50,i]
			if bgr_list[0]==255 and bgr_list[1]==255 and bgr_list[2]==255:
				str=Alphabets[a]+Numbers[b]+'-'+Alphabets[a]+Numbers[b+1]
				vertical_roads_under_construction.append(str)

	##################################################
	
	return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a nested list of
	details of the medicine packages placed in different shops

	** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
	   as well as in the alphabetical order of colors.
	   For example, the list should first have the packages of shop_1 listed. 
	   For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`medicine_packages` : [ list ]
			nested list containing details of the medicine packages present.
			Each element of this list will contain 
			- Shop number as Shop_n
			- Color of the package as a string
			- Shape of the package as a string
			- Centroid co-ordinates of the package
	Example call:
	---
	medicine_packages = detect_medicine_packages(maze_image)
	"""    
	medicine_packages = []

	##############	ADD YOUR CODE HERE	##############

	Color=['Green','Orange','Pink','Skyblue']
	LowerLimit=[[36,0,0],[1, 190, 200],[130,0,220],[85,155,20]]
	UpperLimit=[[86,255,255],[18, 255, 255],[170,255,255],[95,255,255]]

	Shop1=[]
	Shop2=[]
	Shop3=[]
	Shop4=[]
	Shop5=[]
	Shop6=[]


	for i in range(4):
		List=fun(LowerLimit[i],UpperLimit[i],maze_image)
		# print(List,end='\n')
		# print(List)
		for j in range(len(List)):
			if List[j][1][0]>100 and List[j][1][0]<200:
				Shop1.append(['Shop_1',Color[i],List[j][0],List[j][1]])

			elif   List[j][1][0]>200 and List[j][1][0]<300:
				Shop2.append(['Shop_2',Color[i],List[j][0],List[j][1]])

			elif   List[j][1][0]>300 and List[j][1][0]<400:
				Shop3.append(['Shop_3',Color[i],List[j][0],List[j][1]])

			elif   List[j][1][0]>400 and List[j][1][0]<500:
				Shop4.append(['Shop_4',Color[i],List[j][0],List[j][1]])

			elif   List[j][1][0]>500 and List[j][1][0]<600:
				Shop5.append(['Shop_5',Color[i],List[j][0],List[j][1]])

			elif   List[j][1][0]>600 and List[j][1][0]<700:
				Shop6.append(['Shop_6',Color[i],List[j][0],List[j][1]])


	medicine_packages=Shop1+Shop2+Shop3+Shop4+Shop5+Shop6

	##################################################

	return medicine_packages

def detect_arena_parameters(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) horizontal_roads_under_construction : list of missing horizontal links
	iii) vertical_roads_under_construction : list of missing vertical links
	iv) medicine_packages : list containing details of medicine packages

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	arena_parameters['traffic_signals']=detect_traffic_signals(maze_image)
	arena_parameters['horizontal_roads_under_construction']=detect_horizontal_roads_under_construction(maze_image)
	arena_parameters['vertical_roads_under_construction']=detect_vertical_roads_under_construction(maze_image)
	arena_parameters['medicine_packages_present']=detect_medicine_packages(maze_image)
	##################################################
	
	return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "_main_":

    # path directory of images in test_images folder
	img_dir_path = "public_test_images/"

    # path to 'maze_0.png' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
	
	# read image using opencv
	maze_image = cv2.imread(img_file_path)
	
	print('\n============================================')
	print('\nFor maze_' + str(file_num) + '.png')

	# detect and print the arena parameters from the image
	arena_parameters = detect_arena_parameters(maze_image)

	print("Arena Prameters: " , arena_parameters)

	# display the maze image
	cv2.imshow("image", maze_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
	
	if choice == 'y':

		for file_num in range(1, 15):
			
			# path to maze image file
			img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
			
			# read image using opencv
			maze_image = cv2.imread(img_file_path)
	
			print('\n============================================')
			print('\nFor maze_' + str(file_num) + '.png')
			
			# detect and print the arena parameters from the image
			arena_parameters = detect_arena_parameters(maze_image)

			print("Arena Parameter: ", arena_parameters)
				
			# display the test image
			cv2.imshow("image", maze_image)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()