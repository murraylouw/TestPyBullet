import numpy
import pybullet as p
import time
import math
from datetime import datetime
import pybullet_data

class InverseKinematicsSolver:


    def CalculateJointValues(self, positionX, positionY, positionZ, eulerX, eulerY, eulerZ, robotFilePath):

        #p.connect(p.GUI)
        p.connect(p.DIRECT)

        #p.setAdditionalSearchPath(pybullet_data.getDataPath()) # Add path to default objects from pybullet
        #p.loadURDF("plane.urdf", [0, 0, -0.3])
        #robotFilePath = "kuka_iiwa/model.urdf"
        robotId = p.loadURDF(robotFilePath, [0, 0, 0])
        p.resetBasePositionAndOrientation(robotId, [0, 0, 0], [0, 0, 0, 1])
        
        numJoints = p.getNumJoints(robotId)
        endEffectorIndex = numJoints-1

        lowerLimits = [-.967, -2, -2.96, 0.19, -2.96, -2.09] #lower limits for null space
        upperLimits = [.967, 2, 2.96, 2.29, 2.96, 2.09] #upper limits for null space
        jointRanges = [5.8, 4, 5.8, 4, 5.8, 4] #joint ranges for null space
        restPoses = [0, 0, 0, 0, 0, 0] #restposes for null space
        jointDampingCoefficients = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

        for i in range(numJoints):
            p.resetJointState(robotId, i, restPoses[i])

        p.setGravity(0, 0, 0)
        prevPose = [0, 0, 0]
        prevPose1 = [0, 0, 0]
        hasPrevPose = 0
        useNullSpace = 1
        ikSolver = 0
        trailDuration = 15 #trailDuration is duration (in seconds) after debug lines will be removed automatically #use 0 for no-removal

        p.stepSimulation()

        position = [positionX, positionY, positionZ] # x,y,z cartesian position of end-effector
        orientation = p.getQuaternionFromEuler([math.radians(eulerX), math.radians(eulerY), math.radians(eulerZ)]) # end effector points down

        jointPoses = p.calculateInverseKinematics(  robotId, 
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
        # Create comma seperate string
        jointPosesString = ""
        for i in range(numJoints):
            jointPosesString = jointPosesString + str(jointPoses[i]) + ","
        jointPosesString = jointPosesString[:-1] # Remove last comma

        # Set robot to current joint values
        for i in range(numJoints): # reset each joint state
            p.resetJointState(robotId, i, jointPoses[i])

        endEffectorLinkState = p.getLinkState(robotId, endEffectorIndex)
        if (hasPrevPose):
            p.addUserDebugLine(prevPose, position, [0, 0, 0.3], 1, trailDuration)
            p.addUserDebugLine(prevPose1, endEffectorLinkState[4], [1, 0, 0], 1, trailDuration)
        prevPose = position
        prevPose1 = endEffectorLinkState[4]
        hasPrevPose = 1

        p.disconnect()

        #return jointPosesString
        return jointPoses