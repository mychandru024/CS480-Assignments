import sys
import time
BOARD_SIZE = 15
 
def under_attack(col, queens):
    return col in queens or \
           any(abs(col - x) == len(queens)-i for i,x in enumerate(queens))
 
def rsolve(queens,n):
	global listOfAllAssignmenst
	if n == len(queens):
        	return queens
	else:
        	for i in range(n):
			if not under_attack(i,queens):
				listOfAllAssignmenst.append(queens+[i])
                		newqueens = rsolve(queens+[i],n)
                		if newqueens != []:
                    			return newqueens
        	return [] # FAIL


def solve(n):
    solutions = [[]]
    for row in range(n):
        solutions = (solution+[i+1]
                     for solution in solutions # first for clause is evaluated immediately,
                                               # so "solutions" is correctly captured
                     for i in range(BOARD_SIZE)
                     if not under_attack(i+1, solution))
    return solutions

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
print '-----%s----',(time.time() - start_time)

print_board(ans)
print("Total number of assignments tried before arriving to the solutions are : {0}".format(len(listOfAllAssignmenst)))
print("Below are all the assignments tried :")
for listIndex in listOfAllAssignmenst:
	print(listIndex)

