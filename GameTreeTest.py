from gtbase import *

#Test Classes, no implementation value
class Node:
	def __init__(self, name, successors, terminal = 0, gval = 0):
		self.name = name
		self.successors = successors
		self.terminal = terminal
		self.gval = gval
		self.utility = 0

	def __repr__(self):
		return self.name

def genTest(terminal_nodes, upper_levels):
	#Test if this is a valid representation
	num_nodes = len(terminal_nodes)
	i = 0
	for level in upper_levels:
		if sum(level) != num_nodes:
			print('GEN:{}: Not a valid node representation!'.format(i))
			print('{} Nodes, {} Upper Level Connections'.format(num_nodes,sum(level)))
			return 1
		else:
			num_nodes = len(level)

	all_nodes = []
	temp_nodes = []
	#Generate the terminal nodes
	i = 0
	j = 0
	for node in terminal_nodes:
		name = 'N' + str(i) + str(j)
		temp_nodes.append(Node(name,[],1,node))
	return 0

#Generate test nodes from bottom up

#Test Case 1 from slide examples
C1 = Node('C1',[],1,7)
C2 = Node('C2',[],1,-6)
C3 = Node('C3',[],1,4)
C4 = Node('C4',[],1,9)
C5 = Node('C5',[],1,3)
C6 = Node('C6',[],1,-10)
C7 = Node('C7',[],1,2)

B1 = Node('B1',[C1, C2, C3])
B2 = Node('B2',[C4, C5])
B3 = Node('B3',[C6, C7])

A1 = Node('A1',[B1, B2, B3])

S1 = GameTreeSearch(1)
#S1.search(A1,1)

#Test Case 2 from slide examples (pruning)
E1 = Node('E1',[],1,1)
E2 = Node('E2',[],1,1)

D1 = Node('D1',[E1])
D2 = Node('D2',[],1,-1)
D3 = Node('D3',[E2])
D4 = Node('D4',[],1,-1)
D5 = Node('D5',[],1,-1)

C1 = Node('C1',[D1,D2])
C2 = Node('C2',[D3])
C3 = Node('C3',[D4])
C4 = Node('C4',[D5])
C5 = Node('C5',[],1,1)

B1 = Node('B1',[C1, C2, C3])
B2 = Node('B2',[C4, C5])

A1 = Node('A1',[B1, B2])

S1 = GameTreeSearch(1)
#S1.search(A1,1)

#Test Case 3 from slide examples (pruning)
ts3_term = [0, 5, -3, 3, 3, -3, 0, 2, -2, 3, 5, 2, 5, -5, 0, 1, 5, 1, -3, 0, -5, 5, -3, 3, 2]
ts3_levels = [[2,2,1,3,2,2,2,2,2,2,2,2,1],[2,3,2,1,2,1,1,1],[2,1,1,1,2,1],[1,2,2,1],[2,2],[2]]

genTest(ts3_term,ts3_levels)