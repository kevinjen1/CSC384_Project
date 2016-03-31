import math

#No heuristic
def _zero_hfn(node):
	return 0

class GameTreeSearch:
	def __init__(self, trace_level, search_strategy = 'DFS', depth_limit = 0):
		self.search_strategy = search_strategy
		self.depth_limit = depth_limit
		self.trace = trace_level
		return

	def search(self, top_node, turn, heur_fun = _zero_hfn):
		self.heur_fun = heur_fun
		#For turn 1 is MAX, -1 is MIN
		if self.trace == 1:
			print('TRACE: Running search on node {}'.format(top_node))
			print('TRACE: Current player is {}'.format(self.printPlayer(turn)))
		result = self.gtRecurse(top_node, 1, turn)
		return result[0]

	def printPlayer(self, player):
		if player == 1:
			cur_player = 'MAX'
		else:
			cur_player = 'MIN'
		return cur_player

	def gtRecurse(self, node, level, player, alpha=(-1*float("inf")), beta=float("inf")):
		pruned = False

		#If the search is depth limited
		if self.depth_limit != 0:
			if self.curr_level == self.depth_limit:
				if self.trace == 1:
					print('TRACE:{}: Depth Limited Node {}, Hval {}'.format(level,node,node.gval))
				return [node, heur_fun(node)]
		#Check if node is terminal node
		else:
			if node.terminal == 1:
				if self.trace == 1:
					print('TRACE:{}: Terminal Node {}, Gval {}'.format(level,node,node.gval))
				return [node, node.gval]

		#Get node successors (note, will be a function rather than an attribute)
		children = node.successors
		if self.trace == 1:
			print('TRACE:{}: Current player is {}'.format(level,self.printPlayer(player)))
			print('TRACE:{}: Node {} has successors {}'.format(level,node,str(children)))
		choice = 0

		if player == 1:
			best_utility = -1 * float("inf")
		else:
			best_utility = float("inf")


		for child_node in children:
			if self.trace == 1:
				print('TRACE:{}: Searching Node {}'.format(level,child_node))
			[opp_choice, utility] = self.gtRecurse(child_node, level+1, player * -1, alpha, beta)
			if player == 1:
				if utility > best_utility:
					best_utility = utility
					choice = child_node
					#Implementation of alpha pruning
					alpha = best_utility
					if alpha > beta:
						pruned = True
						break
			else:
				if utility < best_utility:
					best_utility = utility
					choice = child_node
					#Implementation of beta pruning
					beta = best_utility
					if beta > alpha:
						pruned = True
						break
		if self.trace == 1:
			if pruned == True:
				print('TRACE:{}: Pruned Node {} with alpha-beta pruning'.format(level, child_node))
			print('TRACE:{}: {} choosing Node {} with Gval {}'.format(level, self.printPlayer(player), choice, best_utility))
		return [choice, best_utility]
