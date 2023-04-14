def getCoordinates(matrix):
    coordinates= dict()

    for line in range(len(matrix)):
        for column in range (len(matrix[line])):
            if matrix[line][column] != '0':
                coordinates[matrix[line][column]] = [line, column]
    
    return coordinates

def calculateDistance(route, coordinates):
    distance = 0
    start_line, start_column = coordinates['R']

    for i in range(len(route)):
        if i == 0:
            current_line, current_column = coordinates[route[i]]
            destination_line, destination_column = coordinates[route[i+1]]

            distance += abs(current_line - start_line) + abs(current_column - start_column) + abs(destination_line - current_line) + abs(destination_column - current_column)

        elif i == len(route) - 1: 
            current_line, current_column = coordinates[route[i]]

            distance += abs(start_line - current_line) +  abs(start_column - current_column)
        else:
            current_line, current_column = coordinates[route[i]]
            destination_line, destination_column = coordinates[route[i+1]]

            distance += abs(destination_line - current_line) + abs(destination_column - current_column)
        
    return distance

def txtToMatrix(fileName):
    matrix = []
    file = open(fileName)
    lines = file.readlines()

    for line in lines:
        if not line.isspace():
            matrix.append(line.replace("\n", ""). split(" "))
    
    return matrix

def getPoints(matrix):
    points = []
    coordinates = getCoordinates(matrix)

    for k in coordinates.keys():
        if k != 'R':
            points.append(k)
    
    return points

    