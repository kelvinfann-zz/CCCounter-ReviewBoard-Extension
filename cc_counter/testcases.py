import os

from ccreader import analyze_file, get_comparison_data
from utils import track_func_ccchanges

TESTFILE_DIR = "testfiles"
TEST_FILE1 = "Util.java"
TEST_FILE2 = "Solver.java"
TEST_FILE3 = "Solver2.java"

TEST_FILES = [TEST_FILE1, TEST_FILE2, TEST_FILE3]
TEST_FILES = [os.path.join(TESTFILE_DIR, test_file) for test_file in TEST_FILES]

def main():
	test_all()

def test_all():

	check_dirr()
	test_analyze_file()
	test_get_full_function_names()

def pass_tests(function_name):
	pass_tests = "\n\tPasses All Tests for: "
	print pass_tests + function_name + "\n"
	return True

def check(boolean, pass_msg=None, fail_msg="A Test Error"):
	if boolean:
		if pass_msg is not None: print(pass_msg)
	else:
		raise Exception(fail_msg)

def check_dirr():
	print
	function_name = "Test File Checker Utility"
	check(os.path.exists(TESTFILE_DIR),
		pass_msg="Test File '" + TESTFILE_DIR + "' found",
		fail_msg="Test File directory not able to located")
	for test_file in TEST_FILES:
		check(os.path.exists(test_file),
			pass_msg="Test File '" + test_file + "' found",
			fail_msg="Test file '" + test_file + "' not able to located")

	print("\n\tAll Tests Files Found\n")
	return True


def test_analyze_file():
	function_name = "analyze_file"
	files = list(analyze_file(test_file) for test_file in TEST_FILES)
	for file_analysis in files:
		print file_analysis.keys()
		check(type(file_analysis) is dict,
			fail_msg=function_name + " returning wrong type, should be dict")
		for function in file_analysis:
			check(type(function) is str,
				fail_msg=function_name + " returning wrong type, should be str")
			check(type(file_analysis[function]) is dict,
				fail_msg=function_name + " returning wrong type, should be dict")
			for linenum in file_analysis[function]:
				print file_analysis[function][linenum]
	for test_file in TEST_FILES:
		print test_file + " returned correct analysis"
	return pass_tests(function_name)


def test_get_full_function_names():
	function_name = "get_full_function_names"
	t = [get_comparison_data(test_file) for test_file in TEST_FILES]
	print t
	print 
	print track_func_ccchanges( TEST_FILES[1], TEST_FILES[2])
	print
	print track_func_ccchanges( TEST_FILES[0], TEST_FILES[1])
	return pass_tests(function_name)

if __name__ == "__main__":
	main()



