#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012 Luiko Czub, TestLink-API-Python-client developers
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
# works with the example project NEW_PROJECT_API  (see TestLinkExample.py)
# FIME LC 29.10.29: test does not really interacts with test link
#                   only negative test with none existing IDs implemented
#                   ok to check every implemented server call one time but not
#                   to cover all possible responses or argument combinations

import unittest
from testlink import TestlinkAPIClient, TestLinkHelper


class TestLinkAPIOnlineTestCase(unittest.TestCase):
    """ TestCases for TestlinkAPIClient - interacts with a TestLink Server.
    works with the example project NEW_PROJECT_API (see TestLinkExample.py)
    """

    def setUp(self):
        self.client = TestLinkHelper().connect(TestlinkAPIClient)


#    def tearDown(self):
#        pass


    def test_checkDevKey(self):
        response = self.client.checkDevKey()
        self.assertEqual(True, response)
        
    def test_about(self):
        response = self.client.about()
        self.assertIn('Testlink API', response)

    def test_ping(self):
        response = self.client.ping()
        self.assertEqual('Hello!', response)

    def test_echo(self):
        response = self.client.echo('Yellow Submarine')
        self.assertEqual('You said: Yellow Submarine', response)
        
    def test_doesUserExist_unknownID(self):
        response = self.client.doesUserExist('Big Bird')
        self.assertIn('Big Bird', response[0]['message'])
        self.assertEqual(10000, response[0]['code'])
        
    def test_getBuildsForTestPlan_unknownID(self):
        response = self.client.getBuildsForTestPlan(4711)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(3000, response[0]['code'])
        
    def test_getFirstLevelTestSuitesForTestProject_unknownID(self):
        response = self.client.getFirstLevelTestSuitesForTestProject(4711)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(7000, response[0]['code'])

    def test_getFullPath_unknownID(self):
        response = self.client.getFullPath(4711)
        self.assertIn('getFullPath', response[0]['message'])
        self.assertEqual(234, response[0]['code'])

    def test_getLastExecutionResult_unknownID(self):
        response = self.client.getLastExecutionResult(4711, 4712)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(3000, response[0]['code'])
        
    def test_getLatestBuildForTestPlan_unknownID(self):
        response = self.client.getLatestBuildForTestPlan(4711)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(3000, response[0]['code'])
        
    def test_getProjects(self):
        response = self.client.getProjects()
        self.assertIsNotNone(response)
        
    def test_getProjectTestPlans_unknownID(self):
        response = self.client.getProjectTestPlans(4711)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(7000, response[0]['code'])
        
    def test_getTestCase_unknownID(self):
        response = self.client.getTestCase(4711)
        # FAILURE in 1.9.3 API message: replacement does not work
        # The Test Case ID (testcaseid: %s) provided does not exist!
        #self.assertIn('4711', response[0]['message'])
        self.assertEqual(5000, response[0]['code'])
        
    def test_getTestCaseAttachments_unknownID(self):
        response = self.client.getTestCaseAttachments(4711)
        # FAILURE in 1.9.3 API message: replacement does not work
        # The Test Case ID (testcaseid: %s) provided does not exist!
        #self.assertIn('4711', response[0]['message'])
        self.assertEqual(5000, response[0]['code'])
        
    def test_getTestCaseCustomFieldDesignValue_unknownID(self):
        response = self.client.getTestCaseCustomFieldDesignValue(
                   4712, 1, 4711, 'a_field', 'a_detail')
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(7000, response[0]['code'])
        
    def test_getTestCaseIDByName_unknownID(self):
        response = self.client.getTestCaseIDByName('Big Bird')
        self.assertIn('getTestCaseIDByName', response[0]['message'])
        self.assertEqual(5030, response[0]['code'])

    def test_getTestCasesForTestPlan_unknownID(self):
        response = self.client.getTestCasesForTestPlan(4711)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(3000, response[0]['code'])

    def test_getTestCasesForTestSuite_unknownID(self):
        response = self.client.getTestCasesForTestSuite(4711, 2, 'a_detail')
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(8000, response[0]['code'])

    def test_getTestPlanByName_unknownID(self):
        response = self.client.getTestPlanByName('project 4711', 'plan 4712')
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(7011, response[0]['code'])

    def test_getTestPlanPlatforms_unknownID(self):
        response = self.client.getTestPlanPlatforms(4711)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(3000, response[0]['code'])

    def test_getTestProjectByName_unknownID(self):
        response = self.client.getTestProjectByName('project 4711')
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(7011, response[0]['code'])

    def test_getTestSuiteByID_unknownID(self):
        response = self.client.getTestSuiteByID(4711)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(8000, response[0]['code'])

    def test_getTestSuitesForTestPlan_unknownID(self):
        response = self.client.getTestSuitesForTestPlan(4711)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(3000, response[0]['code'])

    def test_getTestSuitesForTestSuite_unknownID(self):
        response = self.client.getTestSuitesForTestSuite(4711)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(8000, response[0]['code'])

    def test_getTotalsForTestPlan_unknownID(self):
        response = self.client.getTotalsForTestPlan(4711)
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(3000, response[0]['code'])

    def test_createTestProject_unknownID(self):
        response = self.client.createTestProject('', 'P4711')
        self.assertIn('Empty name', response[0]['message'])
        self.assertEqual(7001, response[0]['code'])

    def test_createBuild_unknownID(self):
        response = self.client.createBuild(4711, 'Build 4712', 'note 4713')
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(3000, response[0]['code'])

    def test_createTestPlan_unknownID(self):
        response = self.client.createTestPlan('plan 4711', 'project 4712')
        self.assertIn('4712', response[0]['message'])
        self.assertEqual(7011, response[0]['code'])

    def test_createTestSuite_unknownID(self):
        response = self.client.createTestSuite( 4711, 'suite 4712', 'detail 4713')
        self.assertIn('4711', response[0]['message'])
        self.assertEqual(7000, response[0]['code'])

    def test_createTestCase_unknownID(self):
        response = self.client.createTestCase('case 4711', 4712, 4713, 
                                               'Big Bird', 'summary 4714')
        self.assertIn('4713', response[0]['message'])
        self.assertEqual(7000, response[0]['code'])

    def test_reportTCResult_unknownID(self):
        response = self.client.reportTCResult(4711, 4712, 'build 4713', 'p', 
                                              'note 4714')
        # FAILURE in 1.9.3 API message: replacement does not work
        # The Test Case ID (testcaseid: %s) provided does not exist!
        #self.assertIn('4711', response[0]['message'])
        self.assertEqual(5000, response[0]['code'])

#    def test_uploadExecutionAttachment_unknownID(self):
#        response = self.client.uploadExecutionAttachment('file 4711', 4712, 
#                        'title 4713', 'descr. 4714')
#        self.assertIn('4711', response[0]['message'])

    def test_getProjectIDByName_unknownID(self):
        response = self.client.getProjectIDByName('project 4711')
        self.assertEqual(-1, response)

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()