#! /usr/bin/python
# -*- coding: UTF-8 -*-
from compiler.pycodegen import TRY_FINALLY
from symbol import except_clause

#  Copyright 2011-2013 Olivier Renault, TestLink-API-Python-client developers
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

TestLinkExample - v0.20
Created on 6 nov. 2011
@author: Olivier Renault (admin@sqaopen.net)

Shows how to use the TestLinkAPI.

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
                                           
Update Oct. 2013, L. Czub
Integrates v0.4.5 changes for  optional arguments and response error handling
The v0.4.0 method calls are still visible as comments (look for CHANGE v0.4.5)
So this file helps to understand where existing own code needs adjustment.
-  
used as behaviour is still                                             
"""                                       
from testlink import TestlinkAPIClient, TestLinkHelper
from testlink.testlinkerrors import TLResponseError
import sys

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
myTestLink = tl_helper.connect(TestlinkAPIClient) 

projNr=len(myTestLink.getProjects())+1

NEWPROJECT="NEW_PROJECT_API-%i" % projNr
NEWPREFIX="NPROAPI%i" % projNr
NEWTESTPLAN="TestPlan_API"
NEWTESTSUITE_A="A - First Level"
NEWTESTSUITE_B="B - First Level"
NEWTESTSUITE_AA="AA - Second Level"
NEWTESTCASE_AA="TESTCASE_AA"
NEWTESTCASE_B="TESTCASE_B"
NEWBUILD="Build v0.4.5"

# -- Start CHANGE v0.4.5 -- 
# if myTestLink.checkDevKey() != True:
#     print "Error with the devKey."      
#     sys.exit(-1)
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
        # seems to be another response failure - we forward it 
        raise   
# -- END CHANGE v0.4.5 -- 
            

print "Number of Projects in TestLink: %s " % (myTestLink.countProjects(),)
print ""
myTestLink.listProjects()
print ""

# Creates the project

# -- Start CHANGE v0.4.5 -- 
# newProject = myTestLink.createTestProject(NEWPROJECT, "NPROAPI",
# "notes=This is a Project created with the API", "active=1", "public=1",
# "options=requirementsEnabled:0,testPriorityEnabled:1,automationEnabled:1,inventoryEnabled:0")
# isOk = newProject[0]['message']
# if isOk=="Success!":
#   newProjectID = newProject[0]['id'] 
#   print "New Project '%s' - id: %s" % (NEWPROJECT,newProjectID)
# else:
#   print "Error creating the project '%s': %s " % (NEWPROJECT,isOk)
#   sys.exit(-1)
newProject = myTestLink.createTestProject(NEWPROJECT, NEWPREFIX,
    notes='This is a Project created with the API', active=1, public=1,
    options={'requirementsEnabled' : 0, 'testPriorityEnabled' : 1,
             'automationEnabled' : 1, 'inventoryEnabled' : 0})
newProjectID = newProject[0]['id']
print "New Project '%s' - id: %s" % (NEWPROJECT,newProjectID)
# -- END CHANGE v0.4.5 -- 

# Creates the test plan
# -- Start CHANGE v0.4.5 -- 
# newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN, NEWPROJECT,
#             "notes=New TestPlan created with the API","active=1", "public=1")    
# isOk = newTestPlan[0]['message']
# if isOk=="Success!":
#   newTestPlanID = newTestPlan[0]['id'] 
#   print "New Test Plan '%s' - id: %s" % (NEWTESTPLAN,newTestPlanID)
# else:
#   print "Error creating the Test Plan '%s': %s " % (NEWTESTPLAN, isOk)
#   sys.exit(-1)
newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN, NEWPROJECT,
            notes='New TestPlan created with the API',active=1, public=1)    
newTestPlanID = newTestPlan[0]['id']
print "New Test Plan '%s' - id: %s" % (NEWTESTPLAN,newTestPlanID)
# -- END CHANGE v0.4.5 -- 

#Creates the test Suite A      
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_A,
            "Details of the Test Suite A")  
# -- Start CHANGE v0.4.5 -- 
# isOk = newTestSuite[0]['message']
# if isOk=="ok":
#   newTestSuiteID = newTestSuite[0]['id'] 
#   print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_A, newTestSuiteID)
# else:
#   print "Error creating the Test Suite '%s': %s " % (NEWTESTSUITE_A, isOk)
#   sys.exit(-1)
newTestSuiteID = newTestSuite[0]['id']
print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_A, newTestSuiteID)
# -- END CHANGE v0.4.5 -- 

FirstLevelID = newTestSuiteID 
 
#Creates the test Suite B      
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_B,
            "Details of the Test Suite B")               
# -- Start CHANGE v0.4.5 -- 
# isOk = newTestSuite[0]['message']
# if isOk=="ok":
#   TestSuiteID_B = newTestSuite[0]['id'] 
#   print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_B, TestSuiteID_B)
# else:
#   print "Error creating the Test Suite '%s': %s " % (NEWTESTSUITE_B, isOk)
#   sys.exit(-1)
TestSuiteID_B = newTestSuite[0]['id']
print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_B, TestSuiteID_B)
# -- END CHANGE v0.4.5 -- 

#Creates the test Suite AA       
# -- Start CHANGE v0.4.5 -- 
# newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_AA,
#             "Details of the Test Suite AA","parentid="+FirstLevelID)               
# isOk = newTestSuite[0]['message']
# if isOk=="ok":
#   TestSuiteID_AA = newTestSuite[0]['id'] 
#   print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_AA, TestSuiteID_AA)
# else:
#   print "Error creating the Test Suite '%s': %s " % (NEWTESTSUITE_AA, isOk)
#   sys.exit(-1)
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_AA,
            "Details of the Test Suite AA",parentid=FirstLevelID)               
TestSuiteID_AA = newTestSuite[0]['id']
print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_AA, TestSuiteID_AA)
# -- END CHANGE v0.4.5 -- 

MANUAL = 1
AUTOMATED = 2

#Creates the test case TC_AA  
myTestLink.initStep("Step action 1", "Step result 1", MANUAL)
myTestLink.appendStep("Step action 2", "Step result 2", MANUAL)
myTestLink.appendStep("Step action 3", "Step result 3", MANUAL)
myTestLink.appendStep("Step action 4", "Step result 4", MANUAL)
myTestLink.appendStep("Step action 5", "Step result 5", MANUAL)
     
# -- Start CHANGE v0.4.5 -- 
# newTestCase = myTestLink.createTestCase(NEWTESTCASE_AA, TestSuiteID_AA, 
#           newProjectID, "admin", "This is the summary of the Test Case AA", 
#           "preconditions=these are the preconditions")                 
# isOk = newTestCase[0]['message']
# if isOk=="Success!":
#   newTestCaseID_AA = newTestCase[0]['id'] 
#   print "New Test Case '%s' - id: %s" % (NEWTESTCASE_AA, newTestCaseID_AA)
# else:
#   print "Error creating the Test Case '%s': %s " % (NEWTESTCASE_AA, isOk)
#   sys.exit(-1)
newTestCase = myTestLink.createTestCase(NEWTESTCASE_AA, TestSuiteID_AA, 
          newProjectID, "admin", "This is the summary of the Test Case AA", 
          preconditions='these are the preconditions')
newTestCaseID_AA = newTestCase[0]['id']
print "New Test Case '%s' - id: %s" % (NEWTESTCASE_AA, newTestCaseID_AA)              
# -- END CHANGE v0.4.5 -- 

#Creates the test case TC_B  
myTestLink.initStep("Step action 1", "Step result 1", AUTOMATED)
myTestLink.appendStep("Step action 2", "Step result 2", AUTOMATED)
myTestLink.appendStep("Step action 3", "Step result 3", AUTOMATED)
myTestLink.appendStep("Step action 4", "Step result 4", AUTOMATED)
myTestLink.appendStep("Step action 5", "Step result 5", AUTOMATED)
     
# -- Start CHANGE v0.4.5 -- 
# newTestCase = myTestLink.createTestCase(NEWTESTCASE_B, TestSuiteID_B, 
#           newProjectID, "admin", "This is the summary of the Test Case B", 
#           "preconditions=these are the preconditions", 
#           "executiontype=%i" % AUTOMATED)               
# isOk = newTestCase[0]['message']
# if isOk=="Success!":
#   newTestCaseID_B = newTestCase[0]['id'] 
#   print "New Test Case '%s' - id: %s" % (NEWTESTCASE_B, newTestCaseID_B)
# else:
#   print "Error creating the Test Case '%s': %s " % (NEWTESTCASE_B, isOk)
#   sys.exit(-1)
newTestCase = myTestLink.createTestCase(NEWTESTCASE_B, TestSuiteID_B, 
          newProjectID, "admin", "This is the summary of the Test Case B", 
          preconditions='these are the preconditions', executiontype=AUTOMATED)
newTestCaseID_B = newTestCase[0]['id']
print "New Test Case '%s' - id: %s" % (NEWTESTCASE_B, newTestCaseID_B)               
# -- END CHANGE v0.4.5 -- 
  
# -- New Examples with v0.4.5 -- 
  
# Add  test cases to test plan - we need the full external id !
tc_aa_full_ext_id = myTestLink.getTestCase(newTestCaseID_AA)[0]['full_tc_external_id']
response = myTestLink._callServer('addTestCaseToTestPlan', 
                {'devKey' : myTestLink.devKey, 
                 'testprojectid' : newProjectID, 
                 'testplanid' : newTestPlanID, 
                 'testcaseexternalid' : tc_aa_full_ext_id, 'version' : 1})
print response
tc_b_full_ext_id = myTestLink.getTestCase(testcaseid=newTestCaseID_B)[0]['full_tc_external_id']
response = myTestLink._callServer('addTestCaseToTestPlan', 
                {'devKey' : myTestLink.devKey, 
                 'testprojectid' : newProjectID, 
                 'testplanid' : newTestPlanID, 
                 'testcaseexternalid' : tc_b_full_ext_id, 'version' : 1})
print response
  
# -- Create Build
newBuild = myTestLink.createBuild(newTestPlanID, NEWBUILD, 'Notes for the Build')
print newBuild
newBuildID = newBuild[0]['id'] 
print "New Build '%s' - id: %s" % (NEWBUILD, newBuildID)
  
# report Test Case Results
# TC_AA failed, build should be guessed, TC identified with external id
newResult = myTestLink.reportTCResult(None, newTestPlanID, None, 'f', '', guess=True,
                                      testcaseexternalid=tc_aa_full_ext_id)
print newResult
# TC_B passed, explicit build and some notes , TC identified with internal id
newResult = myTestLink.reportTCResult(newTestCaseID_B, newTestPlanID, NEWBUILD,
                                      'p', 'first try')
print newResult  

print ""
print "Number of Projects in TestLink: %s " % (myTestLink.countProjects(),)
print ""
myTestLink.listProjects()



 
