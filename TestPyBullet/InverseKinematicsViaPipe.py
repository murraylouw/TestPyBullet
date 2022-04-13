# Convert to a single exe by running the following in cmd in the current directory:
# pip install pyinstaller
# pyinstaller .\InverseKinematicsViaPipe.py --onefile

from typing import ByteString
import InverseKinematicsSolver
import sys
import time
import win32file 
import struct

def main():

    if len(sys.argv) == 8: # Receive input args
        x = float(sys.argv[1])
        y = float(sys.argv[2])
        z = float(sys.argv[3])
        eulerX = float(sys.argv[4])
        eulerY = float(sys.argv[5])
        eulerZ = float(sys.argv[6])
        robotFilePath = str(sys.argv[7])

    else: # If no input args are received, set default values
        x = 1
        y = 1
        z = 1
        eulerX = 0
        eulerY = 0
        eulerZ = 0
        robotFilePath = "kawasaki_BX200L/kawasaki_BX200L.urdf"

        
    ikSolver = InverseKinematicsSolver.InverseKinematicsSolver()


    pipeFile = open(r'\\.\pipe\ik_pipe', 'r+b', 0)

    while True:
    
        # Read input data from pipe
        received_str_length = struct.unpack('I', pipeFile.read(4))[0] # Read str length
        received_string = pipeFile.read(received_str_length).decode('ascii') # Read str
        pipeFile.seek(0)

        print('Received from .NET: ', received_string)

        if received_string.find("stop_listening") != -1: # Exit while loop when key word is read
            break

        identifier_start   = "<tcp_pose>"
        identifier_end     = "</tcp_pose>"
        start_index     = received_string.find(identifier_start) + len(identifier_start)
        end_index       = received_string.find(identifier_end)
        
        tcp_pose = received_string[start_index:end_index].split() # Format data into useable form
        x = float(tcp_pose[0])
        y = float(tcp_pose[1])
        z = float(tcp_pose[2])
        eulerX = float(tcp_pose[3])
        eulerY = float(tcp_pose[4])
        eulerZ = float(tcp_pose[5])

        # Perform calculation on input data
        jointValues = ikSolver.CalculateJointValues(x, y, z, eulerX, eulerY, eulerZ, robotFilePath)
    
        # Send output through pipe:
        message_from_python = '<joint_values>{0}<joint_values/>'.format(jointValues).encode('ascii')
        
        pipeFile.write(struct.pack('I', len(message_from_python)) + message_from_python) # Write str length and str
        pipeFile.seek(0)

        print('Sent from Python: ', message_from_python)
        print()


    while True:
        left, read_data = win32file.ReadFile(receiveHandle, 4096) # Does not proceed until new data is read
        
        received_string = str(read_data)

        if received_string.find("stop_listening") != -1: # Exit while loop when key word is read
            break
        
        identifier_start   = "<tcp_pose>"
        identifier_end     = "</tcp_pose>"
        start_index     = received_string.find(identifier_start) + len(identifier_start)
        end_index       = received_string.find(identifier_end)
        
        tcp_pose = received_string[start_index:end_index].split()
        print("Data received:")
        print(tcp_pose)

        x = float(tcp_pose[0])
        y = float(tcp_pose[1])
        z = float(tcp_pose[2])
        eulerX = float(tcp_pose[3])
        eulerY = float(tcp_pose[4])
        eulerZ = float(tcp_pose[5])

        result = bytes(ikSolver.CalculateJointValues(x, y, z, eulerX, eulerY, eulerZ, robotFilePath))
        print("joint values:")
        print(result)

        win32file.WriteFile(receiveHandle, result, 4096)

    

if __name__ == "__main__":
    main()
