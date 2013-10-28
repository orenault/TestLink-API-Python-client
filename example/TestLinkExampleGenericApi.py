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


"""

Shows how to use the TestLinkAPIGeneric.
- does equal things as Example TestLinkAPI in TestLinkExample.py

=> Counts and lists the Projects 
=> Create a new Project with the following structure:


NewProject 
   |
   ----NewTestPlan
            |
            ------ Test Suite A
            |           |
            |           ------- Test Suite AA 
            |                          |
            |                          --------- Test Case AA
            |                                      |
            ------ Test Suite B                    --- 5 manual test steps
                          |
                          --------- Test Case B
                                           |   
                                           --- 5 automated test steps
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
tl_helper.setParamsFromArgs('''Shows how to use the TestLinkAPI.
=> Counts and lists the Projects 
=> Create a new Project with the following structure:''')
myTestLink = tl_helper.connect(TestlinkAPIGeneric) 

projNr=len(myTestLink.getProjects())+1

NEWPROJECT="PROJECT_API_GENERIC-%i" % projNr
NEWPREFIX="GPROAPI%i" % projNr
NEWTESTPLAN="TestPlan_API_GENERIC"
NEWTESTSUITE_A="A - First Level"
NEWTESTSUITE_B="B - First Level"
NEWTESTSUITE_AA="AA - Second Level"
NEWTESTCASE_AA="TESTCASE_AA"
NEWTESTCASE_B="TESTCASE_B"
NEWBUILD="Build v0.4.5"

NEWATTACHMENT_PY= os.path.realpath(__file__)
this_file_dirname=os.path.dirname(NEWATTACHMENT_PY)
NEWATTACHMENT_PNG=os.path.join(this_file_dirname, 'PyGreat.png')

# example handling Response Error Codes
# first check an invalid devKey and than the own one
try:
     myTestLink.checkDevKey(devKey='007')
except TLResponseError as tl_err:
    if tl_err.code == 2000:
        # expected invalid devKey Error
        # now check the own one - just call with default settings
        myTestLink.checkDevKey()
    else:
        # seems to be another response failure -  we forward it
        raise   

print "Number of Projects in TestLink: %i " % len(myTestLink.getProjects())
print ""
for project in myTestLink.getProjects():
    print "Name: %(name)s ID: %(id)s " % project
print ""

# # Creates the project
newProject = myTestLink.createTestProject(NEWPROJECT, NEWPREFIX, 
    notes='This is a Project created with the Generic API', active=1, public=1,
    options={'requirementsEnabled' : 1, 'testPriorityEnabled' : 1, 
             'automationEnabled' : 1,  'inventoryEnabled' : 1})
print "createTestProject", newProject
newProjectID = newProject[0]['id'] 
print "New Project '%s' - id: %s" % (NEWPROJECT,newProjectID)
 
# Creates the test plan
newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN, NEWPROJECT,
            notes='New TestPlan created with the Generic API',active=1, public=1)    
print "createTestPlan", newTestPlan
newTestPlanID = newTestPlan[0]['id'] 
print "New Test Plan '%s' - id: %s" % (NEWTESTPLAN,newTestPlanID)
 
#Creates the test Suite A      
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_A,
            "Details of the Test Suite A")  
print "createTestSuite", newTestSuite
newTestSuiteID_A = newTestSuite[0]['id'] 
print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_A, newTestSuiteID_A)
 
FirstLevelID = newTestSuiteID_A
  
#Creates the test Suite B      
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_B,
            "Details of the Test Suite B")               
print "createTestSuite", newTestSuite
newTestSuiteID_B = newTestSuite[0]['id'] 
print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_B, newTestSuiteID_B)
 
#Creates the test Suite AA       
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_AA,
            "Details of the Test Suite AA",parentid=FirstLevelID)               
print "createTestSuite", newTestSuite
newTestSuiteID_AA = newTestSuite[0]['id'] 
print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_AA, newTestSuiteID_AA)
 
MANUAL = 1
AUTOMATED = 2
# 
# #Creates the test case TC_AA
steps_tc_aa = [
        {'step_number' : 1, 'actions' : "Step action 1 - aa" , 
         'expected_results' : "Step result 1 - aa", 'execution_type' : MANUAL},
        {'step_number' : 2, 'actions' : "Step action 2 - aa" , 
         'expected_results' : "Step result 2 - aa", 'execution_type' : MANUAL},
        {'step_number' : 3, 'actions' : "Step action 3 - aa" , 
         'expected_results' : "Step result 3 - aa", 'execution_type' : MANUAL},
        {'step_number' : 4, 'actions' : "Step action 4 - aa" , 
         'expected_results' : "Step result 4 - aa", 'execution_type' : MANUAL},
        {'step_number' : 5, 'actions' : "Step action 5 - aa" , 
         'expected_results' : "Step result 5 - aa", 'execution_type' : MANUAL}
               ]  
newTestCase = myTestLink.createTestCase(NEWTESTCASE_AA, newTestSuiteID_AA, 
          newProjectID, "admin", "This is the summary of the Test Case AA", 
          steps_tc_aa, preconditions='these are the preconditions')                 
print "createTestCase", newTestCase
newTestCaseID_AA = newTestCase[0]['id'] 
print "New Test Case '%s' - id: %s" % (NEWTESTCASE_AA, newTestCaseID_AA)
 
#Creates the test case TC_B 
steps_tc_b = [
        {'step_number' : 1, 'actions' : "Step action 1 -b " , 
         'expected_results' : "Step result 1 - b", 'execution_type' : AUTOMATED},
        {'step_number' : 2, 'actions' : "Step action 2 -b " , 
         'expected_results' : "Step result 2 - b", 'execution_type' : AUTOMATED},
        {'step_number' : 3, 'actions' : "Step action 3 -b " , 
         'expected_results' : "Step result 3 - b", 'execution_type' : AUTOMATED},
        {'step_number' : 4, 'actions' : "Step action 4 -b " , 
         'expected_results' : "Step result 4 - b", 'execution_type' : AUTOMATED},
        {'step_number' : 5, 'actions' : "Step action 5 -b " , 
         'expected_results' : "Step result 5 - b", 'execution_type' : AUTOMATED}]
      
newTestCase = myTestLink.createTestCase(NEWTESTCASE_B, newTestSuiteID_B, 
          newProjectID, "admin", "This is the summary of the Test Case B", 
          steps_tc_b, preconditions='these are the preconditions', 
          executiontype=AUTOMATED)               
print "createTestCase", newTestCase
newTestCaseID_B = newTestCase[0]['id'] 
print "New Test Case '%s' - id: %s" % (NEWTESTCASE_B, newTestCaseID_B)
  
# Add  test cases to test plan - we need the full external id !
tc_aa_full_ext_id = myTestLink.getTestCase(testcaseid=newTestCaseID_AA)[0]['full_tc_external_id']
response = myTestLink._callServer('addTestCaseToTestPlan', 
                {'devKey' : myTestLink.devKey, 
                 'testprojectid' : newProjectID, 
                 'testplanid' : newTestPlanID, 
                 'testcaseexternalid' : tc_aa_full_ext_id, 'version' : 1})
print "addTestCaseToTestPlan", response
tc_b_full_ext_id = myTestLink.getTestCase(testcaseid=newTestCaseID_B)[0]['full_tc_external_id']
response = myTestLink._callServer('addTestCaseToTestPlan', 
                {'devKey' : myTestLink.devKey, 
                 'testprojectid' : newProjectID, 
                 'testplanid' : newTestPlanID, 
                 'testcaseexternalid' : tc_b_full_ext_id, 'version' : 1})
print "addTestCaseToTestPlan", response

# -- Create Build
newBuild = myTestLink.createBuild(newTestPlanID, NEWBUILD, 
                                  buildnotes='Notes for the Build')
print "createBuild", newBuild
newBuildID = newBuild[0]['id'] 
print "New Build '%s' - id: %s" % (NEWBUILD, newBuildID)
  
# report Test Case Results
# TC_AA failed, build should be guessed, TC identified with external id
newResult = myTestLink.reportTCResult(newTestPlanID, 'f', guess=True,
                                      testcaseexternalid=tc_aa_full_ext_id)
print "reportTCResult", newResult
newResultID_AA = newResult[0]['id']
# TC_B passed, explicit build and some notes , TC identified with internal id
newResult = myTestLink.reportTCResult(newTestPlanID, 'p', 
                buildid=newBuildID, testcaseid=newTestCaseID_B, 
                notes="first try")
print "reportTCResult", newResult
newResultID_B = newResult[0]['id']

# add this python file as Attachemnt to last execution of TC_B with 
# different filename 'MyPyExampleApiGeneric.py'
a_file=open(NEWATTACHMENT_PY)
newAttachment = myTestLink.uploadExecutionAttachment(a_file, newResultID_B, 
        title='Textfile Example', description='Text Attachment Example for a TestCase',
        filename='MyPyExampleApiGeneric.py')
print "uploadExecutionAttachment", newAttachment
# add png file as Attachemnt to last execution of TC_AA
# !Attention - on WINDOWS use binary mode for none text file
# see http://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files
a_file=open(NEWATTACHMENT_PNG, mode='rb')
newAttachment = myTestLink.uploadExecutionAttachment(a_file, newResultID_AA, 
            title='PNG Example', description='PNG Attachment Example for a TestCase')
print "uploadExecutionAttachment", newAttachment

# get information - TestProject
response = myTestLink.getTestProjectByName(NEWPROJECT)
print "getTestProjectByName", response
response = myTestLink.getProjectTestPlans(newProjectID)
print "getProjectTestPlans", response
response = myTestLink.getFirstLevelTestSuitesForTestProject(newProjectID)
print "getFirstLevelTestSuitesForTestProject", response

# get information - TestPlan
response = myTestLink.getTestPlanByName(NEWPROJECT, NEWTESTPLAN)
print "getTestPlanByName", response
response = myTestLink.getTotalsForTestPlan(newTestPlanID)
print "getTotalsForTestPlan", response
response = myTestLink.getBuildsForTestPlan(newTestPlanID)
print "getBuildsForTestPlan", response
response = myTestLink.getLatestBuildForTestPlan(newTestPlanID)
print "getLatestBuildForTestPlan", response
response = myTestLink.getTestPlanPlatforms(newTestPlanID)
print "getTestPlanPlatforms", response
response = myTestLink.getTestSuitesForTestPlan(newTestPlanID)
print "getTestSuitesForTestPlan", response
# get failed Testcases 
response = myTestLink.getTestCasesForTestPlan(newTestPlanID, executestatus='f')
print "getTestCasesForTestPlan", response

# get information - TestSuite
response = myTestLink.getTestSuiteByID(newTestSuiteID_B)
print "getTestSuiteByID", response
response = myTestLink.getTestSuitesForTestSuite(newTestSuiteID_A)
print "getTestSuitesForTestSuite", response
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_A,
                                               deep=True, detail='full')
print "getTestCasesForTestSuite", response
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_B,
                                               deep=False, detail='only_id')
print "getTestCasesForTestSuite", response

# get informationen - TestCase_B
response = myTestLink.getTestCaseIDByName(NEWTESTCASE_B, testprojectname=NEWPROJECT)
print "getTestCaseIDByName", response
# get informationen - TestCase_AA via Pathname
tcpathname = '::'.join([NEWPROJECT, NEWTESTSUITE_A, NEWTESTSUITE_AA, NEWTESTCASE_AA])
response = myTestLink.getTestCaseIDByName('unknown', testcasepathname=tcpathname)
print "getTestCaseIDByName", response

# get information - general 
response = myTestLink.getFullPath(int(newTestSuiteID_AA))
print "getFullPath", response
response = myTestLink.getFullPath([int(newTestCaseID_AA), int(newTestCaseID_B)])
print "getFullPath", response

print ""
print "Number of Projects in TestLink: %i " % len(myTestLink.getProjects())
print ""
for project in myTestLink.getProjects():
    print "Name: %(name)s ID: %(id)s " % project
print ""

 
# 
# 
#  
