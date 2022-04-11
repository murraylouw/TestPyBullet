import InverseKinematicsSolver
import sys

def main():
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    z = float(sys.argv[3])
    eulerX = float(sys.argv[4])
    eulerY = float(sys.argv[5])
    eulerZ = float(sys.argv[6])
    robotFilePath = str(sys.argv[7])

    ikSolver = InverseKinematicsSolver.InverseKinematicsSolver()
    result = ikSolver.CalculateJointValues(x, y, z, eulerX, eulerY, eulerZ, robotFilePath)
    print("joint values:")
    print(result)

if __name__ == "__main__":
    main()