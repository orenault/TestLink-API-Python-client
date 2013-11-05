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

import xmlrpclib
import testlinkerrors
from .testlinkhelper import TestLinkHelper, VERSION
from .testlinkargs import getMethodsWithPositionalArgs
from .testlinkdecorators import decoApiCallAddAttachment,\
decoApiCallAddDevKey, decoApiCallWithoutArgs, \
decoMakerApiCallReplaceTLResponseError, decoMakerApiCallWithArgs 


class TestlinkAPIGeneric(object): 
    """ client for xmlrpc communication between Python and TestLlink 
        Implements the Testlink API methods as generic PY methods with 
        error handling.
        
        Allows the configuration of arguments for these API method as positional
        or optional arguments.
        
        Changes of TestLink API methods should be implemented in this base class.
        Service Methods like "countProjects" should be implemented on subclasses
        like TestlinkAPIClient
    """   
    
    __slots__ = ['server', 'devKey', '_server_url', '_positionalArgNames']
 
    __version__ = VERSION
    __author__ = 'Luiko Czub, TestLink-API-Python-client developers'

    def __init__(self, server_url, devKey, **args):
        transport=args.get('transport')
        encoding=args.get('encoding')
        verbose=args.get('verbose',0)
        allow_none=args.get('allow_none',0)
        self.server = xmlrpclib.Server(server_url, transport, encoding, 
                                       verbose, allow_none)
        self.devKey = devKey
        self._server_url = server_url
        self._positionalArgNames = getMethodsWithPositionalArgs()
        
        
        
    # GENERIC API CALLS - using decorators
    # http://stackoverflow.com/questions/1015307/python-bind-an-unbound-method
    
    # Method definitions should be build either with 
    # @decoMakerApiCallWithArgs(argNamesPositional, argNamesOptional)
    #    for calling a server method with arguments 
    #    - argNamesPositional = list default positional args
    #    - argNamesOptional   = list additional optional args
    #    to check the server response, if it includes TestLink Error Codes or 
    #    an empty result (which raise a TLResponseError) 
    # or   
    # @decoApiCallWithoutArgs
    #    for calling server methods without arguments
    #    to check the server response, if it includes TestLink Error Codes or 
    #    an empty result (which raise a TLResponseError)
    #  
    # Additional behavior could be added with
    #    
    # @decoApiCallAddDevKey
    #    - to expand the parameter list with devKey key/value pair
    #      before calling the server method
    # @decoMakerApiCallReplaceTLResponseError(replaceCode)
    #    - to catch an TLResponseError after calling the server method and 
    #      with an empty list
    #      - replaceCode : TestLink Error Code, which should be handled 
    #                      default is None for "Empty Results"
    # @decoApiCallAddAttachment(methodAPI):
    #     - to add an mandatory argument 'attachmentfile'
    #       - attachmentfile is a python file descriptor pointing to the file 
    #     - to expand parameter list with key/value pairs
    #          'filename', 'filetype', 'content'
    #       from 'attachmentfile' before calling the server method


    @decoApiCallAddDevKey            
    @decoMakerApiCallWithArgs(['testplanid'])
    def getLatestBuildForTestPlan(self):
        """ getLatestBuildForTestPlan: Gets the latest build by choosing the 
                                    maximum build id for a specific test plan 
        positional args: testplanid
        optional args : --- """
    
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'], 
                              ['testcaseid', 'testcaseexternalid'])
    def getLastExecutionResult(self):
        """ getLastExecutionResult: 
        Gets the result of LAST EXECUTION for a particular testcase
        on a test plan, but WITHOUT checking for a particular build
        positional args: testplanid
        optional args : testcaseid, testcaseexternalid """

    @decoApiCallWithoutArgs
    def sayHello(self):
        """ sayHello: Lets you see if the server is up and running
        positional args: ---
        optional args : --- """

    def ping(self):
        """ alias for methodAPI sayHello """ 
        return self.sayHello()
    
    @decoMakerApiCallWithArgs(['str'])
    def repeat(self):
        """ repeat: Repeats a message back
        positional args: str
        optional args : --- """
    
    @decoApiCallWithoutArgs
    def about(self):
        """ about: Gives basic information about the API
        positional args: ---
        optional args : --- """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid', 'buildname'], 
                              ['buildnotes'])
    def createBuild(self):
        """ createBuild: Creates a new build for a specific test plan
        positional args: testplanid, buildname
        optional args : buildnotes """

    @decoApiCallAddDevKey            
    @decoMakerApiCallWithArgs()
    def getProjects(self):
        """ getProjects: Gets a list of all projects
        positional args: ---
        optional args : --- """

    @decoMakerApiCallReplaceTLResponseError()            
    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testprojectid'])
    def getProjectTestPlans(self):
        """ getProjectTestPlans: Gets a list of test plans within a project
        positional args: testprojectid
        optional args : ---  
        
        returns an empty list, if no testplan is assigned """

    @decoMakerApiCallReplaceTLResponseError()          
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'])
    def getBuildsForTestPlan(self):
        """ getBuildsForTestPlan : Gets a list of builds within a test plan 
        positional args: testplanid
        optional args : --- 
        
        returns an empty list, if no build is assigned """

    @decoMakerApiCallReplaceTLResponseError()          
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'])
    def getTestSuitesForTestPlan(self):
        """ getTestSuitesForTestPlan : List test suites within a test plan alphabetically
        positional args: testplanid
        optional args : ---  
        
        returns an empty list, if no build is assigned """
        
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testprojectname', 'testcaseprefix'],
                              ['notes', 'active', 'public', 'options'])
    def createTestProject(self):
        """ createTestProject : Create a test project  
        positional args: testprojectname, testcaseprefix
        optional args : notes,  active, public, options
        
        options : dictionary with keys
                    requirementsEnabled, testPriorityEnabled, 
                    automationEnabled,inventoryEnabled
                 and values 0 (false) and 1 (true)     """
        
    @decoMakerApiCallReplaceTLResponseError()          
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testsuiteid'], ['deep', 'details'])
    def getTestCasesForTestSuite(self):
        """ getTestCasesForTestSuite : List test suites within a test plan alphabetically
        positional args: testsuiteid
        optional args : deep, details
        
        details - default is 'simple', 
                  use 'full' if you want to get summary,steps & expected_results
                  or 'only_id', if you just need an ID list
        
        returns an empty list, if no build is assigned """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testcasename'], 
                    ['testsuitename', 'testprojectname', 'testcasepathname'])
    def getTestCaseIDByName(self):
        """ getTestCaseIDByName : Find a test case by its name 
        positional args: testcasename, 
        optional args : testsuitename, testprojectname, testcasepathname
        
        testcasepathname : Full test case path name, 
                starts with test project name , pieces separator -> ::   
        server return can be a list or a dictionary 
        - optional arg testprojectname seems to create a dictionary response """
 
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testcasename', 'testsuiteid', 'testprojectid', 
                               'authorlogin', 'summary', 'steps'], 
                ['preconditions', 'importance', 'execution', 'order', 
                 'internalid', 'checkduplicatedname', 'actiononduplicatedname'])
    def createTestCase(self):
        """ createTestCase: Create a test case
        positional args: testcasename, testsuiteid, testprojectid, authorlogin,
                         summary, steps
        optional args : preconditions, importance, execution, order, internalid,
                        checkduplicatedname, actiononduplicatedname 
                        
            steps is a list with dictionaries , example
            [{'step_number' : 1, 'actions' : "action A" , 
                'expected_results' : "result A", 'execution_type' : 0},
                 {'step_number' : 2, 'actions' : "action B" , 
                'expected_results' : "result B", 'execution_type' : 1},
                 {'step_number' : 3, 'actions' : "action C" , 
                'expected_results' : "result C", 'execution_type' : 0}]
            """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid', 'status'], 
                ['testcaseid', 'testcaseexternalid', 'buildid', 'buildname', 
                 'platformid', 'platformname', 'notes', 'guess', 'bugid', 
                 'customfields', 'overwrite'])
    def reportTCResult(self):
        """ reportTCResult : Reports a result for a single test case
        positional args: testplanid, status
        optional args (variations): testcaseid - testcaseexternalid
                                    buildid - buildname
                                    platformid - platformname
        optional args : notes, guess, bugid, customfields, overwrite 
        
        customfields : dictionary with customfields names + values
            VERY IMPORTANT: value must be formatted in the way it's written to db
 """

#   /**
#    * turn on/off testMode
#    *
#    * This method is meant primarily for testing and debugging during development
#    * @param struct $args
#    * @return boolean
#    * @access protected
#    */  
#   public function setTestMode($args)

    @decoMakerApiCallReplaceTLResponseError()          
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'], 
                ['testcaseid', 'keywordid', 'keywords', 'executed', 'assignedto', 
                 'executestatus', 'executiontype', 'getstepinfo', 'details'])
    def getTestCasesForTestPlan(self):
        """ getTestCasesForTestPlan : List test cases linked to a test plan
        positional args: testplanid
        optional args : testcaseid, keywordid, keywords, executed, assignedto,
                        executestatus, executiontype, getstepinfo, details
        
        details - default is 'full', 
                  'simple', 'details' ??

        
        returns an empty list, if no build is assigned """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testcaseexternalid', 'version', 'testprojectid', 
                               'customfieldname'], ['details'])
    def getTestCaseCustomFieldDesignValue(self):
        """ getTestCaseCustomFieldDesignValue : 
        Gets value of a Custom Field with scope='design' for a given Test case
        positional args: testcaseexternalid, version, testprojectid, 
                        customfieldname
        optional args :  details
        
        details =  changes output information
            null or 'value' => just value
            'full' => a map with all custom field definition
                          plus value and internal test case id
            'simple' => value plus custom field name, label, and type (as code).
            
        attention - becareful with testcaseexternalid - it must include an '-'. 
        otherwise TL returns 
        <ProtocolError for xmlrpc.php: 500 Internal Server Error>  """

#    /**
#     * Add a test case version to a test plan 
#     *
#     * @param args['testprojectid']
#     * @param args['testplanid']
#     * @param args['testcaseexternalid']
#     * @param args['version']
#     * @param args['platformid'] - OPTIONAL Only if  test plan has no platforms
#     * @param args['executionorder'] - OPTIONAL
#     * @param args['urgency'] - OPTIONAL
#     *
#     */
#   public function addTestCaseToTestPlan($args)

    @decoMakerApiCallReplaceTLResponseError(7008)            
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testprojectid'])
    def getFirstLevelTestSuitesForTestProject(self):
        """ getFirstLevelTestSuitesForTestProject :  get set of test suites 
                            AT TOP LEVEL of tree on a Test Project
                            
        positional args: testprojectid
        optional args : ---  
        
        returns an empty list, if no suite is assigned (api error 7008) 
        - details see comments for decoMakerApiCallReplaceTLResponseError """

#    /**
#     *  Assign Requirements to a test case 
#     *  we can assign multiple requirements.
#     *  Requirements can belong to different Requirement Spec
#     *         
#   *  @param struct $args
#   *  @param string $args["devKey"]
#   *  @param int $args["testcaseexternalid"]
#   *  @param int $args["testprojectid"] 
#     *  @param string $args["requirements"] 
#     *                array(array('req_spec' => 1,'requirements' => array(2,4)),
#     *                array('req_spec' => 3,'requirements' => array(22,42))
#     *
#     */
#    public function assignRequirements($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs([], ['testcaseid', 'testcaseexternalid'])
    def getTestCaseAttachments(self):
        """ getTestCaseAttachments: Gets attachments for specified test case.
        The attachment file content is Base64 encoded. To save the file to disk 
        in client, Base64 decode the content and write file in binary mode. 
        positional args: ---
        optional args : testcaseid, testcaseexternalid """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testprojectid', 'testsuitename', 'details'], 
                              ['parentid', 'order', 'checkduplicatedname', 
                               'actiononduplicatedname'])
    def createTestSuite(self):
        """ createTestSuite: create a test suite
        positional args: testprojectid, testsuitename, details
        optional args : parentid, order, checkduplicatedname, 
                        actiononduplicatedname """

    @decoApiCallAddDevKey            
    @decoMakerApiCallWithArgs(['testprojectname'])
    def getTestProjectByName(self):
        """ getTestProjectByName: Gets info about target test project
        positional args: testprojectname
        optional args : --- """

    @decoApiCallAddDevKey            
    @decoMakerApiCallWithArgs(['testprojectname', 'testplanname'])
    def getTestPlanByName(self):
        """ getTestPlanByName: Gets info about target test project
        positional args: testprojectname, testplanname
        optional args : --- """


    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs([], ['testcaseid', 'testcaseexternalid', 'version'])
    def getTestCase(self):
        """ getTestCase: get test case specification using external or internal id
        positional args: ---
        optional args : testcaseid, testcaseexternalid, version
        
        attention - becareful with testcaseexternalid - it must inlcude an '-'. 
        otherwise TL returns 
        <ProtocolError for xmlrpc.php: 500 Internal Server Error>"""

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanname', 'testprojectname'], 
                              ['note', 'active', 'public'])
    def createTestPlan(self):
        """ createTestPlan : create a test plan
        positional args: testplanname, testprojectname
        optional args : notes,  active, public """


    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['nodeid'])
    def getFullPath(self):
        """ getFullPath : Gets full path from the given node till the top using 
                          nodes_hierarchy_table
        positional args: nodeid
        optional args : ---  
        
        nodeid = can be just a single id or a list with ids 
                 ATTENTION: id must be an integer. """

#    /**
#    * delete an execution
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["executionid"]
#    *
#    * @return mixed $resultInfo 
#    *         [status]  => true/false of success
#    *         [id]      => result id or error code
#    *         [message]  => optional message for error message string
#    * @access public
#    */  
#    public function deleteExecution($args)


    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testsuiteid'])
    def getTestSuiteByID(self):
        """ getTestSuiteByID : Return a TestSuite by ID
        
        positional args: testsuiteid
        optional args : ---  """


    @decoMakerApiCallReplaceTLResponseError()            
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testsuiteid'])
    def getTestSuitesForTestSuite(self):
        """ getTestSuitesForTestSuite :  get list of TestSuites which are DIRECT
                                         children of a given TestSuite
        positional args: testsuiteid
        optional args : ---  
        
        returns an empty list, if no platform is assigned """

    @decoMakerApiCallReplaceTLResponseError(3041)            
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'])
    def getTestPlanPlatforms(self):
        """ getTestPlanPlatforms :  Returns the list of platforms associated to 
                                    a given test plan
        positional args: testplanid
        optional args : ---  
        
        returns an empty list, if no platform is assigned (api error 3041) 
        - details see comments for decoMakerApiCallReplaceTLResponseError """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'])
    def getTotalsForTestPlan(self):
        """ getTotalsForTestPlan :  Gets the summarized results grouped by platform.
        positional args: testplanid
        optional args : ---  """

    @decoMakerApiCallWithArgs(['user'])
    def doesUserExist(self):
        """ doesUserExist : Checks if user name exists 
        positional args: user
        optional args : --- 
        returns true if everything OK, otherwise error structure """
               
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['devKey'])
    def checkDevKey(self):
        """ checkDevKey :  check if Developer Key exists 
        positional args: ---
        optional args : --- 
        returns true if everything OK, otherwise error structure """
        
# /**
#  * Uploads an attachment for a Requirement Specification.
#  * 
#  * The attachment content must be Base64 encoded by the client before sending it.
#  * 
#  * @param struct $args
#  * @param string $args["devKey"] Developer key
#  * @param int $args["reqspecid"] The Requirement Specification ID
#  * @param string $args["title"] (Optional) The title of the Attachment 
#  * @param string $args["description"] (Optional) The description of the Attachment
#  * @param string $args["filename"] The file name of the Attachment (e.g.:notes.txt)
#  * @param string $args["filetype"] The file type of the Attachment (e.g.: text/plain)
#  * @param string $args["content"] The content (Base64 encoded) of the Attachment
#  * 
#  * @since 1.9beta6
#  * @return mixed $resultInfo an array containing the fk_id, fk_table, title, 
#  * description, file_name, file_size and file_type. If any errors occur it 
#  * returns the error map.
#  */
# public function uploadRequirementSpecificationAttachment($args)
        
# /**
#  * Uploads an attachment for a Requirement.
#  * 
#  * The attachment content must be Base64 encoded by the client before sending it.
#  * 
#  * @param struct $args
#  * @param string $args["devKey"] Developer key
#  * @param int $args["requirementid"] The Requirement ID
#  * @param string $args["title"] (Optional) The title of the Attachment 
#  * @param string $args["description"] (Optional) The description of the Attachment
#  * @param string $args["filename"] The file name of the Attachment (e.g.:notes.txt)
#  * @param string $args["filetype"] The file type of the Attachment (e.g.: text/plain)
#  * @param string $args["content"] The content (Base64 encoded) of the Attachment
#  * 
#  * @since 1.9beta6
#  * @return mixed $resultInfo an array containing the fk_id, fk_table, title, 
#  * description, file_name, file_size and file_type. If any errors occur it 
#  * returns the erros map.
#  */
# public function uploadRequirementAttachment($args)        

# /**
#  * Uploads an attachment for a Test Project.
#  * 
#  * The attachment content must be Base64 encoded by the client before sending it.
#  * 
#  * @param struct $args
#  * @param string $args["devKey"] Developer key
#  * @param int $args["testprojectid"] The Test Project ID
#  * @param string $args["title"] (Optional) The title of the Attachment 
#  * @param string $args["description"] (Optional) The description of the Attachment
#  * @param string $args["filename"] The file name of the Attachment (e.g.:notes.txt)
#  * @param string $args["filetype"] The file type of the Attachment (e.g.: text/plain)
#  * @param string $args["content"] The content (Base64 encoded) of the Attachment
#  * 
#  * @since 1.9beta6
#  * @return mixed $resultInfo an array containing the fk_id, fk_table, title, 
#  * description, file_name, file_size and file_type. If any errors occur it 
#  * returns the erros map.
#  */
# public function uploadTestProjectAttachment($args)

# /**
#  * Uploads an attachment for a Test Suite.
#  * 
#  * The attachment content must be Base64 encoded by the client before sending it.
#  * 
#  * @param struct $args
#  * @param string $args["devKey"] Developer key
#  * @param int $args["testsuiteid"] The Test Suite ID
#  * @param string $args["title"] (Optional) The title of the Attachment 
#  * @param string $args["description"] (Optional) The description of the Attachment
#  * @param string $args["filename"] The file name of the Attachment (e.g.:notes.txt)
#  * @param string $args["filetype"] The file type of the Attachment (e.g.: text/plain)
#  * @param string $args["content"] The content (Base64 encoded) of the Attachment
#  * 
#  * @since 1.9beta6
#  * @return mixed $resultInfo an array containing the fk_id, fk_table, title, 
#  * description, file_name, file_size and file_type. If any errors occur it 
#  * returns the erros map.
#  */
# public function uploadTestSuiteAttachment($args)

# /**
#  * Uploads an attachment for a Test Case.
#  * 
#  * The attachment content must be Base64 encoded by the client before sending it.
#  * 
#  * @param struct $args
#  * @param string $args["devKey"] Developer key
#  * @param int $args["testcaseid"] Test Case INTERNAL ID
#  * @param string $args["title"] (Optional) The title of the Attachment 
#  * @param string $args["description"] (Optional) The description of the Attachment
#  * @param string $args["filename"] The file name of the Attachment (e.g.:notes.txt)
#  * @param string $args["filetype"] The file type of the Attachment (e.g.: text/plain)
#  * @param string $args["content"] The content (Base64 encoded) of the Attachment
#  * 
#  * @since 1.9beta6
#  * @return mixed $resultInfo an array containing the fk_id, fk_table, title, 
#  * description, file_name, file_size and file_type. If any errors occur it 
#  * returns the erros map.
#  */
# public function uploadTestCaseAttachment($args)


    @decoApiCallAddAttachment            
    @decoMakerApiCallWithArgs(['executionid'], 
                    ['title', 'description', 'filename', 'filetype', 'content'])
    def uploadExecutionAttachment(self):
        """ uploadExecutionAttachment: Uploads an attachment for an execution
        mandatory args: attachmentfile
        positional args: executionid
        optional args : title, description, filename, filetype, content
        
        attachmentfile: python file descriptor pointing to the file
        !Attention - on WINDOWS use binary mode for none text file
        see http://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files
        
        default values for filename, filetype, content are determine from 
        ATTACHMENTFILE, but user could overwrite it, if they want to store the
        attachment with a different name 
        """


# /**
#  * Uploads an attachment for specified table. You must specify the table that 
#  * the attachment is connected (nodes_hierarchy, builds, etc) and the foreign 
#  * key id in this table.
#  * 
#  * The attachment content must be Base64 encoded by the client before sending it.
#  * 
#  * @param struct $args
#  * @param string $args["devKey"] Developer key
#  * @param int $args["fkid"] The Attachment Foreign Key ID
#  * @param string $args["fktable"] The Attachment Foreign Key Table
#  * @param string $args["title"] (Optional) The title of the Attachment 
#  * @param string $args["description"] (Optional) The description of the Attachment
#  * @param string $args["filename"] The file name of the Attachment (e.g.:notes.txt)
#  * @param string $args["filetype"] The file type of the Attachment (e.g.: text/plain)
#  * @param string $args["content"] The content (Base64 encoded) of the Attachment
#  * 
#  * @since 1.9beta6
#  * @return mixed $resultInfo an array containing the fk_id, fk_table, title, 
#  * description, file_name, file_size and file_type. If any errors occur it 
#  * returns the erros map.
#  */
# public function uploadAttachment($args, $messagePrefix='', $setArgs=true)

#     /**
#      * Gets value of a Custom Field for a entity in a given scope (e.g.: a custom
#      * field for a test case in design scope).
#      *
#      * BUGID-4188: feature request - new method - getTestSuiteCustomFieldValue
#      *
#      * @param struct $args
#      * @param string $args["devKey"]: used to check if operation can be done.
#      *                                if devKey is not valid => abort.
#      *
#      * @param string $args["customfieldname"]: custom field name
#      * @param int     $args["tprojectid"]: project id
#      * @param string $args["nodetype"]: note type (testcase, testsuite, ...)
#      * @param int    $args["nodeid"]: node id (test case version id, project id, ...)
#      * @param string $args["scope"]: cf scope (execution, design or testplan_design)
#      * @param int    $args["executionid"]: execution id
#      * @param int    $args["testplanid"]: test plan id
#      * @param int    $args["linkid"]: link id for nodes linked at test plan design scope
#      *
#      * @return mixed $resultInfo
#      *
#      * @access protected
#      */
#     protected function getCustomFieldValue($args)

#     /**
#      * Gets a Custom Field of a Test Case in Execution Scope.
#      * 
#      * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["customfieldname"]: custom field name
#    * @param int    $args["tprojectid"]: project id
#    * @param int    $args["version"]: test case version id
#    * @param int    $args["executionid"]: execution id
#    * @param int    $args["testplanid"]: test plan id
#    *
#    * @return mixed $resultInfo
#    *
#    * @access public
#      */
#   public function getTestCaseCustomFieldExecutionValue($args)
     
#   /**
#     * Gets a Custom Field of a Test Case in Test Plan Design Scope.
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                 if devKey is not valid => abort.
#    *
#    * @param string $args["customfieldname"]: custom field name
#    * @param int    $args["testcaseid"]: project id
#    * @param int    $args["version"]: test case version id
#    * @param int    $args["testplanid"]: test plan id
#    * @param int    $args["linkid"]: link id (important!)
#    *
#    * @return mixed $resultInfo
#    *
#    * @access public
#    */
#   public function getTestCaseCustomFieldTestPlanDesignValue($args)
               
#   /**
#    * Gets a Custom Field of a Test Suite in Design Scope.
#    *
#    * @param struct $args
#     * @param string $args["devKey"]: used to check if operation can be done.
#     *                                 if devKey is not valid => abort.
#    *
#    * @param string $args["customfieldname"]: custom field name
#    * @param int   $args["tprojectid"]: project id
#     * @param int    $args["testsuiteid"]: test suite id
#    * 
#    * @return mixed $resultInfo
#    *
#    * @access public
#    */
#   public function getTestSuiteCustomFieldDesignValue($args)
               
#   /**
#    * Gets a Custom Field of a Test Plan in Design Scope.
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["customfieldname"]: custom field name
#    * @param int    $args["tprojectid"]: project id
#    * @param int    $args["testplanid"]: test plan id
#    *
#    * @return mixed $resultInfo
#    *
#    * @access public
#    */
#   public function getTestPlanCustomFieldDesignValue($args)

#     /**
#      * Gets a Custom Field of a Requirement Specification in Design Scope.
#      * 
#      * @param struct $args
#      * @param string $args["devKey"]: used to check if operation can be done.
#      *                                if devKey is not valid => abort.
#      *
#      * @param string $args["customfieldname"]: custom field name
#      * @param int    $args["tprojectid"]: project id
#      * @param int    $args["reqspecid"]: requirement specification id
#      * 
#      * @return mixed $resultInfo
#      * 
#      * @access public
#      */
#     public function getReqSpecCustomFieldDesignValue($args)
               
#     /**
#      * Gets a Custom Field of a Requirement in Design Scope.
#      * 
#      * @param struct $args
#      * @param string $args["devKey"]: used to check if operation can be done.
#      *                                if devKey is not valid => abort.
#      *
#      * @param string $args["customfieldname"]: custom field name
#      * @param int    $args["tprojectid"]: project id
#      * @param int    $args["requirementid"]: requirement id
#      * 
#      * @return mixed $resultInfo
#      * 
#      * @access public
#      */
#     public function getRequirementCustomFieldDesignValue($args)

#   /**
#    * createTestCaseSteps - can be used also for upgrade (see action)
#    * 
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param string $args["testcaseexternalid"] optional if you provide $args["testcaseid"]
#    * @param string $args["testcaseid"] optional if you provide $args["testcaseexternalid"]
#    * @param string $args["version"] - optional if not provided LAST ACTIVE version will be used
#    *                                  if all versions are INACTIVE, then latest version will be used.   
#    * @param string $args["action"]
#    *               possible values
#    *               'create','update','push'
#    *               create: if step exist NOTHING WILL BE DONE
#    *               update: if step DOES NOT EXIST will be created
#    *                       else will be updated.
#    *               push: shift down all steps with step number >= step number provided
#    *                     and use provided data to create step number requested.
#    *                     NOT IMPLEMENTED YET  
#    * @param array  $args["steps"]:
#    *                each element is a hash with following keys
#    *                step_number,actions,expected_results,execution_type
#    * 
#    * @return mixed $resultInfo
#    *
#    * @internal revisions
#    * 20111018 - franciscom - TICKET 4774: New methods to manage test case steps
#    */
#   function createTestCaseSteps($args)

#   /**
#    * deleteTestCaseSteps
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param string $args["testcaseexternalid"]
#    * @param string $args["version"] - optional if not provided LAST ACTIVE version will be used
#    * @param array  $args["steps"]: each element is a step_number
#    * 
#    * @return mixed $resultInfo
#    *
#    * @internal revisions
#    * 20111018 - franciscom - TICKET 4774: New methods to manage test case steps
#    */
#   function deleteTestCaseSteps($args)

#   /**
#    * Update value of Custom Field with scope='design' for a given Test case
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["testcaseexternalid"]:  
#    * @param string $args["version"]: version number  
#    * @param string $args["testprojectid"]: 
#    * @param string $args["customfields"] - optional
#    *               contains an map with key:Custom Field Name, value: value for CF.
#    *               VERY IMPORTANT: value must be formatted in the way it's written to db,
#    *               this is important for types like:
#    *
#    *               DATE: strtotime()
#    *               DATETIME: mktime()
#    *               MULTISELECTION LIST / CHECKBOX / RADIO: se multipli selezione ! come separatore
#    *
#    *
#    *               these custom fields must be configured to be writte during execution.
#    *               If custom field do not meet condition value will not be written
#    *
#    * @return mixed null if everything ok, else array of IXR_Error objects
#    *         
#    * @access public
#    */    
#   public function updateTestCaseCustomFieldDesignValue($args)

#   /**
#    * Update execution type for a test case version
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["testcaseexternalid"]:  
#    * @param string $args["version"]: version number  
#    * @param string $args["testprojectid"]: 
#      * @param string $args["executiontype"]: TESTCASE_EXECUTION_TYPE_MANUAL,
#      *                     TESTCASE_EXECUTION_TYPE_AUTOMATIC
#      *
#      * @return mixed null if everything ok, else array of IXR_Error objects
#    *         
#    * @access public
#    */    
#   public function setTestCaseExecutionType($args)

#   /**
#    *
#    */
#   public function getExecCountersByBuild($args)

#   /**
#    * create platform 
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testprojectname"]
#    * @param map $args["platformname"]
#    * @param map $args["notes"]
#    * @return mixed $resultInfo
#    * @internal revisions
#    */
#   public function createPlatform($args)

#   /**
#    *
#    */
#   public function getProjectPlatforms($args)

#   /**
#    * addPlatformToTestPlan 
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testplanid"]
#    * @param map $args["platformname"]
#    * @return mixed $resultInfo
#    * @internal revisions
#    */
#   public function addPlatformToTestPlan($args)

#   /**
#    * removePlatformFromTestPlan 
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testplanid"]
#    * @param map $args["platformname"]
#    * @return mixed $resultInfo
#    * @internal revisions
#    */
#   public function removePlatformFromTestPlan($args)

#   /**
#    * if everything ok returns an array on just one element with following user data
#    *
#    * firstName,lastName,emailAddress,locale,isActive,defaultTestprojectID,
#    * globalRoleID 
#    * globalRole    array with role info
#    * tprojectRoles array  
#    * tplanRoles    array
#    * login 
#    * dbID
#    * loginRegExp
#    *
#    * ATTENTION: userApiKey will be set to NULL, because is worst that access to user password
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]   
#    * @param string $args["user"]   Login Name   
#    * 
#    * @return mixed $ret
#    * 
#    */
#   public function getUserByLogin($args)


#   /**
#    * if everything ok returns an array on just one element with following user data
#    *
#    * firstName,lastName,emailAddress,locale,isActive,defaultTestprojectID,
#    * globalRoleID 
#    * globalRole    array with role info
#    * tprojectRoles array  
#    * tplanRoles    array
#    * login 
#    * dbID
#    * loginRegExp
#    *
#    * ATTENTION: userApiKey will be set to NULL, because is worst that access to user password
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]   
#    * @param string $args["userid"]   user ID as present on users table, column ID
#    * 
#    * @return mixed $ret
#    * 
#    */
#   public function getUserByID($args)

#    /**
#     * Update an existing test case
#     * Not all test case attributes will be able to be updated using this method
#     * See details below
#     * 
#     * @param struct $args
#     * @param string $args["devKey"]
#     * @param string $args["testcaseexternalid"] format PREFIX-NUMBER
#     * @param int    $args["version"] optional version NUMBER (human readable) 
#     * @param string $args["testcasename"] - optional
#     * @param string $args["summary"] - optional
#     * @param string $args["preconditions"] - optional
#     * @param array  $args["steps"] - optional
#     *               each element is a hash with following keys
#     *               step_number,actions,expected_results,execution_type
#     *
#     * @param int    $args["importance"] - optional - see const.inc.php for domain
#     * @param int    $args["executiontype"] - optional - see ... for domain
#     * @param int    $args["status'] - optional
#     * @param int    $args["estimatedexecduration'] - optional
#     * @param string $args["user'] - login name used as updater - optional
#     *                               if not provided will be set to user that request update
#     */
#    public function updateTestCase($args)


    
    #
    #  public methods for general server calls
    #                                   

    def callServerWithPosArgs(self, methodNameAPI, *argsPositional, **argsOptional):
        """ concat argsPositional and argsOptional before calling 
        server method methodNameAPI """

        if argsPositional:
            # search keys for values and store these pairs in a dictionary
            dictPos = self._convertPostionalArgs(methodNameAPI, argsPositional)
            # extent optional keys+values with positional keys+vales  
            argsOptional.update(dictPos)
        # now, start calling the server with basic error handling
        response = self._callServer(methodNameAPI, argsOptional)
        # check if response is not empyt and not includes error code
        self._checkResponse(response, methodNameAPI, argsOptional) 
        # seams to be ok, so let give them the data
        return response

    #
    #  internal methods for general server calls
    #                                   

    def _callServer(self, methodNameAPI, argsAPI=None):
        """ call server method METHODNAMEAPI with error handling and 
        returns the responds
        internal method - should not be called directly """
        
        response = None
        try:
            if argsAPI is None:
                response = getattr(self.server.tl, methodNameAPI)()
            else:
                response = getattr(self.server.tl, methodNameAPI)(argsAPI)
        except (IOError, xmlrpclib.ProtocolError), msg:
            new_msg = 'problems connecting the TestLink Server %s\n%s' %\
            (self._server_url, msg) 
            raise testlinkerrors.TLConnectionError(new_msg)
        except xmlrpclib.Fault, msg:
            new_msg = 'problems calling the API method %s\n%s' %\
            (methodNameAPI, msg) 
            raise testlinkerrors.TLAPIError(new_msg)

        return response
    
        
    def _convertPostionalArgs(self, methodName, valueList):        
        """ Returns a dictionary with values from VALUELIST and keys for 
            the expected positional argumenst of selfs method METHODNAME 
            
            if VALUELIST does not match the expectation, an error
            testlinkerrors.TLArgError is raised             """
            
        if not methodName in self._positionalArgNames:
            new_msg = '%s - missing positional args configuration' %\
            (methodName)
            raise testlinkerrors.TLArgError(new_msg)
            
        nameList = self._positionalArgNames[methodName]
        length_NameList = len(nameList)
        length_ValueList = len(valueList)
        
        if length_NameList != length_ValueList:
            new_msg = '%s - mismatching number of positional args %i vs %i' %\
            (methodName, length_NameList, length_ValueList)
            new_msg = '%s\n expected args: %s' % (new_msg, ', '.join(nameList))
            raise testlinkerrors.TLArgError(new_msg)
        return {nameList[x] : valueList[x] for x in range(len(nameList)) }
    
    def _getAttachmentArgs(self, attachmentfile):
        """ returns dictionary with key/value pairs needed, to transfer 
            ATTACHMENTFILE via the api to into TL
            ATTACHMENTFILE: python file descriptor pointing to the file """
        import mimetypes
        import base64
        import os.path
        return {'filename':os.path.basename(attachmentfile.name),
                'filetype':mimetypes.guess_type(attachmentfile.name)[0],
                'content':base64.encodestring(attachmentfile.read())
                }

    
    def _checkResponse(self, response, methodNameAPI, argsOptional):
        """ Checks if RESPONSE is empty or includes Error Messages
            Will raise TLRepsonseError in this case """
        if response:
            try:
                if 'code' in response[0]:
                    raise testlinkerrors.TLResponseError(
                                    methodNameAPI, argsOptional,
                                    response[0]['message'], response[0]['code'])
            except (TypeError, KeyError):
                # if the reponse has not a [{..}] structure, the check
                #    'code' in response[0]
                # raise an error. Following causes are ok
                # TypeError: raised from doesUserExist, cause the postiv 
                #            response is simply 'True'
                # KeyError: raise from uploadExecutionAttachment, cause the 
                #           positiv response is directly a dictionary
                pass
        else:
            raise testlinkerrors.TLResponseError(methodNameAPI, argsOptional,
                                                 'Empty Response! ')
            
            
        
            
    
    #
    #  ADDITIONNAL FUNCTIONS
    #                                   


    def __str__(self):
        message = """
Testlink API - class %s - version %s
@authors: %s

Current connection settings
 Server URL: %s
 DevKey    : %s
"""
        return message % (self.__class__.__name__, self.__version__, 
                          self.__author__, self._server_url, self.devKey)

    
if __name__ == "__main__":
    tl_helper = TestLinkHelper()
    tl_helper.setParamsFromArgs()
    myTestLink = tl_helper.connect(TestlinkAPIGeneric)
    print myTestLink
    print myTestLink.about()



