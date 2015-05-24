class TestFunction:
    """
    """
    def __init__(self, name, function, testset=None):
        self.name = name
        self.function = function
        self.testset = testset
        if self.testset:
            self.testcases(self.testset)

    def testcases(self, testset):
        print "***Testing {0}***".format(self.name)
        for testparam, testexpected in testset:
            testactual = self.function(*testparam)
            statement = "Testcase {1}".format(self.name, testparam)
            if testactual == testexpected:
                pass_statement = "PASS: {0}".format(statement)
                print pass_statement
            else:
                error_statement = "{0}\n\tExpected: {1}\n\tGot: {2}".format(statement, testexpected, testactual)
                raise Exception(error_statement)

