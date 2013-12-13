#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2011-2013 Olivier Renault, Luiko Czub, TestLink-API-Python-client developers
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
myTestLink = tl_helper.connect(TestlinkAPIClient) 

projNr=len(myTestLink.getProjects())+1

NEWPROJECT="NEW_PROJECT_API-%i" % projNr
NEWPREFIX="NPROAPI%i" % projNr
NEWTESTPLAN_A="TestPlan_API A"
NEWTESTPLAN_B="TestPlan_API B"
NEWPLATFORM_A='Big Birds %i' % projNr
NEWPLATFORM_B='Small Birds'
NEWPLATFORM_C='Ugly Birds'
NEWTESTSUITE_A="A - First Level"
NEWTESTSUITE_B="B - First Level"
NEWTESTSUITE_AA="AA - Second Level"
NEWTESTCASE_AA="TESTCASE_AA"
NEWTESTCASE_B="TESTCASE_B"
NEWBUILD='%s v%s' % (myTestLink.__class__.__name__ , myTestLink.__version__)

NEWATTACHMENT_PY= os.path.realpath(__file__)
this_file_dirname=os.path.dirname(NEWATTACHMENT_PY)
NEWATTACHMENT_PNG=os.path.join(this_file_dirname, 'PyGreat.png')

# example asking the api client about methods arguments
print myTestLink.whatArgs('createTestCase')


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
    notes='Example created with Python API class %s' % NEWBUILD, 
    active=1, public=1,
    options={'requirementsEnabled' : 0, 'testPriorityEnabled' : 1,
             'automationEnabled' : 1, 'inventoryEnabled' : 0})
print "createTestProject", newProject
newProjectID = newProject[0]['id']
print "New Project '%s' - id: %s" % (NEWPROJECT,newProjectID)
# -- END CHANGE v0.4.5 -- 

# Creates the test plan
# -- Start CHANGE v0.4.5 -- 
# newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN_A, NEWPROJECT,
#             "notes=New TestPlan created with the API","active=1", "public=1")    
# isOk = newTestPlan[0]['message']
# if isOk=="Success!":
#   newTestPlanID_A = newTestPlan[0]['id'] 
#   print "New Test Plan '%s' - id: %s" % (NEWTESTPLAN_A,newTestPlanID_A)
# else:
#   print "Error creating the Test Plan '%s': %s " % (NEWTESTPLAN_A, isOk)
#   sys.exit(-1)
newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN_A, NEWPROJECT,
            notes='New TestPlan created with the API',active=1, public=1)    
print "createTestPlan", newTestPlan
newTestPlanID_A = newTestPlan[0]['id']
print "New Test Plan '%s' - id: %s" % (NEWTESTPLAN_A,newTestPlanID_A)

# Create test plan B  - uses no platforms
newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN_B, NEWPROJECT,
            notes='New TestPlan created with the Generic API - uses no platforms.',
            active=1, public=1)    
print "createTestPlan", newTestPlan
newTestPlanID_B = newTestPlan[0]['id'] 
print "New Test Plan '%s' - id: %s" % (NEWTESTPLAN_B,newTestPlanID_B)
# -- END CHANGE v0.4.5 -- 

# -- Start NEW v0.4.6 -- 
# Create platform 'Big Birds x' 
newPlatForm = myTestLink.createPlatform(NEWPROJECT, NEWPLATFORM_A, 
        notes='Platform for Big Birds, unique name, only used in this project')
print "createPlatform", newPlatForm
newPlatFormID_A = newPlatForm['id']
# Add Platform  'Big Bird x' to platform 
response = myTestLink.addPlatformToTestPlan(newTestPlanID_A, NEWPLATFORM_A) 
print "addPlatformToTestPlan", response

# Create platform 'Small Birds'
newPlatForm = myTestLink.createPlatform(NEWPROJECT, NEWPLATFORM_B, 
                notes='Platform for Small Birds, name used in all example projects')
print "createPlatform", newPlatForm
newPlatFormID_B = newPlatForm['id']
# Add Platform  'Small Bird' to platform 
response = myTestLink.addPlatformToTestPlan(newTestPlanID_A, NEWPLATFORM_B) 
print "addPlatformToTestPlan", response

# Create platform 'Ugly Birds'
newPlatForm = myTestLink.createPlatform(NEWPROJECT, NEWPLATFORM_C, 
                notes='Platform for Ugly Birds, will be removed from test plan')
print "createPlatform", newPlatForm
newPlatFormID_C = newPlatForm['id']
# Add Platform  'Ugly Bird' to platform 
response = myTestLink.addPlatformToTestPlan(newTestPlanID_A, NEWPLATFORM_C) 
print "addPlatformToTestPlan", response
# -- End NEW v0.4.6 -- 

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
print "createTestSuite", newTestSuite
newTestSuiteID_A = newTestSuite[0]['id']
print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_A, newTestSuiteID_A)
# -- END CHANGE v0.4.5 -- 

FirstLevelID = newTestSuiteID_A
 
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
print "createTestSuite", newTestSuite
newTestSuiteID_B = newTestSuite[0]['id']
print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_B, newTestSuiteID_B)
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
print "createTestSuite", newTestSuite
newTestSuiteID_AA = newTestSuite[0]['id']
print "New Test Suite '%s' - id: %s" % (NEWTESTSUITE_AA, newTestSuiteID_AA)
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
newTestCase = myTestLink.createTestCase(NEWTESTCASE_AA, newTestSuiteID_AA, 
          newProjectID, "admin", "This is the summary of the Test Case AA", 
          preconditions='these are the preconditions')
print "createTestCase", newTestCase
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
newTestCase = myTestLink.createTestCase(NEWTESTCASE_B, newTestSuiteID_B, 
          newProjectID, "admin", "This is the summary of the Test Case B", 
          preconditions='these are the preconditions', executiontype=AUTOMATED)
print "createTestCase", newTestCase
newTestCaseID_B = newTestCase[0]['id']
print "New Test Case '%s' - id: %s" % (NEWTESTCASE_B, newTestCaseID_B)               
# -- END CHANGE v0.4.5 -- 
  
# -- New Examples with v0.4.5 or later -- 
  
# Add  test cases to test plan - we need the full external id !
# for every test case version 1 is used
tc_version=1
# TC AA should be tested with platforms 'Big Birds'+'Small Birds'
tc_aa_full_ext_id = myTestLink.getTestCase(newTestCaseID_AA)[0]['full_tc_external_id']
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_A, 
                    tc_aa_full_ext_id, tc_version, platformid=newPlatFormID_A)
print "addTestCaseToTestPlan", response
tc_aa_full_ext_id = myTestLink.getTestCase(newTestCaseID_AA)[0]['full_tc_external_id']
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_A, 
                    tc_aa_full_ext_id, tc_version, platformid=newPlatFormID_B)
print "addTestCaseToTestPlan", response
# TC B should be tested with platform 'Small Birds'
tc_b_full_ext_id = myTestLink.getTestCase(testcaseid=newTestCaseID_B)[0]['full_tc_external_id']
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_A, 
                    tc_b_full_ext_id, tc_version, platformid=newPlatFormID_B)
print "addTestCaseToTestPlan", response
# In test plan B TC B  should be tested without  platform 
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_B, 
                                            tc_b_full_ext_id, tc_version)
print "addTestCaseToTestPlan", response

# # Try to Remove Platform  'Big Birds' from platform 
# response = myTestLink.removePlatformFromTestPlan(newTestPlanID_A, NEWPLATFORM_C) 
# print "removePlatformFromTestPlan", response

# Remove Platform  'Ugly Birds' from platform 
response = myTestLink.removePlatformFromTestPlan(newTestPlanID_A, NEWPLATFORM_C) 
print "removePlatformFromTestPlan", response
  
# -- Create Build
newBuild = myTestLink.createBuild(newTestPlanID_A, NEWBUILD, 'Notes for the Build')
print "createBuild", newBuild
newBuildID = newBuild[0]['id'] 
print "New Build '%s' - id: %s" % (NEWBUILD, newBuildID)
  
# report Test Case Results for platform 'Big Bird'
# TC_AA failed, build should be guessed, TC identified with external id
newResult = myTestLink.reportTCResult(None, newTestPlanID_A, None, 'f', '', guess=True,
                                      testcaseexternalid=tc_aa_full_ext_id,
                                      platformname=NEWPLATFORM_A)
print "reportTCResult", newResult
newResultID_AA = newResult[0]['id']
# report Test Case Results for platform 'Small Bird'
# TC_AA passed, build should be guessed, TC identified with external id
newResult = myTestLink.reportTCResult(None, newTestPlanID_A, None, 'p', '', guess=True,
                                      testcaseexternalid=tc_aa_full_ext_id,
                                      platformname=NEWPLATFORM_B)
print "reportTCResult", newResult
newResultID_AA_p = newResult[0]['id']
# TC_B passed, explicit build and some notes , TC identified with internal id
newResult = myTestLink.reportTCResult(newTestCaseID_B, newTestPlanID_A, NEWBUILD,
                                      'p', 'first try', platformname=NEWPLATFORM_B)
print "reportTCResult", newResult 
newResultID_B = newResult[0]['id']

# add this (text) file as Attachemnt to last execution of TC_B  with 
# different filename 'MyPyExampleApiClient.py'
a_file=open(NEWATTACHMENT_PY)
newAttachment = myTestLink.uploadExecutionAttachment(a_file, newResultID_B, 
            'Textfile Example', 'Text Attachment Example for a TestCase',
            filename='MyPyExampleApiClient.py')
print "uploadExecutionAttachment", newAttachment
# add png file as Attachemnt to last execution of TC_AA
# !Attention - on WINDOWS use binary mode for none text file
# see http://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files
a_file=open(NEWATTACHMENT_PNG, mode='rb')
newAttachment = myTestLink.uploadExecutionAttachment(a_file, newResultID_AA, 
            'PNG Example', 'PNG Attachment Example for a TestCase')
print "uploadExecutionAttachment", newAttachment

# get information - TestProject
response = myTestLink.getTestProjectByName(NEWPROJECT)
print "getTestProjectByName", response
response = myTestLink.getProjectTestPlans(newProjectID)
print "getProjectTestPlans", response
response = myTestLink.getFirstLevelTestSuitesForTestProject(newProjectID)
print "getFirstLevelTestSuitesForTestProject", response

# get information - testPlan
response = myTestLink.getTestPlanByName(NEWPROJECT, NEWTESTPLAN_A)
print "getTestPlanByName", response
response = myTestLink.getTotalsForTestPlan(newTestPlanID_A)
print "getTotalsForTestPlan", response
response = myTestLink.getBuildsForTestPlan(newTestPlanID_A)
print "getBuildsForTestPlan", response
response = myTestLink.getLatestBuildForTestPlan(newTestPlanID_A)
print "getLatestBuildForTestPlan", response
response = myTestLink.getTestPlanPlatforms(newTestPlanID_A)
print "getTestPlanPlatforms", response
response = myTestLink.getTestSuitesForTestPlan(newTestPlanID_A)
print "getTestSuitesForTestPlan", response
# get failed Testcases 
# -- Start CHANGE v0.4.5 -- 
#response = myTestLink.getTestCasesForTestPlan(newTestPlanID_A, 'executestatus=f')
response = myTestLink.getTestCasesForTestPlan(newTestPlanID_A, executestatus='f')
# -- END CHANGE v0.4.5 -- 
print "getTestCasesForTestPlan", response

# get information - TestSuite
response = myTestLink.getTestSuiteByID(newTestSuiteID_B)
print "getTestSuiteByID", response
response = myTestLink.getTestSuitesForTestSuite(newTestSuiteID_A)
print "getTestSuitesForTestSuite", response
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_A, True, 'full')
print "getTestCasesForTestSuite", response
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_B, False, 'only_id')
print "getTestCasesForTestSuite", response

# get informationen - TestCase
# -- Start CHANGE v0.4.5 -- 
#response = myTestLink.getTestCaseIDByName(NEWTESTCASE_B, None, NEWPROJECT)
response = myTestLink.getTestCaseIDByName(NEWTESTCASE_B, testprojectname=NEWPROJECT)
# -- END CHANGE v0.4.5 -- 
print "getTestCaseIDByName", response
tcpathname = '::'.join([NEWPROJECT, NEWTESTSUITE_A, NEWTESTSUITE_AA, NEWTESTCASE_AA])
response = myTestLink.getTestCaseIDByName('unknown', testcasepathname=tcpathname)
print "getTestCaseIDByName", response
# get execution result
response = myTestLink.getLastExecutionResult(newTestPlanID_A, None,
                                             testcaseexternalid=tc_aa_full_ext_id)
print "getLastExecutionResult", response
response = myTestLink.getLastExecutionResult(newTestPlanID_A, newTestCaseID_B)
print "getLastExecutionResult", response


# get information - general 
response = myTestLink.getFullPath(int(newTestSuiteID_AA))
print "getFullPath", response
response = myTestLink.getFullPath([int(newTestCaseID_AA), int(newTestCaseID_B)])
print "getFullPath", response

# no test data
# response = myTestLink.getTestCaseCustomFieldDesignValue(
#             tc_aa_full_ext_id, 1, newProjectID, 'cfieldname', 'simple')
# print "getTestCaseCustomFieldDesignValue", response
print "getTestCaseCustomFieldDesignValue", "Sorry currently no testdata"

# response = myTestLink.getTestCaseAttachments(None, testcaseexternalid=tc_aa_full_ext_id)
# print "getTestCaseAttachments", response
# response = myTestLink.getTestCaseAttachments(newTestCaseID_B)
# print "getTestCaseAttachments", response
print "getTestCaseAttachments", "Sorry currently no testdata"


print ""
print "Number of Projects      in TestLink: %s " % myTestLink.countProjects()
print "Number of Platforms  (in TestPlans): %s " % myTestLink.countPlatforms()
print "Number of Builds                   : %s " % myTestLink.countBuilds()
print "Number of TestPlans                : %s " % myTestLink.countTestPlans()
print "Number of TestSuites               : %s " % myTestLink.countTestSuites()
print "Number of TestCases (in TestSuites): %s " % myTestLink.countTestCasesTS()
print "Number of TestCases (in TestPlans) : %s " % myTestLink.countTestCasesTP()
print ""
myTestLink.listProjects()

print 
print ""
myTestLink.listProjects()


 
