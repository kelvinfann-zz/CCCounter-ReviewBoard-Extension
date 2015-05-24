import os
import cc_counter.hfcca as hfcca

class ccfunc(object):
	def __init__(self, function, line, cc, parameters=None):
		self.function = function
		self.line = line
		self.cc = cc
		self.parameters = parameters

	def __str__(self):
		return self.dict_form().__str__()

	def dict_form(self):
		return {"function": self.function,
			"line": self.line,
			"cc": self.cc,
			"parameters": self.parameters,
			}

	def __eq__(self, other): 
		r = False
		if isinstance(other, ccfunc):
			r = other.function == self.function
			r = r and other.line == self.line
			r = r and other.cc == self.cc
			r = r and other.parameters == self.parameters
		return r


def get_comparison_data(filename):
	"""Takes in a file and outputs it's cyclometric complexity analysis and the full 
	headers (titles) of the functions 
	"""
	file_analysis = analyze_file(filename)
	if file_analysis != None:
		add_function_titles(filename, file_analysis)
	return file_analysis
	
def add_function_titles(filename, file_analysis):
	"""Adds to file_analysis the full function titles from the code file into the parameters
	component of the ccfunc object
	"""
	line_to_function = dict()
	for function in file_analysis:
		for linenum in file_analysis[function]:
			line_to_function[linenum] = function
	with open(filename, 'r') as f:
		curr_linenum = 0
		for line in f:
			curr_linenum += 1
			if curr_linenum in line_to_function:
				function_name = line_to_function[curr_linenum]
				file_analysis[function_name][curr_linenum].parameters = line
	return parameter_parser(file_analysis)

def parameter_parser(file_analysis):
	"""Formats the function_titles into sets of the parameters destructively.
	Takes in a dictionary of unformated function_titles and formats the titles 
	inplace
	"""
	parameters = dict()
	for function in file_analysis:
		for linenum in file_analysis[function]:
			parameters =  _parameter_parser(file_analysis[function][linenum].parameters)
			file_analysis[function][linenum].parameters = parameters
	return file_analysis

def _parameter_parser(function_title):
	"""The actual formating function, takes in a function title line (str) and 
	outputs a set of the function's parameters
	"""
	parameters = function_title.replace(" ", "") #Strips whitespace
	parameters = parameters.split('(', 1)[1:] #Identifies parameter beginning
	parameters[-1] = parameters[-1].rsplit(')', 1)[0] #identifies parameter end
	if len(parameters) != 1: 
		raise Exception("Has multiple '(' or ')' and split \
			is not accounting for them")
	return set(parameters[0].split(','))

def analyze_file(filename):
	"""Returns a list of function dictionary entries that include the CC of the functions 
	in a file
	"""
	file_analysis = dict()
	for file_statistics in hfcca_analyze(filename):
		for func in file_statistics:
			if func.name not in file_analysis:
				file_analysis[func.name] = dict()
			if func.start_line in file_analysis[func.name]:
				raise Exception("Currently does not support code that has multiple functions \
					stacked on a single line. Will probably never support code that looks \
					that hideous")
			file_analysis[func.name][func.start_line] = ccfunc(func.name, func.start_line, 
				func.cyclomatic_complexity)
	return file_analysis

def hfcca_analyze(filename):
	"""A wrapper for the hfcca's analyze function.
	"""
	options = hfcca.createHfccaCommandLineParser().parse_args(args=[])[0]
	fileAnalyzer = hfcca.FileAnalyzer(options.no_preprocessor_count)
	return hfcca.mapFilesToAnalyzer([filename], fileAnalyzer, options.working_threads)

def func_identifier(filename):
	"""Returns a list of function names
	"""
	for file_stats in hfcca_analyze(filename):
		#we just return immidently since there is only one file in the hfcca analyze
		return [func.name for func in file_stats]
	raise TypeError
