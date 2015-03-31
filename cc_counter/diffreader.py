import os
import subprocess

from cc_counter.ccreader import analyze_file

def get_functions(filename):
	"""Takes in a file and outputs it's cyclometric complexity and the full headers of
	the functions 
	"""

	ccdata = analyze_file(filename)
	function_titles = get_function_titles(filename, ccdata)

	return ccdata, function_titles

	
def get_function_titles(filename, ccdata):
	"""Returns a dictionary of all the full function titles from the code file
	Format: { function_name: {line_num: function_title, ... }, ... }
	"""

	line_to_function = dict()
	pre_function_titles = dict()

	for function in ccdata:
		for linenum in ccdata[function]:
			line_to_function[linenum] = function
	
	with open(filename, 'r') as f:
		curr_linenum = 0
		for line in f:
			curr_linenum += 1
			if curr_linenum in line_to_function:
				function_name = line_to_function[curr_linenum]
				if function_name not in pre_function_titles:
					pre_function_titles[function_name] = dict()
				pre_function_titles[function_name][curr_linenum] = line

	return parameter_parser(pre_function_titles)

def parameter_parser(function_titles):
	"""Formats the function_titles into sets of the parameters destructively.
	Takes in a dictionary of unformated function_titles and formats the titles 
	inplace
	"""

	parameters = dict()

	for function in function_titles:
		for linenum in function_titles[function]:
			parameters =  _parameter_parser(function_titles[function][linenum])
			function_titles[function][linenum] = parameters

	return function_titles

def _parameter_parser(function_title):
	"""The actual formating function, takes in a function title line (str) and 
	outputs a set of the function's parameters
	"""

	parameters = function_title.split('(', 1)[1:]
	parameters[-1] = parameters[-1].split(')', 1)[0]

	if len(parameters) != 1: 
		raise Exception("Has multiple '(' or ')' and split \
			is not accounting for them")
	return set(parameters[0].split(','))