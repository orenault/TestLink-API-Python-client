import re


class DocTestParser(object):
    """Find all externaltestcaseid's in a test's docstring.

    If your externaltestcaseid prefix is abc and the test has 'abc-123' in it's docstring.
    `DocTestParser('abc').get_testcases()` would return `['abc-123']`.
    """
    def __init__(self, doc_matcher=None, doc_matchers=None):
        """
        :param doc_matchers: List of regex to find in docstring
        """
        self.doc_matchers = doc_matchers if doc_matchers is not None else []
        if doc_matcher:
            self.doc_matchers.append(doc_matcher)

    def get_testcases(self, test):
        testcases = set()
        for matcher in self.doc_matchers:
            testcases |= set(re.findall('{}-\d+'.format(matcher), test.doc))
        return testcases
