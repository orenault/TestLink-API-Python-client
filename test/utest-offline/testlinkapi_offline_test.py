#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012-2013 Luiko Czub, TestLink-API-Python-client developers
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
from testlink.testlinkerrors import TLArgError

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
                         'testproject_id': '21', 'id': '22'},
                        {'name': 'TestPlan_NoSuite', 
                         'notes': 'TestPlan with No Suites and No Platforms', 
                         'active': '1', 'is_public': '1', 
                         'testproject_id': '21', 'id': '222'}] ,
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
              'getTestSuitesForTestPlan' : {'22' : '', '222' : ''},
              'getTestCasesForTestPlan' : {'22' : '', '222' : ''},
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
                '22' : [{'notes': '', 'id': '1', 'name': 'dutch'}, {'notes': '', 'id': '2', 'name': 'platt'}],
                '222' : [{'message': 'Test plan (name:TestPlan_API) has no platforms linked', 
                         'code': 3041}]},
              'getBuildsForTestPlan' : {'22' : '', '222' : ''},
              'getTestCaseIDByName' : {
                'dictResult' :  {'1': {'parent_id': '24', 'tc_external_id': '2', 
                                       'id': '33', 'tsuite_name': 'B - First Level', 
                                       'name': 'TESTCASE_B'}}, 
                'listResult' : [{'parent_id': '25', 'tc_external_id': '1', 
                                 'id': '26', 'tsuite_name': 'AA - Second Level', 
                                 'name': 'TESTCASE_AA'}]},
              'getTestCase' : {
                '26' : [{'full_tc_external_id': 'NPROAPI-1-26', 'node_order': '0', 'is_open': '1', 'id': '26', 
                         'author_last_name': 'LkaTlinkD7', 'updater_login': '', 'layout': '1', 'tc_external_id': '1', 
                         'version': '1', 'estimated_exec_duration': '', 'testsuite_id': '25', 'updater_id': '', 
                         'status': '1', 'updater_first_name': '', 'testcase_id': '5099', 'author_first_name': 'Tester', 
                         'importance': '2', 'modification_ts': '', 'execution_type': '1', 'preconditions': '', 
                         'active': '1', 'creation_ts': '2013-12-26 21:17:43', 'name': 'TC-C', 'summary': 'SumSumSum', 
                         'updater_last_name': '', 
                         'steps': [{'step_number': '1', 'actions': 'Step action 1', 'execution_type': '2', 'active': '1', 
                                    'id': '5101', 'expected_results': 'Step result 1'}], 
                         'author_id': '3', 'author_login': 'tester'}]
                               },
              'getFullPath' : {
                               
                26 : {'26' : ['TestPlan_API', 'A - First Level', 'AA - Second Level']},
                    },
              'getTestProjectByName' : {
                'TestPlan_API' : {
                    'opt': {'requirementsEnabled': 0, 'testPriorityEnabled': 1, 
                            'automationEnabled': 1, 'inventoryEnabled': 0}, 
                    'prefix': 'NPROAPI', 'name': 'NEW_PROJECT_API', 'color': '',
                    'notes': 'This is a Project created with the API', 
                    'option_priority': '0', 
                    'options': 'O:8:"stdClass":4:{s:19:"requirementsEnabled";i:0;s:19:"testPriorityEnabled";i:1;s:17:"automationEnabled";i:1;s:16:"inventoryEnabled";i:0;}', 
                    'tc_counter': '2', 'option_reqs': '0', 'active': '1', 
                    'is_public': '1', 'id': '21', 'option_automation': '0'},
                    },
              'createTestCase' : 'dummy response createTestCase',
              }

SCENARIO_STEPS = {'createTestCase' : ['noRealReponseData - ok for step tests']}

class DummyAPIClient(TestlinkAPIClient):
    """ Dummy for Simulation TestLinkAPICLient. 
    Overrides _callServer() Method to return test scenarios
    """

    __slots__ = ['scenario_data', 'callArgs']
    
    def __init__(self, server_url, devKey):
        super(DummyAPIClient, self).__init__(server_url, devKey)
        self.scenario_data = {}
        self.callArgs = None

    def loadScenario(self, a_scenario):
        self.scenario_data = a_scenario

    def _callServer(self, methodAPI, argsAPI=None):
        self.callArgs = argsAPI
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
        elif methodAPI in ['getTestCaseIDByName']:
            response = data[argsAPI['testcasename']]
        elif methodAPI in ['getTestCase']:
            response = data[argsAPI['testcaseid']]
        elif methodAPI in ['getFullPath']:
            response = data[argsAPI['nodeid']]
        elif methodAPI in ['getTestProjectByName']:
            response = data[argsAPI['testprojectname']]
        else:
            response = data
        return response
    
    
class TestLinkAPIOfflineTestCase(unittest.TestCase):
    """ TestCases for TestlinkAPIClient - does not interacts with a TestLink Server.
    works with DummyAPIClientm which returns special test data
    """

    example_steps = [{'step_number' : '1', 'actions' : "action A" , 
                'expected_results' : "result A", 'execution_type' : "0"},
                 {'step_number' : '2', 'actions' : "action B" , 
                'expected_results' : "result B", 'execution_type' : "1"},
                 {'step_number' : '3', 'actions' : "action C" , 
                'expected_results' : "result C", 'execution_type' : "0"}]
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
        self.assertEqual(2, response)
        
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
        self.assertEqual(2, response)
        
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
        
    def test_initStep(self):
        self.api.initStep("action A", "result A", 0)
        steps = self.example_steps[:1]
        self.assertEqual(steps, self.api.stepsList)
        
    def test_appendStep(self):
        steps = self.example_steps
        self.api.stepsList = steps[:1] 
        self.api.appendStep("action B", "result B", 1)
        self.api.appendStep("action C", "result C", 0)
        self.assertEqual(steps, self.api.stepsList)

    def test_createTestCaseWithSteps(self):
        self.api.loadScenario(SCENARIO_STEPS)
        self.api.initStep("action A", "result A", 0)
        self.api.appendStep("action B", "result B", 1)
        self.api.appendStep("action C", "result C", 0)
        self.api.createTestCase('case 4711', 4712, 4713, 'Big Bird', 
                                'summary 4714')
        self.assertEqual(self.example_steps, self.api.callArgs['steps'])
        self.assertEqual([], self.api.stepsList)

    def test_createTestCaseWithConfusingSteps(self):
        self.api.loadScenario(SCENARIO_STEPS)
        self.api.initStep("action A", "result A", 0)
        self.api.appendStep("action B", "result B", 1)
        self.api.appendStep("action C", "result C", 0)
        with self.assertRaisesRegexp(TLArgError, 'confusing createTestCase*'):
            self.api.createTestCase('case 4711', 4712, 4713, 'Big Bird', 
                                    'summary 4714', steps=[])
        
    def test_getTestCaseIDByName_dictResult(self):
        "test that getTestCaseIDByName converts dictionary result into a list"
        self.api.loadScenario(SCENARIO_A)
        # v0.4.0 version for optional args testsuitename + testprojectname
        #response = self.api.getTestCaseIDByName('dictResult', None, 'NEW_PROJECT_API')
        # v0.4.5 version
        response = self.api.getTestCaseIDByName('dictResult', 
                                            testprojectname='NEW_PROJECT_API')
        self.assertEqual(list, type(response))
        self.assertEqual('TESTCASE_B', response[0]['name']) 
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestCaseIDByName_listResult(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCaseIDByName('listResult')
        self.assertEqual(list, type(response))
        self.assertEqual('TESTCASE_AA', response[0]['name']) 
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test__copyTC_generate_new(self):
        self.api.loadScenario(SCENARIO_A)
        self.api._copyTC('26', 'generate_new', {})
        self.assertEqual('generate_new',  
                         self.api.callArgs['actiononduplicatedname'])

    def test__copyTC_create_new_version(self):
        self.api.loadScenario(SCENARIO_A)
        self.api._copyTC('26', 'create_new_version', {})
        self.assertEqual('create_new_version',  
                         self.api.callArgs['actiononduplicatedname'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()