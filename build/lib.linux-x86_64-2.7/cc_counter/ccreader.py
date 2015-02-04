import cc_counter.hfcca as hfcca

def analyze_file(filename):
	"""Returns a list of dictionary enetries that include the CC of the functions 
	in a file
	"""
	cyclomatic_complexity = []
	for file_statistics in hfcca_analyze(filename):
		for func in file_statistics:
			func_entry = {
				'CCN': func.cyclomatic_complexity,
				'name': func.name,
				'line': func.start_line,
			}
			cyclomatic_complexity.append(func_entry)
	return cyclomatic_complexity

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

def output_txt(txt_filename, input_txt, mode='w'):
	"""takes in a list of strings and outputs it to a textfile
	"""
	txt_file = open(txt_filename, mode)
	for s in input_txt:
		s = str(s) + "\n"
		txt_file.write(s)
	txt_file.close()
	return

