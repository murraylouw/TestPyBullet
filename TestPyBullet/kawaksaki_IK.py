
import pybullet as p
import time
import math
from datetime import datetime
import pybullet_data
import subprocess
import sys

p.connect(p.GUI)

p.setAdditionalSearchPath(pybullet_data.getDataPath()) # Add path to default objects from pybullet
p.loadURDF("plane.urdf", [0, 0, 0])

exec(open("kawasaki_BX200L/kawasaki_BX200L_urdf.py").read()) # Generate URDF file with python script
robotId = p.loadURDF("kawasaki_BX200L/kawasaki_BX200L.urdf", [0, 0, 0])

p.resetBasePositionAndOrientation(robotId, [0, 0, 0], [0, 0, 0, 1])
# p.changeDynamics(robotId, 0, frictionAnchor=100000000) # Add friction anchor to base
endEffectorIndex = 5
numJoints = p.getNumJoints(robotId)

lowerLimits = [-.967, -2, -2.96, 0.19, -2.96, -2.09] #lower limits for null space
upperLimits = [.967, 2, 2.96, 2.29, 2.96, 2.09] #upper limits for null space
jointRanges = [5.8, 4, 5.8, 4, 5.8, 4] #joint ranges for null space
restPoses = [0, 0, 0, 0, 0, 0] #restposes for null space
jointDampingCoefficients = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

# for i in range(numJoints):
#   p.resetJointState(robotId, i, restPoses[i])

p.setGravity(0, 0, -10)
prevPose = [0, 0, 0]
prevPose1 = [0, 0, 0]
hasPrevPose = 0
useNullSpace = 1
ikSolver = 0
trailDuration = 15 #trailDuration is duration (in seconds) after debug lines will be removed automatically #use 0 for no-removal

# Ask for and set individual joint values:
# while 1:  
#   print("joint_number  jolint_value[deg]:")
#   inputs = input().split()
#   joint_index = int(inputs[0])-1
#   joint_value = math.radians(float(inputs[1]))
#   p.resetJointState(robotId, joint_index, joint_value)
#   p.stepSimulation()
#   # time.sleep(0.1)


while 1:  

  p.stepSimulation()

  print("Enter: x y z eulerX eulerY eulerZ ") # Receive inputs from console
  inputs = input().split()
  x = float(inputs[0])
  y = float(inputs[1])
  z = float(inputs[2])
  eulerX = float(inputs[3])
  eulerY = float(inputs[4])
  eulerZ = float(inputs[5])

  position = [x, y, z] # x,y,z cartesian position of end-effector
  orientation = p.getQuaternionFromEuler([math.radians(eulerX), math.radians(eulerY), math.radians(eulerZ)]) # end effector points down

  jointPoses = p.calculateInverseKinematics(robotId, 
                                            endEffectorIndex, 
                                            position, 
                                            orientation, 
                                            lowerLimits, 
                                            upperLimits, 
                                            jointRanges, 
                                            restPoses,
                                            solver=ikSolver,
                                            maxNumIterations=100,
                                            residualThreshold=.01)
    
  for i in range(numJoints): # reset each joint state
    p.resetJointState(robotId, i, jointPoses[i])

  endEffectorLinkState = p.getLinkState(robotId, endEffectorIndex)
  if (hasPrevPose):
    p.addUserDebugLine(prevPose, position, [0, 0, 0.3], 1, trailDuration)
    p.addUserDebugLine(prevPose1, endEffectorLinkState[4], [1, 0, 0], 1, trailDuration)
  prevPose = position
  prevPose1 = endEffectorLinkState[4]
  hasPrevPose = 1

  print("Actual position: ")
  print(prevPose1)

p.disconnect()

