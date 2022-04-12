import InverseKinematicsSolver
import sys
import time
import win32file 

def main():

    if len(sys.argv) == 8:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
        z = float(sys.argv[3])
        eulerX = float(sys.argv[4])
        eulerY = float(sys.argv[5])
        eulerZ = float(sys.argv[6])
        robotFilePath = str(sys.argv[7])

    else: # If no input args are received
        x = 1
        y = 1
        z = 1
        eulerX = 0
        eulerY = 0
        eulerZ = 0
        robotFilePath = "kawasaki_BX200L/kawasaki_BX200L.urdf"

        
    ikSolver = InverseKinematicsSolver.InverseKinematicsSolver()

    receiveHandle = win32file.CreateFile(
        "\\\\.\\pipe\\TCP_pose", 
        win32file.GENERIC_READ | win32file.GENERIC_WRITE, 
        0, 
        None, 
        win32file.OPEN_EXISTING, 
        0, 
        None)

    while True:
        left, read_data = win32file.ReadFile(receiveHandle, 4096) # Does not proceed until new data is read
        
        data_str = str(read_data)

        if data_str.find("stop_listening") != -1: # Exit while loop when key word is read
            break
        
        identifier_start   = "<TCP_pose>"
        identifier_end     = "</TCP_pose>"
        start_index     = data_str.find(identifier_start) + len(identifier_start)
        end_index       = data_str.find(identifier_end)
        
        tcp_pose = data_str[start_index:end_index].split()
        print("Data received:")
        print(tcp_pose)

        x = float(tcp_pose[0])
        y = float(tcp_pose[1])
        z = float(tcp_pose[2])
        eulerX = float(tcp_pose[3])
        eulerY = float(tcp_pose[4])
        eulerZ = float(tcp_pose[5])

        result = ikSolver.CalculateJointValues(x, y, z, eulerX, eulerY, eulerZ, robotFilePath)
        print("joint values:")
        print(result)

    

if __name__ == "__main__":
    main()
