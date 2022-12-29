'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2a.py
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
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2
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
##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to actuate the rotary joints of the robot in this function, such that
	it traverses the points in given order

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
	c=0

	c1=detect_distance_sensor_1(sim)
	c2=detect_distance_sensor_2(sim)
	c3=detect_distance_sensor_3(sim)

	lj=sim.getObject('/Diff_Drive_Bot/left_joint')
	rj=sim.getObject('/Diff_Drive_Bot/right_joint')

	def left_turn(f=1):
		sim.setJointTargetVelocity(rj,f*2)
		sim.setJointTargetVelocity(lj,f*(-2))

	def right_turn(f=1):
		sim.setJointTargetVelocity(rj,f*(-2))
		sim.setJointTargetVelocity(lj,f*2)

	def forward(f=1):
		sim.setJointTargetVelocity(rj,f*3)
		sim.setJointTargetVelocity(lj,f*3)

	def linearInterpolation(x, rX, rY, exX, exY):
		y = exX+(x-rX)*(exY-exX)/(rY-rX)
		return y

	while(True):
		c1=detect_distance_sensor_1(sim) #front
		c2=detect_distance_sensor_2(sim) #right
		c3=detect_distance_sensor_3(sim) #left

		print("c1 : ", c1)
		print("c2 : ", c2)
		print("c3 : ", c3)

		if(c2 < 13 and c2 != 0):
			left_turn()
		
		elif(c3 < 13 and c3 != 0):
			right_turn()

		elif(c1==0 or c2 > 24):
			forward()
		
		else:
			if(c2 == 0):
				right_turn()

			elif(c3 == 0):
				left_turn()
			
			else:
				if(c2 > c3):
					right_turn()
				
				elif(c2 < c3):
					left_turn()
				
				else:
					forward()

		# if(c2!=0):
		# 	if(c2 == 0):
		# 		right_turn(0.5)

		# 	elif(c3 == 0):
		# 		left_turn(0.5)


		# if(c2 > 15 and c2 < 25):
		# 	forward()
		
		# elif(c2 <= 15):
		# 	left_turn()
		
		# else:
		# 	right_turn()


	# def right_wall(c):
	# 	c=c+1
	# 	print("///________________///")
	# 	print(c)
	# 	print("///________________///")
	# 	while(1):
	# 		lj=sim.getObject('/Diff_Drive_Bot/left_joint')
	# 		rj=sim.getObject('/Diff_Drive_Bot/right_joint')
	# 		c1=detect_distance_sensor_1(sim)
	# 		c2=detect_distance_sensor_2(sim)
	# 		c3=detect_distance_sensor_3(sim)
	# 		if(c1==0 and  c2>=17 and c2<=22):
	# 			forward()
	# 		elif(c1>0):
	# 			if(c>5 and c1<30):
	# 				sim.setJointTargetVelocity(rj,0)
	# 				sim.setJointTargetVelocity(lj,0)
	# 			else:
	# 				left_turn()
	# 		elif(c2==0):
	# 			if(c>5 and c1<30):
	# 				sim.setJointTargetVelocity(rj,0)
	# 				sim.setJointTargetVelocity(lj,0)
	# 			else:
	# 				left_wall(c)
	# 		elif( c2>22):
	# 			right_turn()
	# 			forward()
	# 		elif(c2<17):
	# 			left_turn()
	# 			forward()
			
	# def left_wall(c):
	# 	c=c+1
	# 	print("///________________///")
	# 	print(c)
	# 	print("///________________///")
	# 	while(1):
	# 		lj=sim.getObject('/Diff_Drive_Bot/left_joint')
	# 		rj=sim.getObject('/Diff_Drive_Bot/right_joint')
	# 		c1=detect_distance_sensor_1(sim)
	# 		c2=detect_distance_sensor_2(sim)
	# 		c3=detect_distance_sensor_3(sim)
	# 		if(c1==0 and  c3>=17 and c3<=22):
	# 			forward()
	# 		elif(c1>0):
	# 			if(c>5 and c1<30):
	# 				sim.setJointTargetVelocity(rj,0)
	# 				sim.setJointTargetVelocity(lj,0)
	# 			else:
	# 				right_turn()
	# 		elif(c3==0):
	# 			if(c>5 and c1<30):
	# 				sim.setJointTargetVelocity(rj,0)
	# 				sim.setJointTargetVelocity(lj,0)
	# 			else:
	# 				right_wall(c)
	# 			# if((c1!=0 and c2==0) or (c1!=0 and c2!=0)):
	# 			# 	left_turn()
	# 		elif( c3>22):
	# 			left_turn()
	# 			forward()
	# 		elif(c3<17):
	# 			right_turn()
	# 			forward()

	# r=right_wall(c)
	# print("count:-",c)
	##################################################

def detect_distance_sensor_1(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_1 = detect_distance_sensor_1(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	d1=sim.getObject('/Diff_Drive_Bot/distance_sensor_1')
	dist=sim.readProximitySensor(d1)
	distance=dist[1]*100
	##################################################
	return int(distance)

def detect_distance_sensor_2(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	d1=sim.getObject('/Diff_Drive_Bot/distance_sensor_2')
	dist=sim.readProximitySensor(d1)
	distance=dist[1]*100
	##################################################
	return int(distance)

def detect_distance_sensor_3(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_3'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_1 = detect_distance_sensor_1(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	d1=sim.getObject('/Diff_Drive_Bot/distance_sensor_3')
	dist=sim.readProximitySensor(d1)
	distance=dist[1]*100
	##################################################
	return int(distance)
	

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
			control_logic(sim)
			time.sleep(5)

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