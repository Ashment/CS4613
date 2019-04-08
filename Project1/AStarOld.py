
#####################################################
#################  P R O J E C T  1  ################
#####################################################
#                       CS4613                      #
#                 Baizhou David Hou                 #
#                       bh1762                      #
#####################################################

# This file contains the implementations of the classes
# 	and methods pretaining to the A* algorithm used
# 	in the 8Puzzle solution script.

import copy

######################################################
#      ____ _        _    ____ ____  _____ ____      #
#     / ___| |      / \  / ___/ ___|| ____/ ___|     #
#    | |   | |     / _ \ \___ \___ \|  _| \___ \     #
#    | |___| |___ / ___ \ ___) |__) | |___ ___) |    #
#     \____|_____/_/   \_\____/____/|_____|____/     #
#                                                    #
######################################################

# This class keeps track of nodes and variables related to the search.
class AStarSearch:
	###   CLASS ATTRIBUTES   ###
	###    list explored     ###
	###    list goalMap      ###
	###    list priorityQ    ###

	def __init__(self, inRoot, goMap):
		self.priorityQ = [inRoot];
		self.explored = [];
		self.goalMap = goMap;
		self.totalNodes = 1;

	def doSearch(self):
		done = False;

		while not done:
		
			self.expandNode();
			# If next node to be expanded is solution, the search is done.
			if(self.priorityQ[-1].tMap == self.goalMap):
				done = True;

		# Return the solution node
		return self.priorityQ[-1];

	# Expands the first node in priority queue and adds children to the priority queue.
	def expandNode(self):
		print("ASTAR EXPANDING NODE")

		nNode = self.priorityQ.pop();
		potChildren = nNode.GenerateChildren();

		# Add children to queue if it is not a state already seen.
		for i in potChildren:
			match = False
			for j in self.explored:
				if i.tMap == j.tMap:
					match = True;

			if not match:
				self.priorityQ.append(i)
				self.totalNodes += 1;
				if(self.totalNodes % 5 == 0):
					print("Expanded Nodes:", self.totalNodes);
				self.explored.append(i);
				print("Seen Nodes: " ,len(self.explored));
#				print(i);

		self.priorityQ.sort(key=self.getNodeHeu, reverse=True);

		return 0;

	def getNodeHeu(self, inNode):
		return inNode.heu;

class StateNode:
	### CLASS ATTRIBUTES ###
	###    list tMap     ### >>> Element: [ [R1], [R2]. [R3] ]
	###     int heu      ### (stands for heuristic)
	###     int dep      ### (stands for depth) 
	###    list path     ### >>> Element: ["A" , StateNode]
	###     str heuT     ### (Stands for heu type)
	###     int fCost    ###

	##### CLASS METHODS ####
	def __init__(self, inMap, goMap, depth, inPath=[], heuType="A"):	
		self.tMap = inMap;
		self.gMap = goMap;
		self.dep = depth;
		self.path = inPath;

		self.heuT = heuType;
		self.heu = getHeuristicMan(self.tMap, goMap);
		if(self.heuT != "A"):
			self.heu += (2*getLinearConflicts(self.tMap, self.gMap));

		self.fCost = self.heu + self.dep;

		self.heu += depth;

	# Gets location of empty tile slot.
	def GetEmptyPos(self):
		found = False;
		xp = 0;
		yp = 0;

		while not found and (yp < 3):
			if(self.tMap[yp][xp] == 0):
				found = True;
			else:
				xp += 1;
				if(xp > 2):
					xp = 0;
					yp += 1;

		return (yp, xp);

	# Gets list of potential children of current state.
	def GenerateChildren(self):
		print("GENERATING CHILDREN")
		zPos = self.GetEmptyPos();
		potChildren = [];

		# Check left and right and swap to generate new state if valid.
		for xx in range(-1, 2, 2):
			nxx = zPos[1] + xx;
			nMap = copy.deepcopy(self.tMap);
			nPath = copy.deepcopy(self.path);

			if(nxx < 3 and nxx >= 0):
				if(xx < 0):
					nPath.append(("L", self));
				else:
					nPath.append(("R", self));

				nMap[zPos[0]][nxx], nMap[zPos[0]][zPos[1]] = nMap[zPos[0]][zPos[1]], nMap[zPos[0]][nxx];
				potChildren.append(StateNode(nMap, self.gMap, self.dep + 1, nPath, self.heuT));

		# Check up and down and swap to generate new state if valid.
		for yy in range(-1, 2, 2):
			nyy = zPos[0] + yy;
			nMap = copy.deepcopy(self.tMap);
			nPath = copy.deepcopy(self.path);
			
			if(nyy < 3 and nyy >= 0):
				if(yy < 0):
					nPath.append(("U", self));
				else:
					nPath.append(("D", self));

				nMap[nyy][zPos[1]], nMap[zPos[0]][zPos[1]] = nMap[zPos[0]][zPos[1]], nMap[nyy][zPos[1]];
				potChildren.append(StateNode(nMap, self.gMap, self.dep + 1, nPath, self.heuT));

		return potChildren;

	# Gives info on self in desired output format.
	def getOutput(self):
		out = "";
		for row in self.tMap:
			for each in row:
				out += str(each) + " ";
			out += "\n";

		return out;

	def __str__(self):
		out = "";
		for row in self.tMap:
			for each in row:
				out += str(each) + " ";
			out += "\n";

		out += "Heu: " + str(self.heu) + "\n";

		out += "Path: "
		for e in self.path:
			out += e[0];
			out += " ";
		out += "\n";

		return out;



######################################################
#     __  __ _____ _____ _   _  ___  ____  ____      #
#    |  \/  | ____|_   _| | | |/ _ \|  _ \/ ___|     #
#    | |\/| |  _|   | | | |_| | | | | | | \___ \     #
#    | |  | | |___  | | |  _  | |_| | |_| |___) |    #
#    |_|  |_|_____| |_| |_| |_|\___/|____/|____/     #
#                                                    #
######################################################

def getManhattanDist(targetVal, goalMap, startPos):
	print("GET MANHATTAN DISTANCE")
	if(targetVal == 0):
		return 0;

	tFound = False;
	cX = 0;
	cY = 0;

	# Find targetVal position in goalMap
	while not tFound:
		print("________Finding Target Val")
		if(goalMap[cY][cX] == targetVal):
			tFound = True;
		else:
			if(cX < 2):
				cX += 1;
			else:
				cX = 0;
				cY += 1;
	print("____Target Val Found.")

	# Get and return distance
	dist = abs(cX - startPos[1]) + abs(cY - startPos[0]);
	return dist;

# Get number of linear conflicts
def getLinearConflicts(tMap, goalMap):
	conflicts = 0;

	for i in range(len(tMap)):
#		print("ROW", i)
		# Check row i for linear conflicts.
		for xx in range(len(tMap)):
#			print("->", xx)
			gp = getgoalPos(tMap, [i, xx], goalMap);

			# If current tile on row has goal on this row.
			if(gp[0] == i):
				for xxx in range(len(tMap)):
					if(xxx > xx) and tMap[i][xx] != 0 and tMap[i][xxx] != 0:
						gp = getgoalPos(tMap, [i, xxx], goalMap);
						# If tile goal is also in the same row
						if (gp[0] == i):
							if (xxx > xx and gp[1] <= xx) or (xxx < xx and gp[1] >= xx):
								conflicts += 1;
#								print("---", tMap[i][xx], "<->", tMap[i][xxx],"conflicts:", conflicts)

#		print("COL", i)
		# Check row i for linear conflicts.
		for yy in range(len(tMap)):
#			print("->", yy)
			gp = getgoalPos(tMap, [yy, i], goalMap);

			# If current tile on column has goal on this column.
			if(gp[1] == i):
				for yyy in range(len(tMap)):
					if(yyy > yy) and tMap[yy][i] != 0 and tMap[yyy][i] != 0:
						gp = getgoalPos(tMap, [yyy, i], goalMap);
						# If tile goal is also in the same column
						if (gp[0] == i):
							if (yyy > yy and gp[0] <= yy) or (yyy < yy and gp[0] >= yy):
								conflicts += 1;
#								print("---", tMap[yy][i], "<->", tMap[yyy][i],"conflicts:", conflicts)

	return conflicts;

# Get goal position of tile at startPos in tMap
def getgoalPos(tMap, startPos, goalMap):
	tFound = False;
	cX = 0;
	cY = 0;

	targetVal = tMap[startPos[0]][startPos[1]];
	# Find targetVal position in goalMap
	while not tFound:
		if(goalMap[cY][cX] == targetVal):
			tFound = True;
		else:
			if(cX < 2):
				cX += 1;
			else:
				cX = 0;
				cY += 1;

	return [cY, cX];

# Sums manhattan distances of tiles in inMap to goMap
def getHeuristicMan(inMap, goalMap):
	retSum = 0;

	# Get manhattan distance of each tile and add to sum.
	for i in range(len(inMap)):
		for j in range (len(inMap)):
			retSum += getManhattanDist(inMap[i][j], goalMap, [i,j]);

	return retSum




