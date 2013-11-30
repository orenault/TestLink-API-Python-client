#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2013 Luiko Czub, TestLink-API-Python-client developers
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
from testlink import TestlinkAPIGeneric, TestLinkHelper
from testlink.testlinkerrors import TLArgError, TLResponseError

#from testlink.testlinkapigeneric import positionalArgNamesDefault
# scenario_a includes response from a testlink 1.9.8 server
SCENARIO_A = {'repeat' : 'You said: One World',
              'sayHello' : 'Hey Folks!',
              'doesUserExist' : {
                'Big Bird' :  [{'message': '(doesUserExist) - Cannot Find User Login provided (Big Bird).', 
                                'code': 10000}],
                'admin' : True },
              'getProjectTestPlans' : {
                'onePlan' : [{'name': 'TestPlan_API', 
                         'notes': 'New TestPlan created with the API', 
                         'active': '1', 'is_public': '1', 
                         'testproject_id': '21', 'id': '22'}] ,
                'noPlan' : '' },
              'getBuildsForTestPlan' : {'noBuild' : '' },
              'getTestPlanPlatforms' : {
                'twoPlatforms' : [{'notes': '', 'id': '1', 'name': 'dutch'}, 
                                  {'notes': '', 'id': '2', 'name': 'platt'}],
                'noPlatform' : [{'message': 'Test plan (noPlatform) has no platforms linked', 
                         'code': 3041}]},
              'getTestSuitesForTestPlan' : {'noSuite' : ''},
              'getTestSuitesForTestSuite' : {'noSuite' : ''},
              'getFirstLevelTestSuitesForTestProject' : {
                'noSuite' : [{'message': 'Test Project (noSuite) is empty.', 
                              'code': 7008}]},
              'getTestCasesForTestSuite' : {'noTestCase' : [] },
              'getTestCasesForTestPlan'  : {'noTestCase' : [] },
              'getTestCaseIDByName' : {
                'dictResult' :  {'1': {'parent_id': '24', 'tc_external_id': '2', 
                                       'id': '33', 'tsuite_name': 'B - First Level', 
                                       'name': 'TESTCASE_B'}}, 
                'listResult' : [{'parent_id': '25', 'tc_external_id': '1', 
                                 'id': '26', 'tsuite_name': 'AA - Second Level', 
                                 'name': 'TESTCASE_AA'}]},
              'getProjectPlatforms' : {
                   'twoPlatforms' : {'dutch' : {'id': '1', 'name': 'dutch'}, 
                                     'platt' : {'id': '2', 'name': 'platt'}},
                    'noPlatform'  : {}   
                    }
              }

class DummyAPIGeneric(TestlinkAPIGeneric):
    """ Dummy for Simulation TestLinkAPIGeneric. 
    Overrides 
    - _callServer() Method to return test scenarios
    - extend positional_arg_names for  method 'DummyMethod'
    """

    __slots__ = ['scenario_data', 'callArgs']
  
    def __init__(self, server_url, devKey):
        super(DummyAPIGeneric, self).__init__(server_url, devKey)
        self._positionalArgNames['DummyMethod'] = ['Uno', 'due', 'tre']
        self.scenario_data = {}
        self.callArgs = None


    def loadScenario(self, a_scenario):
        self.scenario_data = a_scenario

    def _callServer(self, methodAPI, argsAPI=None):
        self.callArgs = argsAPI
        response = None
        if methodAPI in ['DummyMethod']:
            response = [argsAPI]
        else:
            data = self.scenario_data[methodAPI]
            if methodAPI in ['doesUserExist']:
                response = data[argsAPI['user']]
            elif methodAPI in ['getProjectTestPlans', 'getProjectPlatforms',
                               'getFirstLevelTestSuitesForTestProject']:
                response = data[argsAPI['testprojectid']]
            elif methodAPI in ['getBuildsForTestPlan', 'getTestPlanPlatforms', 
                        'getTestSuitesForTestPlan', 'getTestCasesForTestPlan']:
                response = data[argsAPI['testplanid']]
            elif methodAPI in ['getTestSuitesForTestSuite', 
                               'getTestCasesForTestSuite']:
                response = data[argsAPI['testsuiteid']]
            elif methodAPI in ['getTestCaseIDByName']:
                response = data[argsAPI['testcasename']]
            else:
                response = data
        return response
    
    
class TestLinkAPIGenericOfflineTestCase(unittest.TestCase):
    """ TestCases for TestlinkAPIGeneric - does not interacts with a TestLink Server.
    works with DummyAPIGeneric which returns special test data
    """

    def setUp(self):
        self.api = TestLinkHelper().connect(DummyAPIGeneric)
        self.callArgs = None
        
#    def tearDown(self):
#        pass


    def test_convertPositionalArgs(self):
        response = self.api._convertPostionalArgs('DummyMethod',  [1,2,3])
        self.assertEqual({'Uno' : 1, 'due' :2, 'tre' : 3}, response)
        
    def test__convertPositionalArgs_missingConf(self):
        client = self.api
        def a_func(a_api): a_api._convertPostionalArgs('NoConfigMethod',  [1,2])
        self.assertRaises(TLArgError, a_func, client)
        
    def test__convertPositionalArgs_lessValues(self):
        client = self.api
        def a_func(a_api): a_api._convertPostionalArgs('DummyMethod',  [1,2])
        self.assertRaises(TLArgError, a_func, client)
        
    def test__convertPositionalArgs_moreValues(self):
        client = self.api
        def a_func(a_api): a_api._convertPostionalArgs('DummyMethod',  [1,2,3,4])
        self.assertRaises(TLArgError, a_func, client)

    def test_callServerWithPosArgs_pos(self):
        self.api.callServerWithPosArgs('DummyMethod',  1,2,3)
        self.assertEqual({'Uno' : 1, 'due' :2, 'tre' : 3}, self.api.callArgs)

    def test_callServerWithPosArgs_pos_opt(self):
        self.api.callServerWithPosArgs('DummyMethod',  1,2,3, quad=4)
        self.assertEqual({'Uno' : 1, 'due' :2, 'tre' : 3, 'quad' : 4}, self.api.callArgs)

    def test_callServerWithPosArgs_opt(self):
        self.api.callServerWithPosArgs('DummyMethod',  quad=4)
        self.assertEqual({'quad' : 4}, self.api.callArgs)

    def test_callServerWithPosArgs_none(self):
        self.api.callServerWithPosArgs('DummyMethod')
        self.assertEqual({}, self.api.callArgs)
        
    def test_checkResponse_emptyResponse(self):
        client = self.api
        def a_func(a_api, response): 
            a_api._checkResponse(response, 'DummyMethod',  
                                 {'Uno' : 1, 'due' :2, 'tre' : 3})
        self.assertRaises(TLResponseError, a_func, client, '')
        self.assertRaises(TLResponseError, a_func, client, [])
        
    def test_checkResponse_errorResponse(self):
        client = self.api
        responseA = [{'message': '(reportTCResult) - TC ID 709 does not exist!', 
                      'code': 5000}]
        def a_func(a_api, response): 
            a_api._checkResponse(response, 'DummyMethod',  
                                 {'Uno' : 1, 'due' :2, 'tre' : 3})
        self.assertRaises(TLResponseError, a_func, client, responseA)

    def test_checkResponse_okResponse(self):
        self.api._checkResponse(
                        [{'message': 'all fine, cause no key with name code'}],
                         'DummyMethod', {'Uno' : 1, 'due' :2, 'tre' : 3})
        self.api._checkResponse(
                        'some API Call juts returns one string without codes',
                         'DummyMethod', {'Uno' : 1, 'due' :2, 'tre' : 3})
        
    def test_checkResponse_booleanResponse(self):
        response = True
        self.api._checkResponse(response, 'DummyMethod', 
                                {'Uno' : 1, 'due' :2, 'tre' : 3})
        
    def test_checkResponse_dictionaryResponse(self):
        response = {'note' : 'uploadAttachment Calls return {..} and not [{..}]'}
        self.api._checkResponse(response, 'DummyMethod', 
                                {'Uno' : 1, 'due' :2, 'tre' : 3})
        
    def test_whatArgs_noArgs(self):
        response = self.api.whatArgs('sayHello')
        self.assertRegexpMatches(response, 'sayHello().*')
        
    def test_whatArgs_onlyOptionalArgs(self):
        response = self.api.whatArgs('getTestCaseAttachments')
        self.assertRegexpMatches(response, 'getTestCaseAttachments\(\[.*=<.*>\].*\).*')
        
    def test_whatArgs_OptionalAndPositionalArgs(self):
        response = self.api.whatArgs('createBuild')
        self.assertRegexpMatches(response, 'createBuild\(<.*>.*\).*')

    def test_whatArgs_MandatoryArgs(self):
        response = self.api.whatArgs('uploadExecutionAttachment')
        self.assertRegexpMatches(response, 
                    'uploadExecutionAttachment\(<attachmentfile>, <.*>.*\).*')

    def test_whatArgs_unknownMethods(self):
        response = self.api.whatArgs('apiUnknown')
        self.assertRegexpMatches(response, 
                "callServerWithPosArgs\('apiUnknown', \[apiArg=<apiArg>\]\)")
        
    def test_noWrapperName_apiMethods(self):
        " decorator test: API Methods internal function name should be unchanged "
        
        # apiMethod with decorator @decoApiCallWithoutArgs
        self.assertEqual('sayHello', self.api.sayHello.__name__)
        # apiMethod with decorator @decoApiCallWithArgs
        self.assertEqual('repeat', self.api.repeat.__name__)
        # apiMethod with decorator @decoApiCallAddDevKey 
        self.assertEqual('createBuild', self.api.createBuild.__name__)
        # apiMethod with decorator @decoMakerApiCallReplaceTLResponseError()
        self.assertEqual('getProjectTestPlans', self.api.getProjectTestPlans.__name__)
        # apiMethod with decorator @decoApiCallAddAttachment
        self.assertEqual('uploadExecutionAttachment', self.api.uploadExecutionAttachment.__name__)
        
    def test_ping(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.ping()
        self.assertEqual('Hey Folks!', response)
        
        
    def test_getProjectTestPlans_noPlan(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectTestPlans('noPlan')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getProjectTestPlans_onePlan(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectTestPlans('onePlan')
        self.assertEqual('21', response[0]['testproject_id'])
        self.assertEqual(1, len(response))
        
    def test_getProjectPlatforms_noPlatform(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectPlatforms('noPlatform')
        self.assertEqual({}, response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getProjectPlatforms_twoPlatforms(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectPlatforms('twoPlatforms')
        self.assertEqual('1', response['dutch']['id'])
        self.assertEqual(2, len(response))
        
        
    def test_getBuildsForTestPlan_noBuild(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getBuildsForTestPlan('noBuild')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestPlanPlatforms_noPlatform(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestPlanPlatforms('noPlatform')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestPlanPlatforms_twoPlatforms(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestPlanPlatforms('twoPlatforms')
        self.assertEqual('dutch', response[0]['name'])
        self.assertEqual(2, len(response))

    def test_getTestSuitesForTestPlan_noSuite(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestSuitesForTestPlan('noSuite')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
       
    def test_getTestSuitesForTestSuite_noSuite(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestSuitesForTestSuite('noSuite')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getFirstLevelTestSuitesForTestProject_noSuite(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getFirstLevelTestSuitesForTestProject('noSuite')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestCasesForTestSuite_noTestCase(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCasesForTestSuite('noTestCase')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
           
    def test_getTestCasesForTestPlan_noTestCase(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCasesForTestPlan('noTestCase')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestCaseIDByName_dictResult(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCaseIDByName('dictResult', 
                                            testprojectname='NEW_PROJECT_API')
        self.assertEqual(dict, type(response))
        self.assertEqual('TESTCASE_B', response['1']['name']) 
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestCaseIDByName_listResult(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCaseIDByName('listResult')
        self.assertEqual(list, type(response))
        self.assertEqual('TESTCASE_AA', response[0]['name']) 
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()