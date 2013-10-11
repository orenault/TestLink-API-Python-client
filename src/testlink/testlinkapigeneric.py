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

from testlinkhelper import TestLinkHelper, VERSION
import testlinkerrors


# Default Definition which (python) API-Method expects which postional arguments
# this must not be equal to mandatory params of the (php) xmlrpc Methods
# it defines argumenst, which values must be passed without explicit names
# to the API-Method
# this is stored during the init in ._positionalArgNames
# subclasses could override this definition, if there (python) method should
# work with different positional arguments
positionalArgNamesDefault = {
            'repeat' : ['str'],
            'createTestProject' : ['testprojectname', 'testcaseprefix'],
            'doesUserExist' : ['user']
}

# decorators for generic api calls
# see http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python

def decoApiCallWithoutArgs(methodAPI):
    """ Decorator for calling server methods without arguments """  
    def wrapper(self):
#        print methodAPI.__name__
        return self.callServerWithPosArgs(methodAPI.__name__)
    return wrapper

def decoApiCallWithArgs(methodAPI):
    """ Decorator for calling server methods with arguments """  
    def wrapper(self, *argsPositional, **argsOptional):
        return self.callServerWithPosArgs(methodAPI.__name__, 
                                          *argsPositional, **argsOptional)
    return wrapper

def decoApiCallAddDevKey(methodAPI):
    """ Decorator to expand parameter list with devKey"""  
    def wrapper(self, *argsPositional, **argsOptional):
        if not ('devKey' in argsOptional):
            argsOptional['devKey'] = self.devKey
#        print argsAPI
        return methodAPI(self, *argsPositional, **argsOptional)
    return wrapper


class TestlinkAPIGeneric(object):    
    
    __slots__ = ['server', 'devKey', '_server_url', '_positionalArgNames']
 
    __VERSION__ = VERSION
    
    def __init__(self, server_url, devKey):
        self.server = xmlrpclib.Server(server_url)
        self.devKey = devKey
        self._server_url = server_url
        self._positionalArgNames = positionalArgNamesDefault.copy()
        
        
        
    # GENERIC API CALLS - using decorators
    # http://stackoverflow.com/questions/1015307/python-bind-an-unbound-method
    
    @decoApiCallWithoutArgs
    def sayHello(self):
        """ sayHello: Lets you see if the server is up and running
        positional args: ---
        optional args : --- """

    def ping(self):
        """ alias for methodAPI sayHello """ 
        return self.sayHello()
    
    @decoApiCallWithArgs
    def repeat(self):
        """ repeat: Repeats a message back
        positional args: str
        optional args : --- """
    
    @decoApiCallWithoutArgs
    def about(self):
        """ about: Gives basic information about the API
        positional args: ---
        optional args : --- """

#    * Creates a new build for a specific test plan
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testplanid"]
#    * @param string $args["buildname"];
#    * @param string $args["buildnotes"];
#    * @return mixed $resultInfo
#   public function createBuild($args)

    @decoApiCallAddDevKey               
    @decoApiCallWithArgs
    def getProjects(self):
        """ getProjects: Gets a list of all projects
        positional args: ---
        optional args : --- """

#    * Gets a list of test plans within a project
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testprojectid"]
#    * @return mixed $resultInfo
#   public function getBuildsForTestPlan($args)

#    * List test suites within a test plan alphabetically
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testplanid"]
#    * @return mixed $resultInfo
#    */
#    public function getTestSuitesForTestPlan($args)
        
#    * create a test project
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param string $args["testprojectname"]
#    * @param string $args["testcaseprefix"]
#    * @param string $args["notes"] OPTIONAL
#    * @param map $args["options"] OPTIONAL ALL int treated as boolean
#    *        keys  requirementsEnabled,testPriorityEnabled,automationEnabled,inventoryEnabled
#    *
#    * @param int $args["active"]  OPTIONAL
#      * @param int $args["public"]  OPTIONAL
#      *   
#    * @return mixed $resultInfo
#    */
#   public function createTestProject($args)

    @decoApiCallAddDevKey               
    @decoApiCallWithArgs
    def createTestProject(self):
        """ createTestProject : Create a test project  
        positional args: testprojectname, testcaseprefix
        optional args : notes,  active, public, options
        
        options : dictionary with keys
                    requirementsEnabled, testPriorityEnabled, 
                    automationEnabled,inventoryEnabled
                 and values 0 (false) and 1 (true)     """
        
#   /**
#    * List test cases within a test suite
#    * 
#    * By default test cases that are contained within child suites 
#    * will be returned. 
#    * Set the deep flag to false if you only want test cases in the test suite provided 
#    * and no child test cases.
#    *  
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testsuiteid"]
#    * @param boolean $args["deep"] - optional (default is true)
#    * @param boolean $args["details"] - optional (default is simple)
#    *                                use full if you want to get 
#    *                                summary,steps & expected_results
#    *
#    * @return mixed $resultInfo
#    *
#    *
#    */
#    public function getTestCasesForTestSuite($args)

#   /**
#   * Find a test case by its name
#   * 
#   * <b>Searching is case sensitive.</b> The test case will only be returned if there is a definite match.
#   * If possible also pass the string for the test suite name. 
#   *
#   * No results will be returned if there are test cases with the same name that match the criteria provided.  
#   * 
#   * @param struct $args
#   * @param string $args["devKey"]
#   * @param string $args["testcasename"]
#   * @param string $args["testsuitename"] - optional
#   * @param string $args["testprojectname"] - optional
#   * @param string $args["testcasepathname"] - optional
#   *               Full test case path name, starts with test project name
#   *               pieces separator -> :: -> default value of getByPathName()
#   * @return mixed $resultInfo
#   */
#   public function getTestCaseIDByName($args)

#    /**
#       * createTestCase
#       * @param struct $args
#       * @param string $args["devKey"]
#       * @param string $args["testcasename"]
#       * @param int    $args["testsuiteid"]: test case parent test suite id
#       * @param int    $args["testprojectid"]: test case parent test suite id
#       *
#       * @param string $args["authorlogin"]: to set test case author
#       * @param string $args["summary"]
#       * @param array  $args["steps"]
#       *
#       * @param string $args["preconditions"] - optional
#       * @param int    $args["importance"] - optional - see const.inc.php for domain
#       * @param int    $args["execution"] - optional - see ... for domain
#       * @param int    $args["order'] - optional
#       * @param int    $args["internalid"] - optional - do not use
#       * @param string $args["checkduplicatedname"] - optional
#       * @param string $args["actiononduplicatedname"] - optional
#       *
#       * @return mixed $resultInfo
#       * @return string $resultInfo['operation'] - verbose operation
#       * @return boolean $resultInfo['status'] - verbose operation
#       * @return int $resultInfo['id'] - test case internal ID (Database ID)
#       * @return mixed $resultInfo['additionalInfo'] 
#       * @return int $resultInfo['additionalInfo']['id'] same as $resultInfo['id']
#       * @return int $resultInfo['additionalInfo']['external_id'] without prefix
#       * @return int $resultInfo['additionalInfo']['status_ok'] 1/0
#       * @return string $resultInfo['additionalInfo']['msg'] - for debug 
#       * @return string $resultInfo['additionalInfo']['new_name'] only present if new name generation was needed
#       * @return int $resultInfo['additionalInfo']['version_number']
#       * @return boolean $resultInfo['additionalInfo']['has_duplicate'] - for debug 
#       * @return string $resultInfo['message'] operation message
#       */
#    public function createTestCase($args)

#    /**
#    * Reports a result for a single test case
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testcaseid"]: optional, if not present           
#      *                                 testcaseexternalid must be present
#      *
#      * @param int $args["testcaseexternalid"]: optional, if does not is present           
#      *                                         testcaseid must be present
#      *
#    *
#    *
#    * @param int $args["testplanid"] 
#      * @param string $args["status"] - status is {@link $validStatusList}
#    * @param int $args["buildid"] - optional.
#    *                               if not present and $args["buildname"] exists
#    *                               then 
#    *                                    $args["buildname"] will be checked and used if valid
#    *                               else 
#    *                                    build with HIGHEST ID will be used
#    *
#    * @param int $args["buildname"] - optional.
#    *                               if not present Build with higher internal ID will be used
#    *
#      *
#    * @param string $args["notes"] - optional
#    * @param bool $args["guess"] - optional defining whether to guess optinal params or require them 
#    *                               explicitly default is true (guess by default)
#    *
#    * @param string $args["bugid"] - optional
#      *
#      * @param string $args["platformid"] - optional, if not present platformname must be present
#    * @param string $args["platformname"] - optional, if not present platformid must be present
#      *    
#      *
#      * @param string $args["customfields"] - optional
#      *               contains an map with key:Custom Field Name, value: value for CF.
#      *               VERY IMPORTANT: value must be formatted in the way it's written to db,
#      *               this is important for types like:
#      *
#      *               DATE: strtotime()
#      *               DATETIME: mktime()
#      *               MULTISELECTION LIST / CHECKBOX / RADIO: se multipli selezione ! come separatore
#      *
#      *
#      *               these custom fields must be configured to be writte during execution.
#      *               If custom field do not meet condition value will not be written
#      *
#      * @param boolean $args["overwrite"] - optional, if present and true, then last execution
#      *                for (testcase,testplan,build,platform) will be overwritten.            
#      *
#    * @return mixed $resultInfo 
#    *         [status]  => true/false of success
#    *         [id]      => result id or error code
#    *         [message]  => optional message for error message string
#    * @access public
#    *
#    * @internal revisions
#    * 20101208 - franciscom - BUGID 4082 - no check on overwrite value
#    *
#    */
#   public function reportTCResult($args)

#   /**
#    * turn on/off testMode
#    *
#    * This method is meant primarily for testing and debugging during development
#    * @param struct $args
#    * @return boolean
#    * @access protected
#    */  
#   public function setTestMode($args)

#   /**
#    * getTestCasesForTestPlan
#    * List test cases linked to a test plan
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testplanid"]
#    * @param int $args["testcaseid"] - optional
#    * @param int $args["buildid"] - optional
#    * @param int $args["keywordid"] - optional mutual exclusive with $args["keywords"]
#    * @param int $args["keywords"] - optional  mutual exclusive with $args["keywordid"]
#    *
#    * @param boolean $args["executed"] - optional
#    * @param int $args["$assignedto"] - optional
#    * @param string $args["executestatus"] - optional
#    * @param array $args["executiontype"] - optional
#    * @param array $args["getstepinfo"] - optional - default false
#    * @param string $args["details"] - optional 
#    *                  'full': (default) get summary,steps,expected_results,test suite name
#    *                   'simple':
#    *                   'details':
#    * @return mixed $resultInfo
#    *
#    * @internal revisions
#    * @since 1.9.4
#    * 20111226 - franciscom - TICKET 4843: 'getTestCasesForTestPlan' - add support for new argument 'details'
#    */
# public function getTestCasesForTestPlan($args)

#   /**
#    * Gets value of a Custom Field with scope='design' for a given Test case
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["testcaseexternalid"]:  
#    * @param string $args["version"]: version number  
#    * @param string $args["testprojectid"]: 
#    * @param string $args["customfieldname"]: custom field name
#    * @param string $args["details"] optional, changes output information
#    *                                null or 'value' => just value
#    *                                'full' => a map with all custom field definition
#    *                                             plus value and internal test case id
#    *                                'simple' => value plus custom field name, label, and type (as code).
#      *
#      * @return mixed $resultInfo
#    *         
#    * @access public
#    */    
#   public function getTestCaseCustomFieldDesignValue($args)

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

#    /**
#     * get set of test suites AT TOP LEVEL of tree on a Test Project
#     *
#     * @param args['testprojectid']
#     *  
#     * @return array
#     *
#     */
#    public function getFirstLevelTestSuitesForTestProject($args)

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

# /**
#  * Gets attachments for specified test case.
#  * The attachment file content is Base64 encoded. To save the file to disk in client,
#  * Base64 decode the content and write file in binary mode. 
#  * 
#  * @param struct $args
#  * @param string $args["devKey"] Developer key
#  * @param int $args["testcaseid"]: optional, if does not is present           
#  *                                 testcaseexternalid must be present
#  *
#  * @param int $args["testcaseexternalid"]: optional, if does not is present           
#  *                                         testcaseid must be present
#  * 
#  * @return mixed $resultInfo
#  */
# public function getTestCaseAttachments($args)

#     /**
#    * create a test suite
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testprojectid"]
#    * @param string $args["testsuitename"]
#    * @param string $args["details"]
#    * @param int $args["parentid"] optional, if do not provided means test suite must be top level.
#    * @param int $args["order"] optional. Order inside parent container
#    * @param int $args["checkduplicatedname"] optional, default true.
#    *                                          will check if there are siblings with same name.
#      *
#      * @param int $args["actiononduplicatedname"] optional
#      *                                            applicable only if $args["checkduplicatedname"]=true
#    *                                            what to do if already a sibling exists with same name.
#    *   
#    * @return mixed $resultInfo
#    */
#     public function createTestSuite($args)

#     /**
#      * Gets info about target test project
#      *
#      * @param struct $args
#      * @param string $args["devKey"]
#      * @param string $args["testprojectname"]     
#      * @return mixed $resultInfo      
#      * @access public
#      */    
#     public function getTestProjectByName($args)

#     /**
#      * Gets info about target test project
#      *
#      * @param struct $args
#      * @param string $args["devKey"]
#      * @param string $args["testprojectname"]     
#      * @param string $args["testplanname"]     
#      * @return mixed $resultInfo      
#      * @access public
#      */    
#     public function getTestPlanByName($args)

# /**
# * get test case specification using external ir internal id
# * 
# * @param struct $args
# * @param string $args["devKey"]
# * @param int $args["testcaseid"]: optional, if does not is present           
# *                                 testcaseexternalid must be present
# *
# * @param int $args["testcaseexternalid"]: optional, if does not is present           
# *                                         testcaseid must be present
# * @param int $args["version"]: optional, if does not is present max version number will be
# *                                        retuned
# *
# * @return mixed $resultInfo
# */
# public function getTestCase($args)

#   /**
#    * create a test plan
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testplanname"]
#    * @param int $args["testprojectname"]
#    * @param string $args["notes"], optional
#    * @param string $args["active"], optional default value 1
#    * @param string $args["public"], optional default value 1
#      *   
#    * @return mixed $resultInfo
#    * @internal revision
#    *  20100704 - franciscom - BUGID 3565
#    */
#   public function createTestPlan($args)

#   /**
#    * Gets full path from the given node till the top using nodes_hierarchy_table
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param mixed $args["nodeID"] can be just a single node or an array of INTERNAL (DB) ID
#    * @return mixed $resultInfo      
#    * @access public
#    *
#    * @internal revision
#    * BUGID 3993
#    * $args["nodeID"] can be just a single node or an array
#    * when path can not be found same date structure will be returned, that on situations
#    * where all is ok, but content for KEY(nodeID) will be NULL instead of rising ERROR  
#    *
#    */    
#   public function getFullPath($args)

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

#    /**
#      * Return a TestSuite by ID
#      *
#      * @param
#      * @param struct $args
#      * @param string $args["devKey"]
#      * @param int $args["testsuiteid"]
#      * @return mixed $resultInfo
#      * 
#      * @access public
#      */
#     public function getTestSuiteByID($args)

#   /**
#    * get list of TestSuites which are DIRECT children of a given TestSuite
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testsuiteid"]
#    * @return mixed $resultInfo
#    *
#    * @access public
#    */
#   public function getTestSuitesForTestSuite($args)

#   /**
#      * Returns the list of platforms associated to a given test plan
#      *
#      * @param
#      * @param struct $args
#      * @param string $args["devKey"]
#      * @param int $args["testplanid"]
#      * @return mixed $resultInfo
#      * 
#      * @access public
#      */
#   public function getTestPlanPlatforms($args)

#   /**
#    * Gets the summarized results grouped by platform.
#    * @see 
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["tplanid"] test plan id
#    *
#    * @return map where every element has:
#    *
#    *  'type' => 'platform'
#    *  'total_tc => ZZ
#    *  'details' => array ( 'passed' => array( 'qty' => X)
#    *                       'failed' => array( 'qty' => Y)
#    *                       'blocked' => array( 'qty' => U)
#    *                       ....)
#    *
#    * @access public
#    */
#   public function getTotalsForTestPlan($args)


    @decoApiCallWithArgs
    def doesUserExist(self):
        """ doesUserExist : Checks if user name exists 
        positional args: user
        optional args : --- 
        returns true if everything OK, otherwise error structure """
               
    @decoApiCallAddDevKey               
    @decoApiCallWithArgs
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

# /**
#  * Uploads an attachment for an execution.
#  * 
#  * The attachment content must be Base64 encoded by the client before sending it.
#  * 
#  * @param struct $args
#  * @param string $args["devKey"] Developer key
#  * @param int $args["executionid"] execution ID
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
# public function uploadExecutionAttachment($args)

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
        return self._callServer(methodNameAPI, argsOptional)

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
            testlinkerrors.TLParamError is raised             """
            
        if not methodName in self._positionalArgNames:
            new_msg = '%s - missing positional args configurtion' %\
            (methodName)
            raise testlinkerrors.TLParamError(new_msg)
            
        nameList = self._positionalArgNames[methodName]
        length_NameList = len(nameList)
        length_ValueList = len(valueList)
        
        if length_NameList != length_ValueList:
            new_msg = '%s - mismatching number of positional args %i vs %i' %\
            (methodName, length_NameList, length_ValueList)
            raise testlinkerrors.TLParamError(new_msg)
        return {nameList[x] : valueList[x] for x in range(len(nameList)) }
            
    
    #
    #  ADDITIONNAL FUNCTIONS
    #                                   


    def __str__(self):
        message = """
Testlink API - class %s - version %s
@author: Olivier Renault, James Stock, TestLink-API-Python-client developers
"""
        return message % (self.__class__.__name__, self.__VERSION__)

    
if __name__ == "__main__":
    tl_helper = TestLinkHelper()
    tl_helper.setParamsFromArgs()
    myTestLink = tl_helper.connect(TestlinkAPIGeneric)
    print myTestLink
    print myTestLink.about()



