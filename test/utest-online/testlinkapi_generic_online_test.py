#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2013-2017 Luiko Czub, TestLink-API-Python-client developers
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# ------------------------------------------------------------------------

# this test requires an online TestLink Server, which connection parameters
# are defined in environment variables
#     TESTLINK_API_PYTHON_DEVKEY and TESTLINK_API_PYTHON_DEVKEY
#
# works with the example project NEW_PROJECT_API_GENERIC
#  (see TestLinkExampleGenericApi.py)
# FIME LC 29.10.29: test does not really interacts with test link
#                   only negative test with none existing IDs implemented
#                   ok to check every implemented server call one time but not
#                   to cover all possible responses or argument combinations

import sys
import os.path

if sys.version_info[0] == 2 and sys.version_info[1] == 6:
    # py26 needs backport unittest2
    import unittest2 as unittest
else:
    import unittest
    
if sys.version_info[0] == 2 and sys.version_info[1] == 7:
    # py27 and py31 assertRaisesRegexp was renamed in py32 to assertRaisesRegex
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp
    # py27 and py31 assertRegexpMatches was renamed in py32 to assertRegex
    unittest.TestCase.assertRegex = unittest.TestCase.assertRegexpMatches


from testlink import TestlinkAPIGeneric, TestLinkHelper
from testlink.testlinkerrors import TLResponseError

# example text file attachment = this python file
# why not using os.path.realpath(__file__)
# -> cause __file__ could be compiled python file *.pyc, if the test run is 
#    repeated without changing the test code
ATTACHMENT_EXAMPLE_TEXT= os.path.join(os.path.dirname(__file__), 
                                      'testlinkapi_generic_online_test.py')

class TestLinkAPIGenericOnlineTestCase(unittest.TestCase):
    """ TestCases for TestlinkAPIClient - interacts with a TestLink Server.
    works with the example project NEW_PROJECT_API (see TestLinkExample.py)
    """

    def setUp(self):
        self.client = TestLinkHelper().connect(TestlinkAPIGeneric)

#    def tearDown(self):
#        pass

    def test_checkDevKey(self):
        response = self.client.checkDevKey()
        self.assertEqual(True, response)
        
    def test_checkDevKey_unknownKey(self):
        with self.assertRaisesRegex(TLResponseError, '2000.*invalid'):
            self.client.checkDevKey(devKey='unknownKey')
        
    def test_sayHello(self):
        response = self.client.sayHello()
        self.assertEqual('Hello!', response)

    def test_repeat(self):
        response = self.client.repeat('Yellow Submarine')
        self.assertEqual('You said: Yellow Submarine', response)
        
    def test_about(self):
        response = self.client.about()
        self.assertIn('Testlink API', response)

    def test_doesUserExist_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '10000.*Big Bird'):
            self.client.doesUserExist('Big Bird')
        
    def test_createTestProject_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7001.*Empty name'):
            self.client.createTestProject(testprojectname='', 
                                                 testcaseprefix='P40000711')
 
    def test_createTestProject_unknownITS(self):
        with self.assertRaisesRegex(TLResponseError, '13000.*Unable to find'):
            self.client.createTestProject(testprojectname='aProject', 
                                testcaseprefix='aPrefix', itsname='unknownITS')
 
    def test_getProjects(self):
        response = self.client.getProjects()
        self.assertIsNotNone(response)
         
    def test_createTestPlan_projectname_posArg_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7011.*40000712'):
            self.client.createTestPlan('plan 40000711', 'project 40000712')
 
    def test_createTestSuite_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.createTestSuite( 40000711, 'suite 40000712', 'detail 40000713')
        
    def test_createTestCase_unknownID(self):
        tc_steps = []
        with self.assertRaisesRegex(TLResponseError, '7000.*40000713'):
            self.client.createTestCase('case 40000711', 40000712, 40000713, 
                                        'Big Bird', 'summary 40000714', tc_steps)
 
    def test_getBuildsForTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.getBuildsForTestPlan(40000711)
         
    def test_getFirstLevelTestSuitesForTestProject_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.getFirstLevelTestSuitesForTestProject(40000711)
 
    def test_getFullPath_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, 'getFullPath.*234'):
            self.client.getFullPath('40000711')
 
    def test_getLastExecutionResult_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.getLastExecutionResult(40000711, testcaseid=40000712)
         
    def test_getLatestBuildForTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.getLatestBuildForTestPlan(40000711)
         
    def test_getProjectTestPlans_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.getProjectTestPlans(40000711)
         
    def test_getProjectPlatforms_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.getProjectPlatforms(40000711)
        
    def test_getTestCase_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5000.*40000711'):
            self.client.getTestCase(testcaseid=40000711)
         
    def test_getTestCase_unknownExternalID(self):
        with self.assertRaisesRegex(TLResponseError, '5040.*GPROAPI-40000711'):
            self.client.getTestCase(testcaseexternalid='GPROAPI-40000711')
            
    def test_getTestCaseAttachments_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5000.*40000711'):
            self.client.getTestCaseAttachments(testcaseid=40000711)
         
    def test_getTestCaseCustomFieldDesignValue_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.getTestCaseCustomFieldDesignValue(
                   'TC-40000712', 1, 40000711, 'a_field', details='full')
         
    def test_getTestCaseIDByName_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5030.*Cannot find'):
            self.client.getTestCaseIDByName('Big Bird')
 
    def test_getTestCasesForTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.getTestCasesForTestPlan(40000711)
 
    def test_getTestCasesForTestSuite_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '8000.*40000711'):
            self.client.getTestCasesForTestSuite(40000711)
 
    def test_getTestPlanByName_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7011.*40000711'):
            self.client.getTestPlanByName('project 40000711', 'plan 40000712')
 
    def test_getTestPlanPlatforms_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.getTestPlanPlatforms(40000711)
 
    def test_getTestProjectByName_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7011.*40000711'):
            self.client.getTestProjectByName('project 40000711')
 
    def test_getTestSuiteByID_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '8000.*40000711'):
            self.client.getTestSuiteByID(40000711)
 
    def test_getTestSuitesForTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.getTestSuitesForTestPlan(40000711)
 
    def test_getTestSuitesForTestSuite_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '8000.*40000711'):
            self.client.getTestSuitesForTestSuite(40000711)
 
    def test_getTotalsForTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.getTotalsForTestPlan(40000711)
 
    def test_createBuild_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.createBuild(40000711, 'Build 40000712', buildnotes='note 40000713')
 
    def test_reportTCResult_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5000.*40000711'):
            self.client.reportTCResult(40000712, 'p', testcaseid=40000711, 
                                       buildname='build 40000713', notes='note 40000714' )
 
    def test_uploadExecutionAttachment_unknownID(self):
        attachemantFile = open(os.path.realpath(__file__), 'r')
        with self.assertRaisesRegex(TLResponseError, '6004.*40000712'):
            self.client.uploadExecutionAttachment(attachemantFile, 40000712, 
                        title='title 40000713', description='descr. 40000714')
 
    def test_createPlatform_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7011.*40000711'):
            self.client.createPlatform('Project 40000711', 'Platform 40000712', 
                                       notes='note 40000713')
            
    def test_addPlatformToTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.addPlatformToTestPlan(40000711, 'Platform 40000712')
            
    def test_removePlatformFromTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.removePlatformFromTestPlan(40000711, 'Platform 40000712')
            
    def test_addTestCaseToTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.addTestCaseToTestPlan(40000711, 40000712, 'N-40000713', 1)
            
    def test_updateTestCase_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5040.*N-40000711'):
            self.client.updateTestCase('N-40000711', version=1)
        
    def test_createTestCaseSteps_unknownID(self):
        steps = [{'actions' : "Step action 6 -b added by updateTestCase" , 
                  'expected_results' : "Step result 6 - b added", 
                  'step_number' : 6, 'execution_type' : 1}]
        with self.assertRaisesRegex(TLResponseError, '5040.*N-40000711'):
            self.client.createTestCaseSteps('update', steps, 
                                        testcaseexternalid='N-40000711', version=1)
            
    def test_deleteTestCaseSteps_unknownID(self):
        steps = [2,8]
        with self.assertRaisesRegex(TLResponseError, '5040.*N-40000711'):
            self.client.deleteTestCaseSteps('N-40000711', steps, version=1)
            
    def test_uploadRequirementSpecificationAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '6004.*40000712'):
            self.client.uploadRequirementSpecificationAttachment(attachemantFile, 40000712, 
                        title='title 40000713', description='descr. 40000714')
 
    def test_uploadRequirementAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '6004.*40000712'):
            self.client.uploadRequirementAttachment(attachemantFile, 40000712, 
                        title='title 40000713', description='descr. 40000714')
 
    def test_uploadTestProjectAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '7000.*40000712'):
            self.client.uploadTestProjectAttachment(attachemantFile, 40000712, 
                        title='title 40000713', description='descr. 40000714')
 
    def test_uploadTestSuiteAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '8000.*40000712'):
            self.client.uploadTestSuiteAttachment(attachemantFile, 40000712, 
                        title='title 40000713', description='descr. 40000714')
 
    def test_uploadTestCaseAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '5000.*testcaseid'):
            self.client.uploadTestCaseAttachment(attachemantFile, 40000712, 
                        title='title 40000713', description='descr. 40000714')
 
    def test_uploadAttachment_unknownID(self):
        attachemantFile = open(ATTACHMENT_EXAMPLE_TEXT, 'r')
        with self.assertRaisesRegex(TLResponseError, '6004.*Invalid Foreign Key ID'):
            self.client.uploadAttachment(attachemantFile, '0000', 'nodes_hierarchy',
                        title='title 40000713', description='descr. 40000714')

    def test_testLinkVersion(self):
        response = self.client.testLinkVersion()
        self.assertRegex(response, '\d*\.\d*\.\d*')

    def test_getUserByLogin_unknownKey(self):
        with self.assertRaisesRegex(TLResponseError, '10000.*User Login'):
            self.client.getUserByLogin('unknownUser')
            
    def test_getUserByID_unknownKey(self):
         with self.assertRaisesRegex(TLResponseError, 'NO_USER_BY_ID_LOGIN.*User with DB ID'):
            self.client.getUserByID(40000711)
            
#     def test_setTestMode(self):
#         response = self.client.setTestMode(True)
#         self.assertTrue(response)
#         response = self.client.setTestMode(False)
#         self.assertTrue(response)

    def test_deleteExecution_unknownKey(self):
        try:
            response = self.client.deleteExecution(40000711)
            # case: TL configuration allows deletion of executions
            # response returns Success, even if executionID is unkown
            self.assertEqual([{'status': True, 'message': 'Success!', 'id': 40000711, 
                               'operation': 'deleteExecution'}], response)
        except TLResponseError as tl_err:
            # case: TL configuration does not allow deletion of executions
            # Expects: 232: Configuration does not allow delete executions
            self.assertEqual(232, tl_err.code)

    def test_setTestCaseExecutionType_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000712'):
            self.client.setTestCaseExecutionType('N-40000711', 1, 40000712, 1)
            
    def test_assignRequirements_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000712'):
            self.client.assignRequirements('N-40000711', 40000712, 
                        [{'req_spec' : 40000713, 'requirements' : [40000714, 40000717]}, 
                         {'req_spec' : 4723, 'requirements' : [4725]}])
            
    def test_getExecCountersByBuild_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.getExecCountersByBuild(40000711)
            
    def test_getTestCaseCustomFieldExecutionValue_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '236.*version/executionid'):
            self.client.getTestCaseCustomFieldExecutionValue(
                            'cf_full', '40000711', 1, '715', '40000713')
            
    def test_getTestCaseCustomFieldTestPlanDesignValue_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.getTestCaseCustomFieldTestPlanDesignValue(
                            'cf_full', '40000711', 1, '40000713', '615')
            
    def test_updateTestCaseCustomFieldDesignValue_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.updateTestCaseCustomFieldDesignValue(
                            'TC-40000712', 1, 40000711, {'cf_field1' : 'value1',
                                                 'cf_field2' : 'value2'})

    def test_getTestSuiteCustomFieldDesignValue_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.getTestSuiteCustomFieldDesignValue(
                                                    'cf_full', 40000711, 40000713) 
            
    def test_getTestPlanCustomFieldDesignValue_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.getTestPlanCustomFieldDesignValue(
                                                    'cf_full', 40000711, 40000712)             

    def test_getReqSpecCustomFieldDesignValue_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.getReqSpecCustomFieldDesignValue(
                                                    'cf_full', 40000711, 4732)             

    def test_getRequirementCustomFieldDesignValue_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.getRequirementCustomFieldDesignValue(
                                                    'cf_full', 40000711, 4734)  
            
    def test_assignTestCaseExecutionTask_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.assignTestCaseExecutionTask('username', 40000711, 'TC-40000712', 
                                            buildname='build 40000713', 
                                            platformname='platform 40000714') 
              
    def test_getTestCaseBugs_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.getTestCaseBugs(40000711, testcaseexternalid='TC-40000712', 
                                        buildname='build 40000713',
                                        platformname='platform 40000714')                         

    def test_getTestCaseAssignedTester_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.getTestCaseAssignedTester(40000711, 'TC-40000712', 
                                            buildname='build 40000713', 
                                            platformname='platform 40000714') 
              
    def test_unassignTestCaseExecutionTask_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.unassignTestCaseExecutionTask(40000711, 'TC-40000712', 
                                        buildname='build 40000713', 
                                        platformname='platform 40000714',
                                        user='username',action='unassignOne') 
    
    def test_getProjectKeywords_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.getProjectKeywords(40000711) 

    def test_getTestCaseKeywords_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5040.*40000712'):
            self.client.getTestCaseKeywords(testcaseid=40000712) 

    def test_getTestCaseKeywords_unknownID_set(self):
        with self.assertRaisesRegex(TLResponseError, '5040.*40000712'):
            self.client.getTestCaseKeywords(testcaseid=[40000712, 40000713]) 

    def test_getTestCaseKeywords_unknownID_external_single(self):
        with self.assertRaisesRegex(TLResponseError, '5040.*TC-40000712'):
            self.client.getTestCaseKeywords(testcaseexternalid='TC-40000712')
            
    def test_getTestCaseKeywords_unknownID_external_set(self):
        with self.assertRaisesRegex(TLResponseError, '5040.*TC-40000712'):
            self.client.getTestCaseKeywords(testcaseexternalid=['TC-40000712', 'TC-40000713'])

    def test_deleteTestPlan_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '3000.*40000711'):
            self.client.deleteTestPlan(40000711) 

    def test_addTestCaseKeywords_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5040.*TC-40000712'):
            self.client.addTestCaseKeywords({'TC-40000712' :  
                                             ['KeyWord01', 'KeyWord03']}) 

    def test_removeTestCaseKeywords_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '5040.*TC-40000712'):
            self.client.removeTestCaseKeywords({'TC-40000712' : ['KeyWord01']}) 

    def test_deleteTestProject_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7013.*TProjectPrefix'):
            self.client.deleteTestProject('TProjectPrefix') 

    def test_createTestPlan_projectname_optArg_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7011.*40000712'):
            self.client.createTestPlan('plan 40000711', 
                                       testprojectname='project 40000712')

    def test_createTestPlan_prefix_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, 'NO.*TProjectPrefix'):
            self.client.createTestPlan('plan 40000713', 
                                       prefix='TProjectPrefix')

    def test_updateTestSuiteCustomFieldDesignValue_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000712'):
            self.client.updateTestSuiteCustomFieldDesignValue(
                            '40000712 TP-ID', '40000711 TS-ID',  
                            {'cf_tc_ex_string' : 'a custom exec value', 
                             'cf_tc_ex_numeric' : 111} )

    def test_getTestSuite_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, 'NO.*TProjectPrefix'):
            self.client.getTestSuite('suite 40000712', 'TProjectPrefix')
            

    def test_updateTestSuite_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000711'):
            self.client.updateTestSuite(40000712, testprojectid=40000711, 
                                    testsuitename = 'suite 40000712 updated',
                                    details = 'detail 40000713 updated',
                                    order =1)
            
    def test_getIssueTrackerSystem_unknownITS(self):
        with self.assertRaisesRegex(TLResponseError, '13000.*Unable to find'):
            self.client.getIssueTrackerSystem('unknownITS')
 
    def test_updateBuildCustomFieldsValues_unknownID(self):
        with self.assertRaisesRegex(TLResponseError, '7000.*40000712'):
            self.client.updateBuildCustomFieldsValues(
                            '40000712 project', '40000713 plan', '40000714 build', 
                            {'cf_b_ex_string' : 'a custom exec value', 
                             'cf_b_ex_numeric' : 111} )
         
                                 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()