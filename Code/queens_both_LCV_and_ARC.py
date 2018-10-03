import sys
import copy
import time

BOARD_SIZE = 31
ZERO = 0
ONE = 1
MINUS_ONE = -1

possible_values = []
listOfAllAssignmenst = []

if len(sys.argv) < 2:
 print 'Enter a number to choose an option :\n\
       1. Use just the backtracking recursive version of code\n\
       2. Use Least Constraining Value heuristic\n\
       3. Use Arc Consistency\n\
       4. Use both Least constraining value and Arc consistency\n'
 option = int(raw_input())
else:
 print sys.argv[1]
 option = int(sys.argv[1])

use_lcv = ZERO
use_AC = ZERO
use_rBT = ZERO
if option == 1:
 print 'Using only recursive backtracking'
 use_rBT = ONE
elif option is 2:
 print 'Using Least Contraining Value heuristic'
 use_lcv = ONE
elif option is 3:
 print 'Using Arc Consistency'
 use_AC = ONE
elif option == 4:
 print 'Using both Least Constraining Value and Arc Consistency'
 use_lcv = ONE
 use_AC = ONE
else:
 print 'Invalid Input'

def under_attack(col, queens):
    return col in queens or \
           any(abs(col - x) == len(queens)-i for i,x in enumerate(queens))

if use_lcv:
 def calculateConstaintsimposedbyNewLCV(queens,item,n):
  queens_with_new_position = copy.copy(queens)
  queens_with_new_position.append(item)
  j = len(queens) + 1
  total_constraints = 0
  constraints = 0
  temp = []
  while j < n:
   constraints = 0
   for i in range(n):
    temp = []
    for index,value in enumerate(queens_with_new_position):
     if (i not in temp) and ((i == value) or (abs(index-j) == abs(i-value))):
      constraints += 1
      temp.append(i)
   if constraints == n:
    #All positions are constrained
    return float("Inf")
   total_constraints += constraints
   j += 1
  return total_constraints

 def findUnattackedPositions(n,queens):
  list_unattacked_local = []
  for i in range(n):
   if not under_attack(i,queens):
    list_unattacked_local.append(i)
  return list_unattacked_local

 def find_the_least_constraining_value(n,queens):
  lcv = -1
  list_unattacked = findUnattackedPositions(n,queens)
  if not list_unattacked:
   return lcv
  else:
   numbberOfConstraintsByLCV = float("Inf")
   for unattackedPosition in list_unattacked:
    numberOfConstraints = calculate(queens,unattackedPosition,n)
    if numberOfConstraints == float("Inf"): #last unattacked position cannot lead to a solution, try next one
     continue;
    elif numberOfConstraints < numbberOfConstraintsByLCV:
     numbberOfConstraintsByLCV = numberOfConstraints
     lcv = unattackedPosition
  return lcv

if use_AC:
 def updatePossibleValues(queens,n):
  global possible_values
  possible_values = []
  for i in range(BOARD_SIZE):
   possible_values.append(range(BOARD_SIZE))
  for k,x in enumerate(queens):
   for i in range(n):
    if k == i:
     possible_values[i] = [x]
    else:
     if x in possible_values[i]:
      possible_values[i].remove(x)

 def putArcs(dependencies,i,n):
  for k in range((i + 1),n):
   dependencies.append([i,k])
	
 def checkArcConsistency(n,local_dependencies,queens,value):
  while local_dependencies:
   arctoVerify = local_dependencies.pop(0) #take the first constraint in the list
   if arctoVerify:
    i = arctoVerify.pop(0)
    j = arctoVerify.pop(0)
   else:
    return 1 # no arcs to check, so value is consistent
   if RemoveInconsistentValues(queens+[value],i,j):
    for k in range((len(queens) + 1), n):
     if not ((k == i) or ([k,i] in local_dependencies)):
      local_dependencies.append([k,i]) #adding constraints as we removed a possible value
   for temp_list in possible_values:
    for j in temp_list:
     if j == -1:
      listIndex = temp_list.index(j)
      temp_list.remove(j) 
   for i in range(n): # if possible values for any variable is empty... there is no solution with current assignment
    if not possible_values[i]:
     return 0
  return 1

 def IsConsistentWithAssignedQueens(queens,col,value):
  for row,position in enumerate(queens):
   if (position == value) or (abs(col - row) == abs(value - position)):
    return 0
  return 1

 def RemoveInconsistentValues(queens,i,j):
  removed = 0
  absValue = abs(i-j)
  for x in possible_values[i]: #checking if for every possible value for ith variable whether a consistent assignement exists for jth variable 
   if under_attack(x,queens):
    listIndex = possible_values[i].index(x)
    possible_values[i][listIndex] = -1
    continue
   flag = 1
   for y in possible_values[j]:
    if not IsConsistentWithAssignedQueens(queens,j,y):
     listIndex = possible_values[j].index(y)
     possible_values[j][listIndex] = -1
     continue
    if (x != y) and (abs(x-y) != absValue) : #there is a consistent value for the arc. i.e, positins of queens are not in same row
     flag = 0
     break #found a consistent pair(x,y) for this iteration, so contine continue checking for other values x
   if flag: #did not find a consistent value to jth variable for a possible value to in ith variable
    possible_values[i].remove(x) # so removing that value from possible list of ith variable
    removed  = 1 
    break
  return removed

def rsolve_both(queens,n):
 global listOfAllAssignmenst
 if n == len(queens):
  return queens
 else:
  list_unattacked = findUnattackedPositions(n,queens)
  for i in range(n):
   if not list_unattacked:
     break
   else:
    numbberOfConstraintsByLCV = float("Inf") #finding th least contraining value
    lcv = -1
    for unattackedPosition in list_unattacked:
     if unattackedPosition == -1:
      continue
     numberOfConstraints = calculateConstaintsimposedbyNewLCV(queens,unattackedPosition,n)
     if numberOfConstraints == float("Inf"): #last unattacked position cannot lead to a solution, try next one
      listIndex = list_unattacked.index(unattackedPosition)
      list_unattacked[listIndex] = -1
      continue;
     elif numberOfConstraints < numbberOfConstraintsByLCV:
      numbberOfConstraintsByLCV = numberOfConstraints
      lcv = unattackedPosition
    
    if lcv == -1:
     #Assignment is not possile.. backtracking
     break

    for j in range(n):
     if lcv in possible_values[j]:
      possible_values[j].remove(lcv)
    possible_values[len(queens)] = [lcv]

    constraints = [] #checking arc consistency
    putArcs(constraints,len(queens + [lcv]),n)
    if not checkArcConsistency(n,constraints,queens,lcv):
     updatePossibleValues(queens,n)
     if lcv in list_unattacked:
      list_unattacked.remove(lcv)
      continue

    listOfAllAssignmenst.append(queens+[lcv]) #performing the assignment
    newqueens = rsolve_both(queens+[lcv],n)
    updatePossibleValues(queens,n)

    if newqueens != []:
     return newqueens

    if lcv in list_unattacked:
     list_unattacked.remove(lcv)
  return [] # FAIL

def rsolve_AC(queens,n):
        global listOfAllAssignmenst
        if n == len(queens):
                #print(queens)
                return queens
        else:
                for i in range(n):
                        if not under_attack(i,queens):
                                for j in range(n):
                                 if i in possible_values[j]:
                                  possible_values[j].remove(i)
                                possible_values[len(queens)] = [i]
                                constraints = []
                                putArcs(constraints,len(queens + [i]),n)
                                if not checkArcConsistency(n,constraints,queens,i):
                                 updatePossibleValues(queens,n)
                                 continue
                                listOfAllAssignmenst.append(queens+[i])
                                newqueens = rsolve_AC(queens+[i],n)
                                updatePossibleValues(queens,n)
                                if newqueens != []:
                                        return newqueens
                        else:
                                if i in possible_values[len(queens)]:
                                 possible_values[len(queens)].remove(i)
                return [] # FAIL

def rsolve_lcv(queens,n):
        global listOfAllAssignmenst
        if n == len(queens):
                return queens
        else:
                list_unattacked = findUnattackedPositions(n,queens)
                for i in range(n):
                        if not list_unattacked:
                         break
                        else:
                         numbberOfConstraintsByLCV = float("Inf")
                         lcv = -1
                         for unattackedPosition in list_unattacked:
                          if unattackedPosition == -1:
                            continue
                          numberOfConstraints = calculateConstaintsimposedbyNewLCV(queens,unattackedPosition,n)
                          if numberOfConstraints == float("Inf"): #last unattacked position cannot lead to a solution, try next one
                           listIndex = list_unattacked.index(unattackedPosition)
                           list_unattacked[listIndex] = -1
                           continue;
                          elif numberOfConstraints < numbberOfConstraintsByLCV:
                           numbberOfConstraintsByLCV = numberOfConstraints
                           lcv = unattackedPosition
                         if lcv == -1:
                          break
                         listOfAllAssignmenst.append(queens+[lcv])
                         newqueens = rsolve_lcv(queens+[lcv],n)
                         if newqueens != []:
                          return newqueens
                         if lcv in list_unattacked:
                          list_unattacked.remove(lcv)
                return [] # FAIL

def rsolve_rBT(queens,n):
        global listOfAllAssignmenst
        if n == len(queens):
                return queens
        else:
                for i in range(n):
                        if not under_attack(i,queens):
                                listOfAllAssignmenst.append(queens+[i])
                                newqueens = rsolve_rBT(queens+[i],n)
                                if newqueens != []:
                                        return newqueens
                return [] # FAIL

def print_board(queens):
 row = 0
 n = len(queens)
 for pos in queens:
  for i in range(pos):
   sys.stdout.write( ". ")
  sys.stdout.write( "Q ")
  for i in range((n-pos)-1):
   sys.stdout.write( ". ")
  print

start_time = time.time()
if use_AC and use_lcv:
 updatePossibleValues([],0)
 ans = rsolve_both([],BOARD_SIZE)
elif use_lcv:
 ans = rsolve_lcv([],BOARD_SIZE)
elif use_AC:
 updatePossibleValues([],0)
 ans = rsolve_AC([],BOARD_SIZE)
elif use_rBT:
 ans = rsolve_rBT([],BOARD_SIZE)

print 'Time taken : ',(time.time() - start_time)

print_board(ans)

print("Total number of assignments tried before arriving to the solutions are : {0}".format(len(listOfAllAssignmenst)))

print("Below are all the assignments tried :")
for listIndex in listOfAllAssignmenst:
 print(listIndex)
