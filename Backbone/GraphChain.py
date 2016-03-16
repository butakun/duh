# $Id: GraphChain.py 44 2010-09-21 15:31:56Z kato $

class Graph(dict):

	def FindFirstNodes(self):

		nodes = self.keys()
		for node in self.keys():
			linkedNodes = self[node]
			for linkedNode in linkedNodes:
				if linkedNode in nodes:
					nodes.remove(linkedNode)
		return nodes

class Node(object):
	def __init__(self):
		self.Ready = False
	def Run(self):
		raise Error

def Test():

	graph = Graph()
	graph["A"] = ["B", "D"]
	graph["B"] = ["D"]
	graph["C"] = ["D"]
	graph["D"] = []

	print graph.FindFirstNodes()

if __name__ == "__main__":
	Test()

