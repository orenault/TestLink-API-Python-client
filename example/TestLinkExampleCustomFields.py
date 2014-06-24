#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2013-2014 Luiko Czub, TestLink-API-Python-client developers
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


"""

Shows how to use the TestLinkAPI for custom fields
Cause the TL api itselfs allows only to request the value of custom fields
- no creation or assignment of custom fields is possible
this example requires a special existing project with special custom fields 
assigned

a) run example TestLinkExampleGenericApi.py
   - this creates a project like PROJECT_API_GENERIC-7
   if some additional project are created since running that example, adapt 
   variable projNr in this script your are reading currently 
b) load custom field definitions customFields_ExampleDefs.xml
   TL - Desktop - System - Define Custom Fields - Import
c) assign custom fields to project PROJECT_API_GENERIC-7
   TL - Test Project - Assign Custom Fields
   
   cf_tc_* -> Test Case
   
"""                                       
from testlink import TestlinkAPIGeneric, TestLinkHelper
from testlink.testlinkerrors import TLResponseError
import sys, os.path

# precondition a)
# SERVER_URL and KEY are defined in environment
# TESTLINK_API_PYTHON_SERVER_URL=http://YOURSERVER/testlink/lib/api/xmlrpc.php
# TESTLINK_API_PYTHON_DEVKEY=7ec252ab966ce88fd92c25d08635672b
# 
# alternative precondition b)
# SERVEUR_URL and KEY are defined as command line arguments
# python TestLinkExample.py --server_url http://YOURSERVER/testlink/lib/api/xmlrpc.php
#                           --devKey 7ec252ab966ce88fd92c25d08635672b
#
# ATTENTION: With TestLink 1.9.7, cause of the new REST API, the SERVER_URL 
#            has changed from 
#               (old) http://YOURSERVER/testlink/lib/api/xmlrpc.php
#            to
#               (new) http://YOURSERVER/testlink/lib/api/xmlrpc/v1/xmlrpc.php
tl_helper = TestLinkHelper()
tl_helper.setParamsFromArgs('''Shows how to use the TestLinkAPI for CustomFields.
=> requires an existing project PROJECT_API_GENERIC-*''')
myTestLink = tl_helper.connect(TestlinkAPIGeneric) 

#projNr=len(myTestLink.getProjects())+1
projNr=len(myTestLink.getProjects())

NEWPROJECT="PROJECT_API_GENERIC-%i" % projNr
NEWPREFIX="GPROAPI%i" % projNr
NEWTESTPLAN_A="TestPlan_API_GENERIC A"
NEWTESTPLAN_B="TestPlan_API_GENERIC B"
NEWPLATFORM_A='Big Bird %i' % projNr
NEWPLATFORM_B='Small Bird'
NEWPLATFORM_C='Ugly Bird'
NEWTESTSUITE_A="A - First Level"
NEWTESTSUITE_B="B - First Level"
NEWTESTSUITE_AA="AA - Second Level"
NEWTESTCASE_AA="TESTCASE_AA"
NEWTESTCASE_B="TESTCASE_B"
myApiVersion='%s v%s' % (myTestLink.__class__.__name__ , myTestLink.__version__)
NEWBUILD_A='%s' % myApiVersion
NEWBUILD_B='%s' % myApiVersion

NEWATTACHMENT_PY= os.path.realpath(__file__)
this_file_dirname=os.path.dirname(NEWATTACHMENT_PY)
NEWATTACHMENT_PNG=os.path.join(this_file_dirname, 'PyGreat.png')

# Servers TestLink Version
myTLVersion = myTestLink.testLinkVersion()

# used connection settings
print myTestLink.connectionInfo()
print ""

# get information - TestProject
newProject = myTestLink.getTestProjectByName(NEWPROJECT)
print "getTestProjectByName", newProject
newProjectID = newProject['id'] 
print "Project '%s' - id: %s" % (NEWPROJECT,newProjectID)

# get information - TestPlan
newTestPlan = myTestLink.getTestPlanByName(NEWPROJECT, NEWTESTPLAN_A)
print "getTestPlanByName", newTestPlan
newTestPlanID_A = newTestPlan[0]['id'] 
print "Test Plan '%s' - id: %s" % (NEWTESTPLAN_A,newTestPlanID_A)
response = myTestLink.getTotalsForTestPlan(newTestPlanID_A)
print "getTotalsForTestPlan", response
response = myTestLink.getBuildsForTestPlan(newTestPlanID_A)
print "getBuildsForTestPlan", response
newBuildID_A = response[0]['id']
# get information - TestSuite
response = myTestLink.getTestSuitesForTestPlan(newTestPlanID_A)
print "getTestSuitesForTestPlan", response
newTestSuiteID_A=response[0]['id']
newTestSuiteID_AA=response[1]['id']
newTestSuiteID_B=response[2]['id']
newTestSuite = myTestLink.getTestSuiteByID(newTestSuiteID_B)
print "getTestSuiteByID", newTestSuite

response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_B,
                                               deep=True, detail='full')
print "getTestCasesForTestSuite", response

# get informationen - TestCase_B
response = myTestLink.getTestCaseIDByName(NEWTESTCASE_B, testprojectname=NEWPROJECT)
print "getTestCaseIDByName", response
newTestCaseID_B = response[0]['id'] 
print "Test Case '%s' - id: %s" % (NEWTESTCASE_B, newTestCaseID_B)
newTestCase_B = myTestLink.getTestCase(testcaseid=newTestCaseID_B)[0]
print "getTestCase", newTestCase_B


# new execution result with custom field data
# TC_B passed, explicit build and some notes , TC identified with internal id
newResult = myTestLink.reportTCResult(newTestPlanID_A, 'p', 
                buildid=newBuildID_A, testcaseid=newTestCaseID_B, 
                platformname=NEWPLATFORM_B, notes="custom try",
                customfields={'cf_tc_ex_string' : 'a custom exec value set via api',
                              'cf_tc_sd_listen' : 'ernie'})
print "reportTCResult", newResult

# get execution results
lastResult = myTestLink.getLastExecutionResult(
                        newTestPlanID_A, testcaseid=newTestCaseID_B)[0]
print "getLastExecutionResult", lastResult

# get CustomField Value - TestCase Execution
# response = myTestLink._callServer('getTestCaseCustomFieldExecutionValue', 
#                                   {'devKey' : myTestLink.devKey,
#                                    'customfieldname' : 'cf_tc_ex_string',
#                                    'testprojectid' : newProjectID,
#                                    'version' : lastResult['tcversion_id'],
#                                    'executionid' : lastResult['id'] ,
#                                    'testplanid': lastResult['testplan_id']
#                                    })
response = myTestLink.getTestCaseCustomFieldExecutionValue(
                    'cf_tc_ex_string', newProjectID, lastResult['tcversion_id'],
                     lastResult['id'] , lastResult['testplan_id'] )
print "getTestCaseCustomFieldExecutionValue", response

# update CustomField Value - TestCase SpecDesign
# response = myTestLink._callServer('updateTestCaseCustomFieldDesignValue', 
#                  {'devKey' : myTestLink.devKey,
#                   'testcaseexternalid' : newTestCase_B['full_tc_external_id'],
#                   'version' : int(newTestCase_B['version']),
#                   'testprojectid' : newProjectID,
#                  'customfields' : 
#                  {'cf_tc_sd_string' : 'A custom SpecDesign value set via api',
#                   'cf_tc_sd_list' : 'bibo'}})
response = myTestLink.updateTestCaseCustomFieldDesignValue( 
                 newTestCase_B['full_tc_external_id'],
                 int(newTestCase_B['version']), newProjectID,
                 {'cf_tc_sd_string' : 'A custom SpecDesign value set via api',
                  'cf_tc_sd_list' : 'bibo'})
print "updateTestCaseCustomFieldDesignValue", response

# get CustomField Value - TestCase SpecDesign
args =  {'devKey' : myTestLink.devKey,
                     'testprojectid' : newProjectID,
                     'testcaseexternalid' : newTestCase_B['full_tc_external_id'],
                     'version' : int(newTestCase_B['version'])
                     }
#response = myTestLink._callServer('getTestCaseCustomFieldDesignValue', args)
response = myTestLink.getTestCaseCustomFieldDesignValue( 
                            args['testcaseexternalid'], args['version'],
                            args['testprojectid'], 'cf_tc_sd_string', 
                            details = 'full')
print "getTestCaseCustomFieldDesignValue full", response

response = myTestLink.getTestCaseCustomFieldDesignValue( 
                            args['testcaseexternalid'], args['version'],
                            args['testprojectid'], 'cf_tc_sd_string', 
                            details = 'value')
print "getTestCaseCustomFieldDesignValue value", response

response = myTestLink.getTestCaseCustomFieldDesignValue( 
                            args['testcaseexternalid'], args['version'],
                            args['testprojectid'], 'cf_tc_sd_list', 
                            details = 'simple')
print "getTestCaseCustomFieldDesignValue simple", response

# get CustomField Value - TestCase Testplan Design
response = myTestLink._callServer('getTestCaseCustomFieldTestPlanDesignValue', 
                                  {'devKey' : myTestLink.devKey,
                                   'customfieldname' : 'cf_tc_pd_string',
                                   'testprojectid' : newProjectID,
                                   'version' : lastResult['tcversion_id'],
                                   'testplanid': lastResult['testplan_id'],
                                   'linkid' : 779})
print "getTestCaseCustomFieldTestPlanDesignValue", response

# get CustomField Value - TestSuite
response = myTestLink._callServer('getTestSuiteCustomFieldDesignValue', 
                                  {'devKey' : myTestLink.devKey,
                                   'customfieldname' : 'cf_ts_string',
                                   'testprojectid' : newProjectID,
                                   'testsuiteid': newTestSuiteID_B})
print "getTestSuiteCustomFieldDesignValue", response

# get CustomField Value - TestPlan
response = myTestLink._callServer('getTestPlanCustomFieldDesignValue', 
                                  {'devKey' : myTestLink.devKey,
                                   'customfieldname' : 'cf_tp_string',
                                   'testprojectid' : newProjectID,
                                   'testplanid': lastResult['testplan_id']})
print "getTestPlanCustomFieldDesignValue", response

