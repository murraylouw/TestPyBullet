# Convert to a single exe by running the following in cmd in the current directory:
# pip install pyinstaller
# pyinstaller ./<filename.py> --onefile

from typing import ByteString
import InverseKinematicsSolver
import sys
import time
import win32file 
import struct
import csv

def main():

    # Input arguments
    if len(sys.argv) == 3: 
        robotFilePath = str(sys.argv[1])
        tcpPosesPath = str(sys.argv[2])
        jointValuesPath = str(sys.argv[3])

    else: # If no input args are received, set default values
        robotFilePath = "kawasaki_BX200L/kawasaki_BX200L.urdf"
        tcpPosesPath = "./tcpPoses.csv"
        jointValuesPath = "./jointValues.csv"

    tcpPosesPath = "C:/Users/Murray.Louw/source/repos/InverseKinematicsToolbox/TestInverseKinematicsToolbox/bin/Debug/tcpPoses.csv"
    jointValuesPath = "C:/Users/Murray.Louw/source/repos/InverseKinematicsToolbox/TestInverseKinematicsToolbox/bin/Debug/jointValues.csv"

    ikSolver = InverseKinematicsSolver.InverseKinematicsSolver()

    # Open files for reading and writing
    tcpPosesFile = open(tcpPosesPath)
    jointValuesFile = open(jointValuesPath, 'w', encoding='UTF8', newline='')

    csvReader = csv.reader(tcpPosesFile)
    csvWriter = csv.writer(jointValuesFile)
    header = next(csvReader) # Skip past header row
    
    # Loop through each tcp pose line in input csv file
    for tcpPose in csvReader:
        
        x = float(tcpPose[0])
        y = float(tcpPose[1])
        z = float(tcpPose[2])
        eulerX = float(tcpPose[3])
        eulerY = float(tcpPose[4])
        eulerZ = float(tcpPose[5])

        jointValues = ikSolver.CalculateJointValues(x, y, z, eulerX, eulerY, eulerZ, robotFilePath) # Calculate joint values for each tcp pose
        csvWriter.writerow(jointValues)

    tcpPosesFile.close()
    jointValuesFile.close()
 

if __name__ == "__main__":
    main()

