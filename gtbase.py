import math
from reversi_structure import *
import time
import decimal

#No heuristic
def _zero_hfn(node):
	return 0

class GameTreeSearch:
	def __init__(self, trace_level, depth_limit = 0, search_strategy = 'DFS'):
		self.search_strategy = search_strategy
		self.depth_limit = depth_limit
		self.trace = trace_level
		self.nodes_pruned = 0
		return

	def search(self, top_node, turn, prune=True, heur_fun = _zero_hfn):
		self.heur_fun = heur_fun
		self.prune = prune
		self.nodes_visited = 0
		self.terminal_nodes = 0
		#For turn 1 is MAX, -1 is MIN
		if self.trace == 1:
			print('TRACE: Running search on node {}'.format(top_node))
			print('TRACE: Current player is {}'.format(self.printPlayer(turn)))
		start_time = time.clock()
		result = self.gtRecurse(top_node, 1, turn)
		end_time = time.clock()
		search_time = end_time - start_time

		total_nodes = self.nodes_visited + self.terminal_nodes
		speed = total_nodes/search_time

		search_time = round(search_time,2)
		speed = round(speed,2)
		if self.trace == 3:
			if self.prune == False:
				print('TRACE: Search completed with {} nodes, searched [{}s, {} nodes/s]'.format(total_nodes, search_time, speed))
			else:
				print('TRACE: Search completed with {} nodes searched and {} nodes pruned [{}s, {} nodes/s]'.format(total_nodes, self.nodes_pruned, search_time, speed))
		return result[0]

	def printPlayer(self, player):
		if player == 1:
			cur_player = 'MAX'
		else:
			cur_player = 'MIN'
		return cur_player

	def gtRecurse(self, node, level, player, alpha=(-1*float("inf")), beta=float("inf")):
		pruned = False

		#Get node successors (note, will be a function rather than an attribute)
		node.generateChildNodes()
		if player == 1:	#White is MAX
			children = node.getChildrenWhite()
		else: #Black is MIN
			children = node.getChildrenBlack()

		#Print board
		board_state = node.getReversiBoardObject()
		if self.trace == 1:
			board_state.printBoard()

		#If the search is depth limited
		if self.depth_limit != 0:
			if level == self.depth_limit:
				gval = self.heur_fun(board_state.getBoard())
				self.terminal_nodes += 1

				if self.trace == 1:
					print('TRACE:{}: Depth Limited Node {}, Hval {}'.format(level,node,gval))
				return [node, gval]
		#Check if node is terminal node
		else:
			if len(children) == 0:
				self.terminal_nodes += 1
				if player == 1:
					gval = board_state.getScoreBlack()
				else:
					gval = board_state.getScoreWhite()

				if self.trace == 1:
					print('TRACE:{}: Terminal Node {}, Gval {}'.format(level,node,gval))
				return [node, gval]

		if self.trace == 1:
			print('TRACE:{}: Current player is {}'.format(level,self.printPlayer(player)))
			print('TRACE:{}: Node {} has successors {}'.format(level,node,str(children)))
		choice = 0

		if player == 1:
			best_utility = -1 * float("inf")
		else:
			best_utility = float("inf")

		i = 0
		for child_node in children:
			if self.trace == 1:
				print('TRACE:{}: Searching Node {}'.format(level,child_node))
			[opp_choice, utility] = self.gtRecurse(child_node, level+1, player * -1, alpha, beta)
			if player == 1: #MAX PLAYER
				if utility > best_utility:
					best_utility = utility
					choice = child_node
					#Implementation of alpha pruning
					alpha = best_utility
					if self.prune == True:
						if alpha > beta:
							pruned = True
							break
				if self.trace == 1:
					print('TRACE:{}: Node {} Alpha={} Beta={} after searching {}'.format(level,node,alpha,beta,child_node))
			else:
				if utility < best_utility:
					best_utility = utility
					choice = child_node
					#Implementation of beta pruning
					beta = best_utility
					if self.prune == True:
						if beta < alpha:
							pruned = True
							break
				if self.trace == 1:
					print('TRACE:{}: Node {} Alpha {} Beta {} after searching {}'.format(level,node,alpha,beta,child_node))
			i = i + 1
		if self.trace == 1:
			if pruned == True:
				print('TRACE:{}: Pruned {} nodes with alpha-beta pruning'.format(level, len(children[i+1:])))
				print('TRACE:{}: {} total nodes pruned'.format(level, self.nodes_pruned))
			print('TRACE:{}: {} choosing Node {} with Gval {}'.format(level, self.printPlayer(player), choice, best_utility))

		if pruned == True:
			self.nodes_pruned += len(children[i+1:])

		self.nodes_visited += 1

		if self.trace == 2:
			print('TRACE:{}, {} Nodes Visited'.format(level,self.nodes_visited))

		return [choice, best_utility]
