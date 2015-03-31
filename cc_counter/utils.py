
def track_func_changes(cc_new, titles_new, cc_orig, titles_orig):
	"""Returns a list of dictionary entries for the net change in cyclomatic complexity
	of all the functions between 
	"""
	
	changed_functions = list()
	
	for function in cc_new:
		if function not in cc_orig:
			changed_functions += format_entries(function, cc_new)
		else:
			changed_functions += compare_function(function, cc_new[function],
				titles_new[function], cc_orig[function], titles_orig[function])


def format_entries(function, ccdata):
	
	entries = list()
	for linenum in ccdata[function]:
		entries += [{
			"function": function,
			"line": linenum,
			"cc": ccdata[function][linenum],
			}]
	return entries

def compare_function(function, func_cc_new, func_titles_new, func_cc_orig, func_titles_orig):
	
	changed = list()

	if len(func_cc_new) == 1 && len(func_cc_orig) == 1:
		new_linenum = func_cc_new.keys()[0]
		new_cc = func_cc_new[new_linenum]
		if new_cc != func_cc_orig[func_cc_new.keys()[0]]:
			changed += [{
				"function": function,
				"line": new_linenum,
				"cc": new_cc,
			}]
		return changed

	match = list()
	for linenum_new in func_titles_new:
		match += [(closest_func_match(func_titles_new[linenum_new], func_titles_orig), linenum_new)]
	match.sort()

	matched = set()

	for closest linenum_new	


def closest_func_match(title_new, func_titles_orig):
	closest_match = list()
	for linenum in func_titles_orig:
		closest_match += [(overlap(title_new, func_titles_orig[linenum]), linenum)]
	closest_match.sort()
	return closest_match[::-1]

def overlap(set_one, set_two):
	count = 0
	for item in set_one:
		if item in set_two: count+=1
	return count/len(set_one)

class ccfunc:
	def __init__(self, function, line, cc):
		self.function = function
		self.line = line
		self.cc = cc

	def format_output(self):
		return {"function": self.function,
			"line": self.line,
			"cc": self.cc,
			}

