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
myTestLink = tl_helper.connect(TestlinkAPIGeneric) 


NEWPROJECT="NEW_PROJECT_API_GENERIC"
NEWTESTPLAN="TestPlan_API_GENERIC"
NEWTESTSUITE_A="A - First Level"
NEWTESTSUITE_B="B - First Level"
NEWTESTSUITE_AA="AA - Second Level"
NEWTESTCASE_AA="TESTCASE_AA"
NEWTESTCASE_B="TESTCASE_B"
NEWBUILD="Build v0.4.5"

id_cache={}


if myTestLink.checkDevKey() != True:
    print "Error with the devKey."      
    sys.exit(-1)

print "Number of Projects in TestLink: %i " % len(myTestLink.getProjects())
print ""
for project in myTestLink.getProjects():
    print "Name: %(name)s ID: %(id)s " % project
print ""

# # Creates the project
newProject = myTestLink.createTestProject(NEWPROJECT, 'GPROAPI', 
    notes='This is a Project created with the Generic API', active=1, public=1,
    options={'requirementsEnabled' : 1, 'testPriorityEnabled' : 1, 
             'automationEnabled' : 1,  'inventoryEnabled' : 1})
print(newProject)
isOk = newProject[0]['message']
if isOk=="Success!":
  id_cache[NEWPROJECT] = newProject[0]['id'] 
  print "New Project '%s' - id: %s" % (NEWPROJECT,id_cache[NEWPROJECT])
else:
  print "Error creating the project '%s': %s " % (NEWPROJECT,isOk)
  sys.exit(-1)
 
# Creates the test plan
newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN, NEWPROJECT,
            notes='New TestPlan created with the Generic API',active=1, public=1)    
isOk = newTestPlan[0]['message']
if isOk=="Success!":
  id_cache[NEWTESTPLAN] = newTestPlan[0]['id'] 
  print "New Test Plan '%s' - id: %s" % (NEWTESTPLAN,id_cache[NEWTESTPLAN])
else:
  print "Error creating the Test Plan '%s': %s " % (NEWTESTPLAN, isOk)
  sys.exit(-1)
 
#Creates the test Suite A      
newTestSuite = myTestLink.createTestSuite(id_cache[NEWPROJECT], NEWTESTSUITE_A,
            "Details of the Test Suite A")  
isOk = newTestSuite[0]['message']
if isOk=="ok":
  id_cache[NEWTESTSUITE_A] = newTestSuite[0]['id'] 
  print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_A, id_cache[NEWTESTSUITE_A])
else:
  print "Error creating the Test Suite '%s': %s " % (NEWTESTSUITE_A, isOk)
  sys.exit(-1)
 
FirstLevelID = id_cache[NEWTESTSUITE_A]
  
#Creates the test Suite B      
newTestSuite = myTestLink.createTestSuite(id_cache[NEWPROJECT], NEWTESTSUITE_B,
            "Details of the Test Suite B")               
isOk = newTestSuite[0]['message']
if isOk=="ok":
  id_cache[NEWTESTSUITE_B] = newTestSuite[0]['id'] 
  print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_B, id_cache[NEWTESTSUITE_B])
else:
  print "Error creating the Test Suite '%s': %s " % (NEWTESTSUITE_B, isOk)
  sys.exit(-1)
 
#Creates the test Suite AA       
newTestSuite = myTestLink.createTestSuite(id_cache[NEWPROJECT], NEWTESTSUITE_AA,
            "Details of the Test Suite AA",parentid=FirstLevelID)               
isOk = newTestSuite[0]['message']
if isOk=="ok":
  id_cache[NEWTESTSUITE_AA] = newTestSuite[0]['id'] 
  print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_AA, id_cache[NEWTESTSUITE_AA])
else:
  print "Error creating the Test Suite '%s': %s " % (NEWTESTSUITE_AA, isOk)
  sys.exit(-1)
 
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
newTestCase = myTestLink.createTestCase(NEWTESTCASE_AA, id_cache[NEWTESTSUITE_AA], 
          id_cache[NEWPROJECT], "admin", "This is the summary of the Test Case AA", 
          steps_tc_aa, preconditions='these are the preconditions')                 
isOk = newTestCase[0]['message']
if isOk=="Success!":
  id_cache[NEWTESTCASE_AA] = newTestCase[0]['id'] 
  print "New Test Case '%s' - id: %s" % (NEWTESTCASE_AA, id_cache[NEWTESTCASE_AA])
else:
  print "Error creating the Test Case '%s': %s " % (NEWTESTCASE_AA, isOk)
  sys.exit(-1)
 
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
      
newTestCase = myTestLink.createTestCase(NEWTESTCASE_B, id_cache[NEWTESTSUITE_B], 
          id_cache[NEWPROJECT], "admin", "This is the summary of the Test Case B", 
          steps_tc_b, preconditions='these are the preconditions', 
          executiontype=AUTOMATED)               
isOk = newTestCase[0]['message']
if isOk=="Success!":
  id_cache[NEWTESTCASE_B] = newTestCase[0]['id'] 
  print "New Test Case '%s' - id: %s" % (NEWTESTCASE_B, id_cache[NEWTESTCASE_B])
else:
  print "Error creating the Test Case '%s': %s " % (NEWTESTCASE_B, isOk)
  sys.exit(-1)
  
# Add  test cases to test plan - we need the full external id !
tc_aa_full_ext_id = myTestLink.getTestCase(testcaseid=id_cache[NEWTESTCASE_AA])[0]['full_tc_external_id']
response = myTestLink._callServer('addTestCaseToTestPlan', 
                {'devKey' : myTestLink.devKey, 
                 'testprojectid' : id_cache[NEWPROJECT], 
                 'testplanid' : id_cache[NEWTESTPLAN], 
                 'testcaseexternalid' : tc_aa_full_ext_id, 'version' : 1})
print response
tc_b_full_ext_id = myTestLink.getTestCase(testcaseid=id_cache[NEWTESTCASE_B])[0]['full_tc_external_id']
response = myTestLink._callServer('addTestCaseToTestPlan', 
                {'devKey' : myTestLink.devKey, 
                 'testprojectid' : id_cache[NEWPROJECT], 
                 'testplanid' : id_cache[NEWTESTPLAN], 
                 'testcaseexternalid' : tc_b_full_ext_id, 'version' : 1})
print response

# -- Create Build
newBuild = myTestLink.createBuild(id_cache[NEWTESTPLAN], NEWBUILD, 
                                  buildnotes='Notes for the Build')
print newBuild
isOk = newBuild[0]['message']
if isOk=="Success!":
  id_cache[NEWBUILD] = newBuild[0]['id'] 
  print "New Build '%s' - id: %s" % (NEWBUILD, id_cache[NEWBUILD])
else:
  print "Error creating the Build '%s': %s " % (NEWBUILD, isOk)
  sys.exit(-1)
  
# report Test Case Results
# TC_AA failed, build should be guessed, TC identified with external id
newResult = myTestLink.reportTCResult(id_cache[NEWTESTPLAN], 'f', guess=True,
                                     testcaseexternalid=tc_aa_full_ext_id)
print newResult
# TC_B passed, explicit build and some notes , TC identified with internal id
newResult = myTestLink.reportTCResult(id_cache[NEWTESTPLAN], 'p', 
                buildid=id_cache[NEWBUILD], testcaseid=id_cache[NEWTESTCASE_B], 
                notes="first try")
print newResult

print ""
print "Number of Projects in TestLink: %i " % len(myTestLink.getProjects())
print ""
for project in myTestLink.getProjects():
    print "Name: %(name)s ID: %(id)s " % project
print ""

 
# 
# 
#  
