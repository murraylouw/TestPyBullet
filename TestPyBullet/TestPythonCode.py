
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

    jointValuesFile = "C:/Users/Murray.Louw/source/repos/InverseKinematicsToolbox/TestInverseKinematicsToolbox/bin/Debug/jointValues.csv"
    
    jointValuesFile = open(jointValuesPath, 'w')

    csvWriter = csv.writer(jointValuesFile)
    

    csvWriter.writerow("Test,This")


    tcpPosesFile.close()
    jointValuesFile.close()
 

if __name__ == "__main__":
    main()

