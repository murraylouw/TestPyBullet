
import pybullet as p
import time
import pybullet_data
import numpy as np

physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
#p.setAdditionalSearchPath("C:/Users/Murray.Louw/source/repos/TestPyBullet/TestPyBullet")

p.setGravity(0,0,0)
planeId = p.loadURDF("plane.urdf")

cubeStartPos = [0,0,1]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
bodyUniqueId = p.loadURDF("m1n6s300/m1n6s300.urdf",cubeStartPos, cubeStartOrientation)
#bodyUniqueId = p.loadURDF("kuka_iiwa/model.urdf",cubeStartPos, cubeStartOrientation)

for i in range (10000):
    p.stepSimulation()
    time.sleep(1./240.)
    cubePos, cubeOrn = p.getBasePositionAndOrientation(bodyUniqueId)
    
    #targetPosition = 

    #p.calculateInverseKinematics(
    #                bodyUniqueId,
    #                endEffectorLinkIndex = 6,
    #                targetPosition,
    #                targetOrientation
    #            )

print(cubePos,cubeOrn)
p.disconnect()

def inverse_kinematics(self, target_position, target_orientation, rest_poses=None):
        """
        Helper function to do inverse kinematics for a given target position and 
        orientation in the PyBullet world frame.

        Args:
            target_position: A tuple, list, or numpy array of size 3 for position.
            target_orientation: A tuple, list, or numpy array of size 4 for
                a orientation quaternion.
            rest_poses: (optional) A list of size @num_joints to favor ik solutions close by.

        Returns:
            A list of size @num_joints corresponding to the joint angle solution.
        """

        if rest_poses is None:
            ik_solution = list(
                p.calculateInverseKinematics(
                    self.ik_robot,
                    6,
                    target_position,
                    targetOrientation=target_orientation,
                    restPoses=[0, -1.18, 0.00, 2.18, 0.00, 0.57, 3.3161],
                    jointDamping=[0.1] * 7,
                )
            )
        else:
            ik_solution = list(
                p.calculateInverseKinematics(
                    self.ik_robot,
                    6,
                    target_position,
                    targetOrientation=target_orientation,
                    lowerLimits=[-3.05, -3.82, -3.05, -3.05, -2.98, -2.98, -4.71],
                    upperLimits=[3.05, 2.28, 3.05, 3.05, 2.98, 2.98, 4.71],
                    jointRanges=[6.1, 6.1, 6.1, 6.1, 5.96, 5.96, 9.4],
                    restPoses=rest_poses,
                    jointDamping=[0.1] * 7,
                )
            )
        return ik_solution 