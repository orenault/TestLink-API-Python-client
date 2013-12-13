Changes in TestLink-API-Python-client Source Distribution
=========================================================

TestLink-API-Python-client UNDER DEVELOP v0.4.7
-----------------------------------------------

implement missing 1.9.8 api methods - TestCase
- addTestCaseToTestPlan 

TestLink-API-Python-client release notes v0.4.6 (Dec. 2013)
-----------------------------------------------------------

TestLink-API-Python-client is now installable via PyPI #15

    pip install TestLink-API-Python-client

new api methods for Platforms implemented #10

- createPlatform, getProjectPlatforms
- addPlatformToTestPlan, removePlatformFromTestPlan

TestLink-API-Python-client release notes v0.4.5 (Nov. 2013)
-----------------------------------------------------------

All v0.4.0 API methods from TestlinkAPIClient are shifted to the new super class
TestlinkAPIGeneric and could be used with the new optional argument handling and
asked with whatArgs() for there arguments.

- getProject, createTestProject, createTestCase, createTestSuite, createTestPlan, 
  createTestCase
- createBuild, reportTCResult, uploadExecutionAttachment, 
- getTestProjectByName, getProjectTestPlans, getTotalsForTestPlan, getBuildsForTestPlan
- getLatestBuildForTestPlan, getTestPlanByName
- getTestSuitesForTestPlan, getTestSuiteByID, getTestSuitesForTestSuite, 
  getFirstLevelTestSuitesForTestProject 
- getTestCasesForTestSuite, getTestCasesForTestPlan, getTestCaseIDByName, getFullPath
- getLastExecutionResult, getTestCaseCustomFieldDesignValue, getTestCaseAttachments

Other API methods can be used with the new method

- callServerWithPosArgs(apiMethodame, [apiArgName=apiArgValue])

generic api class TestlinkAPIGeneric #7 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
new class TestlinkAPIGeneric implements the Testlink API methods as generic PY methods
    
- all arguments of Teslink API are supported as optional arguments
- often used (or mandatory) arguments can be configured as positional arguments
- error handling for TestLink API error codes

class TestlinkAPIClient inherits now from TestlinkAPIGeneric the Testlink API methods

- configuration for positional arguments are consistent with v0.4.0
  - except getTestCaseIDByName (see ac6ccf5)

Attention - handling for optional arguments has been changed. Existing code, 
which uses TestlinkAPIClient, must be adapted. Changes between v0.4.5 and v.0.4.0 
are documented in `example/TestLinkExample.py`

public API method callServerWithPosArgs() #4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Every implemented API method uses the new method callServerWithPosArgs() to call
the server and check the response for error codes.

- If the response include an error code, a TLResponseError is raised

This method can although be used to call not yet implemented API methods.

helper method .whatArgs(apiMethodName) #8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Teslink API Client can now be asked, what arguments a API method expects::

	import testlink
	tlh = testlink.TestLinkHelper()
	tls = tlh.connect(testlink.TestlinkAPIClient)
	print tls.whatArgs('createTestPlan')
	createTestPlan(<testplanname>, <testprojectname>, [note=<note>], [active=<active>], [public=<public>], [devKey=<devKey>])
	 create a test plan 

or for a description of all implemented api method ::

	import testlink
	tlh = testlink.TestLinkHelper()
	tls = tlh.connect(testlink.TestlinkAPIClient)
	for m in testlink.testlinkargs._apiMethodsArgs.keys():
		print tls.whatArgs(m), '\n'

other changes
~~~~~~~~~~~~~

see `Milestone v0.4.5 <https://github.com/lczub/TestLink-API-Python-client/issues?milestone=3&state=closed>`_
