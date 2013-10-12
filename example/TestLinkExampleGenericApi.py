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
  newProjectID = newProject[0]['id'] 
  print "New Project '%s' - id: %s" % (NEWPROJECT,newProjectID)
else:
  print "Error creating the project '%s': %s " % (NEWPROJECT,isOk)
  sys.exit(-1)
 
# Creates the test plan
newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN, NEWPROJECT,
            notes='New TestPlan created with the API',active=1, public=1)    
isOk = newTestPlan[0]['message']
if isOk=="Success!":
  newTestPlanID = newTestPlan[0]['id'] 
  print "New Test Plan '%s' - id: %s" % (NEWTESTPLAN,newTestPlanID)
else:
  print "Error creating the Test Plan '%s': %s " % (NEWTESTPLAN, isOk)
  sys.exit(-1)
 
#Creates the test Suite A      
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_A,
            "Details of the Test Suite A")  
isOk = newTestSuite[0]['message']
if isOk=="ok":
  newTestSuiteID = newTestSuite[0]['id'] 
  print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_A, newTestSuiteID)
else:
  print "Error creating the Test Suite '%s': %s " % (NEWTESTSUITE_A, isOk)
  sys.exit(-1)
 
FirstLevelID = newTestSuiteID 
  
#Creates the test Suite B      
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_B,
            "Details of the Test Suite B")               
isOk = newTestSuite[0]['message']
if isOk=="ok":
  TestSuiteID_B = newTestSuite[0]['id'] 
  print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_B, TestSuiteID_B)
else:
  print "Error creating the Test Suite '%s': %s " % (NEWTESTSUITE_B, isOk)
  sys.exit(-1)
 
#Creates the test Suite AA       
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_AA,
            "Details of the Test Suite AA",parentid=FirstLevelID)               
isOk = newTestSuite[0]['message']
if isOk=="ok":
  TestSuiteID_AA = newTestSuite[0]['id'] 
  print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_AA, TestSuiteID_AA)
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
newTestCase = myTestLink.createTestCase(NEWTESTCASE_AA, TestSuiteID_AA, 
          newProjectID, "admin", "This is the summary of the Test Case AA", 
          steps_tc_aa, preconditions='these are the preconditions')                 
isOk = newTestCase[0]['message']
if isOk=="Success!":
  newTestCaseID = newTestCase[0]['id'] 
  print "New Test Case '%s' - id: %s" % (NEWTESTCASE_AA, newTestCaseID)
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
      
newTestCase = myTestLink.createTestCase(NEWTESTCASE_B, TestSuiteID_B, 
          newProjectID, "admin", "This is the summary of the Test Case B", 
          steps_tc_b, preconditions='these are the preconditions', 
          executiontype=AUTOMATED)               
isOk = newTestCase[0]['message']
if isOk=="Success!":
  newTestCaseID = newTestCase[0]['id'] 
  print "New Test Case '%s' - id: %s" % (NEWTESTCASE_B, newTestCaseID)
else:
  print "Error creating the Test Case '%s': %s " % (NEWTESTCASE_B, isOk)
  sys.exit(-1)
 
print ""
print "Number of Projects in TestLink: %i " % len(myTestLink.getProjects())
print ""
for project in myTestLink.getProjects():
    print "Name: %(name)s ID: %(id)s " % project
print ""
# 
# 
# 
#  
