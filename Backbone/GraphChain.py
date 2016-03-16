#    duh, a heuristics-based design exploration code.
#    Copyright (C) 2016 Hiromasa Kato <hiromasa at gmail.com>
#
#    This file is part of duh.
#
#    duh is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    duh is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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

