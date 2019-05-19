
#####################################################
#################  P R O J E C T  2  ################
#####################################################
#                       CS4613                      #
#                 Baizhou David Hou                 #
#                       bh1762                      #
#####################################################

# An Implementation of a sudoku solver using a
# constraint satisfaction problem model. 

######################################################
######        The Solution must return:          #####
######################################################
#       9x9 output that represents the solution.     #
######################################################

import SudoSolve

######################################################
#     __  __ _____ _____ _   _  ___  ____  ____      #
#    |  \/  | ____|_   _| | | |/ _ \|  _ \/ ___|     #
#    | |\/| |  _|   | | | |_| | | | | | | \___ \     #
#    | |  | | |___  | | |  _  | |_| | |_| |___) |    #
#    |_|  |_|_____| |_| |_| |_|\___/|____/|____/     #
#                                                    #
######################################################

# Produce entry points for search algorithm from file.
def InitFromFile(targetFile):
	initialMap = [];

	f = open(targetFile);
	fLines = f.readlines();
	f.close();

	# Getting initial map
	for line in fLines:
		nums = line.split();
		curLine = [];
		for num in nums:
			curLine.append(int(num));
		initialMap.append(curLine);

	# Generate a search instance from initial map.
	searchInstance = SudoSolve.SudokuSearch(initialMap);

	return searchInstance;

# Puts result into desired output format.
def GenerateOutput(outMap):
	out = "";

	for i in range(len(outMap)):
		for j in range(len(outMap[i])):
			out += str(outMap[i][j].value);
			out += " ";
		out += "\n";
	
	return out;


##################################
#     _____ _____ ____ _____     #
#    |_   _| ____/ ___|_   _|    #
#      | | |  _| \___ \ | |      #
#      | | | |___ ___) || |      #
#      |_| |_____|____/ |_|      #
#                                #
##################################

def main():

	# Usability
	fname = input("File Name -> ");

	# Initialize from file and create a search manager object.
	sudoSearch = InitFromFile(fname);
	result = sudoSearch.doSearch();
	output = GenerateOutput(sudoSearch.cellMap);
	output += "\n= = = = = = = = = = = = = = = = = =\n\n";
	output += GenerateOutput(result);

	print();
	print(output);

	#Write results to file if output name is specified.
	fname = "";
	fname = input("Output File Name (or ENTER to skip) -> ");
	if(fname != ""):
		writeout = open(fname, "w+");
		writeout.write(output);
		writeout.close();
		print("Saved.\n");
	else:
		print("Not saved.\n");



main();






