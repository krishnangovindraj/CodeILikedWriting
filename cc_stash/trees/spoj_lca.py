from __future__ import print_function

import sys
sys.setrecursionlimit(10**6)

# RMQ - preprocess 
class RMQ:
	def __init__(self, arr):
		self.arr = arr
		self.dp = None 

	def build(self):
		n = len(self.arr)
		log_max = 1 # the height of the array. 
		tmp = 2		# TODO: see if this shouldn't be 2?
		while tmp < n:
			tmp *= 2
			log_max += 1

		dp = [[i] for i in range(n)]
		
		gap = 1
		for j in range(1, log_max):
			for i in range(n):
				if i+gap < n:
					dp[i].append(dp[i][j-1] if self.arr[dp[i][j-1]] < self.arr[dp[i+gap][j-1]] else dp[i+gap][j-1])
				else:
					dp[i].append(dp[i][j-1])
			gap *= 2
		# That should complete dp
		self.dp = dp
		
	def query_indices(self, i, j):
		if j < i:
			t = j
			j = i
			i = t

		span_needed = (j-i+1)
		span_height = 0
		span = 2
		while span < span_needed:
			span*=2
			span_height += 1

		gap = (span//2)-1
		
		return self.dp[i][span_height] \
			if self.arr[self.dp[i][span_height]] < self.arr[self.dp[j-gap][span_height]] \
			 else self.dp[j-gap][span_height]

class LCA_RMQ:
	def __init__(self, adj_list, root):
		self.root = root
		self.adj_list = adj_list
		self.levels = None
		self.euler_path = None
		self.first_occurence = None
		self.rmq = None


	def preprocess(self):
		self.euler_path, self.levels = self.euler_path_levels_dfs()
		self.rmq = RMQ(self.levels)
		self.rmq.build()
		self.first_occurence = self.compute_first_occurence()

	# Euler path
	def euler_path_levels_dfs(self):
		euler_path = []
		levels = []
		self._euler_path_levels_dfs(self.root, 0, euler_path, levels)
		return euler_path, levels

	def _euler_path_levels_dfs(self, node, depth, path_so_far, levels_so_far):
		levels_so_far.append(depth)
		path_so_far.append(node)
		for c in self.adj_list[node]:
			self._euler_path_levels_dfs(c, depth+1, path_so_far, levels_so_far)
			levels_so_far.append(depth)
			path_so_far.append(node)

	def compute_first_occurence(self):
		n = len(self.euler_path)
		first_occurence = [-1 for i in range(n)]
		for i,p in enumerate(self.euler_path):
			if first_occurence[p] == -1:
				first_occurence[p] = i
		return first_occurence

	def lca(self, u,v):
		i = self.first_occurence[u]
		j = self.first_occurence[v]
		
		return self.euler_path[self.rmq.query_indices(i,j)]
	
# stack-DFS with factor tracker


# Factor tracker for each query



# Answer tracker


# input

def read_int():
	return int(raw_input())

def read_int_list():
	return list(map(int, raw_input().split(' ')))


# main
def spoj_lca():
	TC = read_int()
	for tc in range(TC):
		N = read_int() + 1
		children  = [[] for _ in range(N)]
		
		for i in range(1,N):
			children[i].extend(read_int_list()[1:])
		root = 1
		children[0] = [root]
		
		lca_rmq = LCA_RMQ(children, 0)
		lca_rmq.preprocess()
		Q = read_int()
		print("Case %d:"%(tc+1))
		while Q > 0 :
			Q -= 1
			u,v = read_int_list()
			print(lca_rmq.lca(u,v))

spoj_lca()