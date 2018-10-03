import sys
import copy
import time
BOARD_SIZE = 8

def under_attack(col, queens):
    return col in queens or \
           any(abs(col - x) == len(queens)-i for i,x in enumerate(queens))

def calculate(queens,item,n):
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

def rsolve(queens,n):
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
			  numberOfConstraints = calculate(queens,unattackedPosition,n)
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
                	 newqueens = rsolve(queens+[lcv],n)
               		 if newqueens != []:
                 	  return newqueens
			 if lcv in list_unattacked:
			  list_unattacked.remove(lcv)
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
listOfAllAssignmenst = []
ans = rsolve([],BOARD_SIZE)
print '----%s---',(time.time() - start_time)

print_board(ans)

print("Total number of assignments tried before arriving to the solutions are : {0}".format(len(listOfAllAssignmenst)))
print("Below are all the assignments tried :")
for listIndex in listOfAllAssignmenst:
	print(listIndex)
