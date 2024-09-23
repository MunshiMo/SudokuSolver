import sys
import csv
import pandas as pd
import time
from pandas import read_csv
from queue import PriorityQueue
import copy
import math

nodeCounter = 0
#function created to print the sudoku board in an easy way
def printSudoku(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def validInput(board, num, position): #given a value and position will check for validity
    #check row
    for i in range(len(board[0])):
        #position comes in as a tuple and so by specifying position[n] we get x or y
        if board[position[0]][i] == str(num) and position[1] != str(i):
            return False
        
        
    #chekc column
    for z in range(len(board)):
        if board[z][position[1]] == str(num) and position[0] != str(z):
            return False
    #check current square
    box_x = position[1] // 3 * 3
    box_y = position[0] // 3 * 3
    
    for i in range(box_y, (box_y+ 3)):
        for j in range(box_x, (box_x + 3)):
            if board[i][j] == str(num) and (i,j) != position:
                return False

    return True
    #if true value then return true

                 
def findUnfilled(board): 
    #finds an unfilled spot on the board and returns its position
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'X':
                return (i,j)
    
    return False

    
def availableValues(board,position): #returns a set of possible values
    if board[position[0]][position[1]] != "X":
        return False
    givenDomain = {'1','2','3','4','5','6','7','8','9'}
    
    for i in range(len(board[0])):
        #if board[position[0]][i] != str(num) and position[1] != str(i):
        givenDomain -= set(board[position[0]][i])
        
        
    #chekc column
    for z in range(len(board)):
        #if board[z][position[1]] != str(num) and position[0] != str(z):
        givenDomain -= set(board[z][position[1]])
            
    #check current square
    box_x = position[1] // 3 * 3
    box_y = position[0] // 3 * 3
    
    for i in range(box_y, (box_y+ 3)):
        for j in range(box_x, (box_x + 3)):
            #if board[i][j] != str(num) and (i,j) != position:
            givenDomain -= set(board[i][j])
    possibleVals = list(givenDomain)
    return possibleVals

def setInitialConstraints(row, column):
    #seeks out the values that a give position cant be at the current board
    constraints = []
    minRow = row - (row % 3)
    minColumn = column - (column % 3)
    # add 3x3 neighborhood constraints
    for r in range (minRow, minRow + 3):
        for c in range (minColumn, minColumn + 3):
            if (((row == r) and (column == c)) == False):
                constraints.append((r * 9) + c)
    
    # add row "conflict" variable IDs
    for rowConstraint in range(0, 9):
        if (rowConstraint != column):
            constraints.append((row * 9) + rowConstraint)
    
    # add column "conflict" variable IDs        
    for columnConstraint in range(0, 9):
        if (columnConstraint != row):
            constraints.append((column % 9) + 9 * columnConstraint)        
    
    
    return list(set(constraints))

            
def isBoardComplete(board): #if the board no longer has X it can be considered complete
    for i in range(0,9):
        for j in range(0,9):
            if board[i][j] == 'X':
                return False
    
    return True

def isWholeBoardValid(board):  #using the validInput function I run through the whole board and use the current positions and values to check validity each time
    counter = -1
    for i in range(0,9):
        for j in range(0,9):
            currentVal = board[i][j]
            if validInput(board, currentVal, (i,j)):
                counter = counter + 1
            else:
                return False
    return True
 
def getVariable2DCoordinates(variableID):
    if (variableID in range (0, 81)):
        row = math.floor(variableID / 9)
        column = variableID % 9
        return (row, column)
    else:
        return None
 
def isWholeBoardValid2(puzzle, constraints):  #using the validInput function I run through the whole board and use the def isSolved(puzzle, constraints):
    for varA in range(0, 81):
        constraintList = constraints.get(varA)
        (row1, column1) = getVariable2DCoordinates(varA)
        for constrainedVariable in constraintList:
            (row2, column2) = getVariable2DCoordinates(constrainedVariable)
            if (puzzle[row1][column1] == puzzle[row2][column2]) or (puzzle[row1][column1] == 'X'):
                return False
    return True

 
def bruteForce(board, initial, variable, solved, constraints):
    #want to perform depth first search meaning we go all the way to the last right most node.
    global nodeCounter
    if (variable == 80):#isBoardComplete(board):
#if variable = 80 that means we have gone thru all the spaces present
        if isWholeBoardValid2(board, constraints): 
            solved = True
            return (board, solved)
    else:
        variable = variable + 1
        (i,j) = getVariable2DCoordinates(variable)
        #using an index we can get the position of a spot
        if initial[i][j] == 'X':
#if there isnt a value the domain can be 1-10
            domain = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        else:
 #else it is the already present value
            domain = [initial[i][j]]
        for value in domain:
            board[i][j] = value
            nodeCounter += 1
            #increment nodecoutner to keep track of the expansions going on 
            (board,solved) = bruteForce(board, initial, variable, solved, constraints)
            if solved == True:
                return (board,solved)     
        board[i][j] == 'X'
        variable = variable - 1
        #if need be decrement to go back and backtrack
    return (board,solved)           


def cspBacktracking(board, constraints):
    global nodeCounter
    
    find = findUnfilled(board) #will return a position for us to look into
    if not find and isWholeBoardValid2(board, constraints):
        return True
    else:
        row, col = find #store the given location where the first number is for row and the second for column
        pair = (row,col)
#cycling thru 1-10 we test each value
    for i in range(1,10):
        if validInput(board, i, pair):
            board[row][col] = str(i)
            nodeCounter += 1
#if working then we can increment
            if cspBacktracking(board, constraints): #recursive call
                return True
            else:
                board[row][col] = 'X'  #restore to original state

    return False

def InferencesMRV(board):
    #want to go through the empty spots and choose the ideal position pair
    #with the least amount of constraints so that it can be filled in first
    currMinVal = 10
    domainVals = {'1','2','3','4','5','6','7','8','9'}
    for i in range(0,9):
        for j in range(0,9):
            if board[i][j] == 'X':
                vals = domainVals -  set(availableValues(board, (i,j))) #will give the contraints
                if len(vals) < currMinVal:
                    currMinVal = len(vals)
                    pos = (i,j)
    return pos
             
        
    
    
def cspForwardChecking(board, constraints):
    global nodeCounter
    find = findUnfilled(board) #will return a position for us to look into
    if not find and isWholeBoardValid2:
        return True
    else:
        minPair = InferencesMRV(board)
        row, col = minPair #store the given location where the first number is for row and the second for column
        #now that we find the pair with the least constraints we can test
        
        availValsDomain = availableValues(board, minPair)
#using the values that are available rather than cycling thru the whole 1-10
    for i in availValsDomain:
        if validInput(board, i, minPair):
            board[row][col] = str(i)
            nodeCounter += 1

            if cspForwardChecking(board, constraints): #recursive call
                return True
            else:
                board[row][col] = 'X'  #restore to original state

    return False



def main(): 
    global nodeCounter
    numberOfArgumentsPassedFromCommandLine = len(sys.argv)
    print("Number of arguments passed (including your script name):", numberOfArgumentsPassedFromCommandLine)
#gather args from user and print expected infromation

    print("Munshi, Mohammed, A20468727 solution:")
    testFile = sys.argv[1] 
    print("\nTestCaseFile:", testFile)

    mode = sys.argv[2] #goal state
    print("\nAlgorithm:",  mode)
#if args > 3 then that is too many and should be stopped
    if len(sys.argv) > 3:
        print("Error too many arguments being passed retry")
        exit()
    #-------------------------------------------------------------    
    file = open(str(testFile)) #input testfile
    nodeCounter = 0
    data = list(csv.reader(file,delimiter=","))
    file.close()

    file = open(str(testFile)) #input testfile
    nodeCounter = 0
    initial = list(csv.reader(file,delimiter=","))
    file.close()
    #create inital as an original copy
    constraints = dict()
    var = 0
    for row in range(0, 9):
        for column in range(0, 9):
            constraints[var] = setInitialConstraints(row, column)
            var = var + 1
#get initial constraints
    if(int(mode) < 1 or int(mode) > 4 ):
        print("Error: incorrect inputs values are 1 - 4")
        return
 #check to ensure mode is a value between 1-4 since that is what we consider anythign else is flagged   
    if(int(mode) == 1):
        methodUsed = "Bruteforce"
        print("\n")
        printSudoku(data)
        print("\n")
        print("Bruteforce will be attempted")
        print("\n")
        startTime = time.time()
#start the time keeping        
        (data, solved) = bruteForce(data, initial, -1, False, constraints)
        printSudoku(data)
        
        execTime = time.time()-startTime
        #pint outputs
        print("\nA20468727")
        print(testFile)
        print(methodUsed)
        print("Nodes generated: ", nodeCounter)
        print("Runtime: " , execTime)
        
        
        #write to a new csv file
        newFile = str(testFile) 
        newFile = newFile.replace(".csv", "_solution.csv")
        with open(str(newFile), 'w', newline='') as outputFile:
            thewriter = csv.writer(outputFile)
            for i in range(0,9):
                thewriter.writerow(data[i])
                
    elif(int(mode) == 2):
        methodUsed = "CSP Backtracking"
        print("\n")
        printSudoku(data)
        print("CSP Backtracking will be attempted")
        
        startTime = time.time()
        cspBacktracking(data, constraints)
        printSudoku(data)
        
        execTime = time.time()-startTime
        
        print("\nA20468727")
        print(testFile)
        print(methodUsed)
        print("Nodes generated: ", nodeCounter)
        print("Runtime: " , execTime)
        
                #write to a new csv file
        newFile = str(testFile) 
        newFile = newFile.replace(".csv", "_solution.csv")
        with open(str(newFile), 'w', newline='') as outputFile:
            thewriter = csv.writer(outputFile)
            for i in range(0,9):
                thewriter.writerow(data[i])
    elif(int(mode) == 3):
        methodUsed = "CSP Forward Checking w/ MRV"
        print("\n")
        printSudoku(data)       
        print()
        print("CSP Forward Checking with MRV attempted")
        
        startTime = time.time()
        cspForwardChecking(data,constraints)
        execTime = time.time()-startTime
        
        print("\nA20468727")
        print(testFile)
        print(methodUsed)
        print("Nodes generated: ", nodeCounter)
        print("Runtime: " , execTime)
        print()
        printSudoku(data)
        
        #write to a new csv file
        newFile = str(testFile) 
        newFile = newFile.replace(".csv", "_solution.csv")
        
        with open(str(newFile), 'w', newline='') as outputFile:
            thewriter = csv.writer(outputFile)
            for i in range(0,9):
                thewriter.writerow(data[i])
    #4 is to check a solution csv    
    elif(int(mode) == 4):
        print("\n")
        printSudoku(data)
        print("will test for validity in sudoku")
        #only if both are true then we have success
        if isBoardComplete(data) and isWholeBoardValid:
            printSudoku(data)
            print("success")
            return True    

main()
        



