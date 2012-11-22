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

# this test works WITHOUT an online TestLink Server
# no calls are send to a TestLink Server

import unittest
from testlink import TestlinkAPIClient, TestLinkHelper

# scenario_a includes response from a testlink 1.9.3 server
SCENARIO_A = {'getProjects' : [
               {'opt': {'requirementsEnabled': 0, 'testPriorityEnabled': 1, 
                        'automationEnabled': 1, 'inventoryEnabled': 0}, 
                'prefix': 'NPROAPI', 'name': 'NEW_PROJECT_API', 'color': '', 
                'notes': 'This is a Project created with the API', 
                'option_priority': '0', 
                'options': 'O:8:"stdClass":4:{s:19:"requirementsEnabled";i:0;s:19:"testPriorityEnabled";i:1;s:17:"automationEnabled";i:1;s:16:"inventoryEnabled";i:0;}', 
                'tc_counter': '2', 'option_reqs': '0', 'active': '1', 
                'is_public': '1', 'id': '21', 'option_automation': '0'}, 
               {'opt': {'requirementsEnabled': 1, 'testPriorityEnabled': 1, 
                        'automationEnabled': 1, 'inventoryEnabled': 1}, 
                'prefix': 'TP', 'name': 'TestProject', 'color': '', 
                'notes': '<p>Initiales TestProject, um &nbsp;TestLink kennen zu lernen</p>', 
                'option_priority': '0', 
                'options': 'O:8:"stdClass":4:{s:19:"requirementsEnabled";i:1;s:19:"testPriorityEnabled";i:1;s:17:"automationEnabled";i:1;s:16:"inventoryEnabled";i:1;}', 
                'tc_counter': '0', 'option_reqs': '0', 'active': '1', 
                'is_public': '1', 'id': '1', 'option_automation': '0'}],
              'getProjectTestPlans' : {
                '21' : [{'name': 'TestPlan_API', 
                         'notes': 'New TestPlan created with the API', 
                         'active': '1', 'is_public': '1', 
                         'testproject_id': '21', 'id': '22'}] ,
                '1' : '' },
              'getFirstLevelTestSuitesForTestProject' : {
                '21' :  [{'node_type_id': '2', 'name': 'A - First Level', 
                          'parent_id': '21', 'node_order': '0', 
                          'node_table': 'testsuites', 'id': '23'}, 
                         {'node_type_id': '2', 'name': 'B - First Level', 
                          'parent_id': '21', 'node_order': '0', 
                          'node_table': 'testsuites', 'id': '24'}],
                '1' : [{'message': '(getFirstLevelTestSuitesForTestProject) - Test Project (TestProject) is empty.', 
                        'code': 7008}] },
              'getTestSuitesForTestPlan' : {'22' : ''},
              'getTestCasesForTestPlan' : {'22' : ''},
              # TL(1.9.3)->getTestSuitesForTestSuite really returns {...} and not [{....}] !!!
              'getTestSuitesForTestSuite' : {
                '23' : {'node_type_id': '2', 'name': 'AA - Second Level', 
                        'parent_id': '23', 'node_order': '0', 
                        'details': 'Details of the Test Suite AA', 'id': '25'},
                '24' : ''},
              'getTestCasesForTestSuite' : {
                '23' : [{'node_type_id': '3', 'tcversion_id': '25', 
                         'name': 'TESTCASE_AA', 'parent_id': '25', 
                         'node_order': '0', 'node_table': 'testcases', 
                         'external_id': 'NPROAPI-1', 'id': '26'}],
                '24' : [{'node_type_id': '3', 'tcversion_id': '24', 
                         'name': 'TESTCASE_B', 'parent_id': '24', 
                         'node_order': '0', 'node_table': 'testcases', 
                         'external_id': 'NPROAPI-2', 'id': '33'}],
                '25' : [{'node_type_id': '3', 'tcversion_id': '25', 
                         'name': 'TESTCASE_AA', 'parent_id': '25', 
                         'node_order': '0', 'node_table': 'testcases', 
                         'external_id': 'NPROAPI-1',  'id': '26'}]
                 },
              'getTestPlanPlatforms' : {
                '22' : [{'message': 'Test plan (name:TestPlan_API) has no platforms linked', 
                         'code': 3041}]},
              'getBuildsForTestPlan' : {'22' : ''}
              }

class DummyAPIClient(TestlinkAPIClient):
    """ Dummy for Simulation TestLinkAPICLient. 
    Overrides _callServer() Method to return test scenarios
    """
    
    def __init__(self, server_url, devKey):
        super(DummyAPIClient, self).__init__(server_url, devKey)
        self.scenario_data = {}

    def loadScenario(self, a_scenario):
        self.scenario_data = a_scenario

    def _callServer(self, methodAPI, argsAPI=None):
        data = self.scenario_data[methodAPI]
        response = None
        if methodAPI in ['getProjectTestPlans', 
                         'getFirstLevelTestSuitesForTestProject']:
            response = data[argsAPI['testprojectid']]
        elif methodAPI in ['getTestSuitesForTestPlan', 
                           'getTestCasesForTestPlan', 'getTestPlanPlatforms',
                           'getBuildsForTestPlan']:
            response = data[argsAPI['testplanid']]
        elif methodAPI in ['getTestCasesForTestSuite', 
                           'getTestSuitesForTestSuite']:
            response = data[argsAPI['testsuiteid']]
        else:
            response = data
        return response
    
    
class TestLinkAPIOfflineTestCase(unittest.TestCase):
    """ TestCases for TestlinkAPIClient - does not interacts with a TestLink Server.
    works with DummyAPIClientm which returns special test data
    """

    def setUp(self):
        self.api = TestLinkHelper().connect(DummyAPIClient)

#    def tearDown(self):
#        pass


    def test_countProjects(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countProjects()
        self.assertEqual(2, response)
        
    def test_countTestPlans(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countTestPlans()
        self.assertEqual(1, response)
        
    def test_countTestSuites(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countTestSuites()
        self.assertEqual(0, response)
        
    def test_countTestCasesTP(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countTestCasesTP()
        self.assertEqual(0, response)
        
    def test_countTestCasesTS(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countTestCasesTS()
        self.assertEqual(0, response)

    def test_countPlatforms(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countPlatforms()
        self.assertEqual(0, response)
        
    def test_countBuilds(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countBuilds()
        self.assertEqual(0, response)

#    def test_listProjects(self):
#        self.api.loadScenario(SCENARIO_A)
#        self.api.listProjects()
#         no assert check cause method returns nothing
#         'just' prints to stdout
        
    def test_getProjectIDByName(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectIDByName('NEW_PROJECT_API')
        self.assertEqual('21', response)
        response = self.api.getProjectIDByName('UNKNOWN_PROJECT')
        self.assertEqual(-1, response)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()