import cc_counter.ccreader as r
from testclass import TestFunction

"""
Tests:
    * func_identifier
    * analyze_file
    * add_function_titles

Does not test:
    * hfcca_analyze - its just a wrapper function
    * _parameter_parser - it is a helper function for parameter_parser
    * parameter_parser - it is just a linking function between add_function_titles and _parameter_parser
"""

def test_func_identifier():
    name = "func_identifier"
    function = r.func_identifier
    testset = [
        (["sample0.java"],
            []),
        (["sample1.java"],
            ["One"]),
        (["sample2.java"], 
            ["One", "EmptyClass", "SingleClass", "sccc2", "MultipleClass", "mccc4"]),
        ]
    TestFunction(name, function, testset=testset)

def test_analyze_file():
    name = "analyze_file"
    function = r.analyze_file
    testset = [
        (["sample0.java"],
            dict()),
        (["sample1.java"],
            {"One": {1: r.ccfunc("One", 1, 1)}}),
        (["sample2.java"],
            {"One": {1: r.ccfunc("One", 1, 1)},
            "EmptyClass": {3:r.ccfunc("EmptyClass", 3, 1)},
            "SingleClass": {6:r.ccfunc("SingleClass", 6, 1)},
            "sccc2": {7:r.ccfunc("sccc2", 7, 2)},
            "MultipleClass": {13:r.ccfunc("MultipleClass", 13, 1)},
            "mccc4": {14:r.ccfunc("mccc4", 14, 4)},
            }),
        ]
    TestFunction(name, function, testset=testset)

def test_add_function_titles():
    """
    """
    name = "parameter_parser"
    def function(filename):
        file_analysis = r.analyze_file(filename)
        file_analysis = r.add_function_titles(filename, file_analysis)
        for function in file_analysis:
            for ln in file_analysis[function]:
                file_analysis[function][ln] = file_analysis[function][ln].dict_form()
        return file_analysis
    testset = [
        (["sample0.java"],
            dict()),
        (["sample1.java"],
            {"One": {1: r.ccfunc("One", 1, 1, set([""])).dict_form()}}),
        (["sample2.java"],
            {"One": {1: r.ccfunc("One", 1, 1, set([""])).dict_form()},
            "EmptyClass": {3:r.ccfunc("EmptyClass", 3, 1, set([""])).dict_form()},
            "SingleClass": {6:r.ccfunc("SingleClass", 6, 1, set(["a"])).dict_form()},
            "sccc2": {7:r.ccfunc("sccc2", 7, 2, set(["a"])).dict_form()},
            "MultipleClass": {13:r.ccfunc("MultipleClass", 13, 1, set(["a", "b"])).dict_form()},
            "mccc4": {14:r.ccfunc("mccc4", 14, 4, set(["a", "b"])).dict_form()},
            }),
        ]
    TestFunction(name, function, testset=testset)

test_func_identifier()
test_analyze_file()
test_add_function_titles()
