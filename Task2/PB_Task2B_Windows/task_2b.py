'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2B   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2b.py
*  Created:				
*  Last Modified:		8/10/2022
*  Author:				e-Yantra Team
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
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
from pyzbar.pyzbar import decode
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################
c=0
d=0
e= None
st=0
def right_turn(sim):
	global c
	c+=1
	global d
	d=0
	rjoint=sim.getObject('/Diff_Drive_Bot/right_joint')
	ljoint=sim.getObject('/Diff_Drive_Bot/left_joint')
	sim.setJointTargetVelocity(rjoint,-0.8)
	sim.setJointTargetVelocity(ljoint,0.8)

def left_turn(sim):
	global c
	c+=1
	global d
	d=0
	rjoint=sim.getObject('/Diff_Drive_Bot/right_joint')
	ljoint=sim.getObject('/Diff_Drive_Bot/left_joint')
	sim.setJointTargetVelocity(rjoint,0.8)
	sim.setJointTargetVelocity(ljoint,-0.8)

def right_turn2(sim):
	rjoint=sim.getObject('/Diff_Drive_Bot/right_joint')
	ljoint=sim.getObject('/Diff_Drive_Bot/left_joint')
	sim.setJointTargetVelocity(rjoint,-0.2)
	sim.setJointTargetVelocity(ljoint,0.2)

def left_turn2(sim):
	rjoint=sim.getObject('/Diff_Drive_Bot/right_joint')
	ljoint=sim.getObject('/Diff_Drive_Bot/left_joint')
	sim.setJointTargetVelocity(rjoint,0.2)
	sim.setJointTargetVelocity(ljoint,-0.2)

def stop(sim):
	rjoint=sim.getObject('/Diff_Drive_Bot/right_joint')
	ljoint=sim.getObject('/Diff_Drive_Bot/left_joint')
	sim.setJointTargetVelocity(rjoint,0)
	sim.setJointTargetVelocity(ljoint,0)
	
def node_contour(sim):
	visionSensorHandle=sim.getObject('/Diff_Drive_Bot/vision_sensor')
	img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
	img = np.frombuffer(img, dtype=np.uint8).reshape(resX, resY, 3)
	img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
	hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	low_yellow = np.array([20, 100, 100])
	high_yellow = np.array([30, 255, 255])
	or_mask = cv2.inRange(hsv_frame, low_yellow,high_yellow)
	img1 = cv2.bitwise_and(img, img, mask=or_mask)
	imgray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
	contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours


def blackline_contour(sim):
	color = [255, 255, 255]
	visionSensorHandle=sim.getObject('/Diff_Drive_Bot/vision_sensor')
	img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
	img = np.frombuffer(img, dtype=np.uint8).reshape(resX, resY, 3)
	img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
	crop_img = img[0:int(img.shape[0]/2), 0:int(img.shape[1])]
	gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return len(contours)

def detect(sim):
	global d
	global c
	global e
	flag=0
	if len(node_contour(sim))!=0:
		if c==4 or c==8 or c==12:
				forward(sim)
		while(len(node_contour(sim))!=0): 
			d+=1
			if c==4:
				while(flag==0):
					activate(sim,"checkpoint E")
					if read_qr_code(sim)==type(e):
						continue
					elif read_qr_code(sim)=="Orange Cone" or read_qr_code(sim)=="Blue Cylinder" or read_qr_code(sim)=="Pink Cuboid":
						stop(sim)
						deliver(sim,"checkpoint E")
						deactivate(sim,"checkpoint E")
						flag=1
						forward2(sim)
						break
			elif c==8:
				while(flag==0):
					activate(sim,"checkpoint I")
					if read_qr_code(sim)==type(e):
						continue
					elif read_qr_code(sim)=="Orange Cone" or read_qr_code(sim)=="Blue Cylinder" or read_qr_code(sim)=="Pink Cuboid":
						stop(sim)
						deliver(sim,"checkpoint I")
						deactivate(sim,"checkpoint I")
						flag=1
						forward2(sim)
						break
			elif c==12:
				while(flag==0):
					activate(sim,"checkpoint M")
					if read_qr_code(sim)==type(e):
						continue
					elif read_qr_code(sim)=="Orange Cone" or read_qr_code(sim)=="Blue Cylinder" or read_qr_code(sim)=="Pink Cuboid":
						stop(sim)
						deliver(sim,"checkpoint M")
						deactivate(sim,"checkpoint M")
						flag=1
						forward2(sim)
						break

	else:
		return d
	
def activate(sim,checkpoint):
	arena_dummy_handle = sim.getObject("/Arena_dummy") 
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
	sim.callScriptFunction("activate_qr_code", childscript_handle, checkpoint)

def deactivate(sim,checkpoint):
	arena_dummy_handle = sim.getObject("/Arena_dummy") 
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
	sim.callScriptFunction("deactivate_qr_code", childscript_handle, checkpoint)

def deliver(sim,checkpoint):
	pack=read_qr_code(sim)
	packages={"Orange Cone":"package_1", "Blue Cylinder":"package_2", "Pink Cuboid":"package_3"}
	arena_dummy_handle = sim.getObject("/Arena_dummy") 
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
	sim.callScriptFunction("deliver_package", childscript_handle,packages[pack], checkpoint)


def angle2(sim):
	list=[]
	visionSensorHandle=sim.getObject('/Diff_Drive_Bot/vision_sensor')
	img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
	img = np.frombuffer(img, dtype=np.uint8).reshape(resX, resY, 3)
	img = cv2.flip(img, 0)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	approxs = []
	for contour in contours:
		approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)
		cv2.drawContours( img, [approx], -1, (0, 255, 0), 5)
		approxs.append(approx)
	contourMaxArea = max(approxs, key=cv2.contourArea)
	
	M = cv2.moments(contourMaxArea)
	if M['m00'] != 0:
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		cv2.drawContours(img, [contourMaxArea], -1, (0, 255, 0), 2)
		cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
		cv2.putText(img, "center", (cx - 20, cy - 20),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
	list.append(cx)
	list.append(cy)

	deg1 = round(math.degrees(math.atan2((contourMaxArea[1][0][1]-contourMaxArea[0][0][1]), (contourMaxArea[0][0][0]-contourMaxArea[1][0][0]))))
	deg2 = round(math.degrees(math.atan2((contourMaxArea[2][0][1]-contourMaxArea[1][0][1]), (contourMaxArea[1][0][0]-contourMaxArea[2][0][0]))))
	
	absDeg1=abs(90-deg1)
	absDeg2=abs(90-deg2)

	max_deg = deg2 if absDeg1>absDeg2 else deg1
	list.append(max_deg)
	return list

def forward2(sim):
	rjoint=sim.getObject('/Diff_Drive_Bot/right_joint')
	ljoint=sim.getObject('/Diff_Drive_Bot/left_joint')
	sim.setJointTargetVelocity(rjoint,2.0)
	sim.setJointTargetVelocity(ljoint,2.0)	

def forward(sim):
	rjoint=sim.getObject('/Diff_Drive_Bot/right_joint')
	ljoint=sim.getObject('/Diff_Drive_Bot/left_joint')
	sim.setJointTargetVelocity(rjoint,1.0)
	sim.setJointTargetVelocity(ljoint,1.0)

def turn(sim):
	global d
	global c
	global st
	c1=0
	c2=0
	c3=0
	c4=0
	if d>0 and c==0:
		left_turn(sim)
		while(1):
			while(blackline_contour(sim)==2):
				c1+=1
			while(blackline_contour(sim)==1 ):
				c3+=1
			while(blackline_contour(sim)==2 and c1>0):
				c2+=1
			while(blackline_contour(sim)==1 and c3>0 ):
				c4+=1
			while(blackline_contour(sim)==2 and c1>0 and c2>0):
				x_coordinate(sim)
				break
			break		
	elif d>0 and (c==1 or c==3 or c==5 or c==7 or c==9 or c==11 or c==13 or c==15):
		right_turn(sim)
		while(1):
			while(blackline_contour(sim)==2):
				c1+=1
			while(blackline_contour(sim)==1 ):
				c3+=1
			while(blackline_contour(sim)==2 and c1>0):
				c2+=1
			while(blackline_contour(sim)==1 and c3>0 ):
				c4+=1
			while(blackline_contour(sim)==2 and c1>0 and c2>0):
				# stop()
				x_coordinate(sim)
				break
			break		

			
	elif d>0 and (c==2  or c==6 or c==10  or c==14 ):
		left_turn(sim)
		while(1):
			while(blackline_contour(sim)==2):
				c1+=1
			while(blackline_contour(sim)==1 ):
				c3+=1
			while(blackline_contour(sim)==2 and c1>0):
				c2+=1
			while(blackline_contour(sim)==1 and c3>0 ):
				c4+=1
			while(blackline_contour(sim)==2 and c1>0 and c2>0):
				stop(sim)
				break
			break		

			

	elif d>0 and (c==4 or c==8 or c==12):
		c+=1
		d=0
	
	elif d>0 and c==16:
		st=1
		d=0

def correction(sim):
	global e
	if angle2(sim)[2]>91 :
		stop(sim)
		left_turn2(sim)

	elif angle2(sim)[2]<89:
		stop(sim)
		right_turn2(sim)

	elif angle2(sim)[2]<=91 and angle2(sim)[2]>=89:
		forward2(sim)

def x_coordinate(sim):
	rjoint=sim.getObject('/Diff_Drive_Bot/right_joint')
	ljoint=sim.getObject('/Diff_Drive_Bot/left_joint')
	sim.setJointTargetVelocity(rjoint,1)
	sim.setJointTargetVelocity(ljoint,1)
	while(angle2(sim)[0]<260):
		sim.setJointTargetVelocity(rjoint,1.5)
		sim.setJointTargetVelocity(ljoint,0.7)
		while(angle2(sim)[0]<260):
			continue

	while(angle2(sim)[0]>260):
		sim.setJointTargetVelocity(ljoint,1.5)
		sim.setJointTargetVelocity(rjoint,0.7)
		while(angle2(sim)[0]>260):
			continue

# def x_coordinate2(sim):
# 	rjoint=sim.getObject('/Diff_Drive_Bot/right_joint')
# 	ljoint=sim.getObject('/Diff_Drive_Bot/left_joint')
# 	sim.setJointTargetVelocity(rjoint,1)
# 	sim.setJointTargetVelocity(ljoint,1)
# 	while(angle2(sim)[0]<266):
# 		sim.setJointTargetVelocity(rjoint,0.8)
# 		sim.setJointTargetVelocity(ljoint,0.6)
# 		while(angle2(sim)[0]<266):
# 			continue

# 	while(angle2(sim)[0]>246):
# 		sim.setJointTargetVelocity(ljoint,0.8)
# 		sim.setJointTargetVelocity(rjoint,0.6)
# 		while(angle2(sim)[0]>246):
# 			continue

##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to make the robot follow the line to cover all the checkpoints
	and deliver packages at the correct locations.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	None

	Example call:
	---
	control_logic(sim)
	"""
	##############  ADD YOUR CODE HERE  ##############
	rjoint=sim.getObject('/Diff_Drive_Bot/right_joint')
	ljoint=sim.getObject('/Diff_Drive_Bot/left_joint')
	visionSensorHandle=sim.getObject('/Diff_Drive_Bot/vision_sensor')
	sim.setJointTargetVelocity(rjoint,1)
	sim.setJointTargetVelocity(ljoint,1)
	

	while(1):
		global e
		global c
		global st
		D=detect(sim)
		if st==1:
			stop(sim)
			break
		elif D==0:
			# x_coordinate2(sim)
			correction(sim)
		elif type(D)==type(e):
			pass
		elif D>0:
			while(1):
				if(detect(sim)>0):
					turn(sim)
					forward2(sim)
					break
				else: continue
		else:	
			# x_coordinate2(sim)
			correction(sim)

		

		
	
	##################################################

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the camera's field of view and
	returns the message encoded into it.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	`qr_message`   :    [ string ]
		QR message retrieved from reading QR code

	Example call:
	---
	control_logic(sim)
	"""
	qr_message = None
	##############  ADD YOUR CODE HERE  ##############
	visionSensorHandle=sim.getObject('/Diff_Drive_Bot/vision_sensor')
	img, resX, resY = sim.getVisionSensorCharImage(visionSensorHandle)
	img = np.frombuffer(img, dtype=np.uint8).reshape(resX, resY, 3)
	img = cv2.flip(img, 0)
	for code in decode(img):
		qr_message=code.data.decode('Utf-8')



	##################################################
	return qr_message


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
	client = RemoteAPIClient()
	sim = client.getObject('sim')	

	try:

		## Start the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.startSimulation()
			if sim.getSimulationState() != sim.simulation_stopped:
				print('\nSimulation started correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be started correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be started !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

		## Runs the robot navigation logic written by participants
		try:
			time.sleep(5)
			control_logic(sim)

		except Exception:
			print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually if required.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

		
		## Stop the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.stopSimulation()
			time.sleep(0.5)
			if sim.getSimulationState() == sim.simulation_stopped:
				print('\nSimulation stopped correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be stopped correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be stopped !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

	except KeyboardInterrupt:
		## Stop the simulation using ZeroMQ RemoteAPI
		return_code = sim.stopSimulation()
		time.sleep(0.5)
		if sim.getSimulationState() == sim.simulation_stopped:
			print('\nSimulation interrupted by user in CoppeliaSim.')
		else:
			print('\nSimulation could not be interrupted. Stop the simulation manually .')
			sys.exit()