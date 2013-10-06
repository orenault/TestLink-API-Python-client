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

# decorators for generic api calls
# see http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python

def decoApiCallWithoutArgs(methodAPI):
    """ Decorator for calling server methods without arguments """  
    def wrapper(self):
#        print methodAPI.__name__
        return self._callServer(methodAPI.__name__)
    return wrapper

def decoApiCallWithArgs(methodAPI):
    """ Decorator for calling server methods with arguments """  
    def wrapper(self, **argsAPI):
#        print methodAPI.__name__, ' ', argsAPI 
        return self._callServer(methodAPI.__name__, argsAPI)
    return wrapper

def decoApiCallAddDevKey(methodAPI):
    """ Decorator to expand parameter list with devKey"""  
    def wrapper(self, **argsAPI):
        if not ('devKey' in argsAPI):
            argsAPI['devKey'] = self.devKey
#        print argsAPI
        return methodAPI(self, **argsAPI)
    return wrapper


class TestlinkAPIGeneric(object):    
    
    __slots__ = ['server', 'devKey', 'stepsList', '_server_url']
 
    __VERSION__ = VERSION

    def __init__(self, server_url, devKey):
        self.server = xmlrpclib.Server(server_url)
        self.devKey = devKey
        self.stepsList = []
        self._server_url = server_url
        
    def _callServer(self, methodAPI, argsAPI=None):
        """ call server method METHODAPI with error handling and returns the 
        responds """
        
        response = None
        try:
            if argsAPI is None:
                response = getattr(self.server.tl, methodAPI)()
            else:
                response = getattr(self.server.tl, methodAPI)(argsAPI)
        except (IOError, xmlrpclib.ProtocolError), msg:
            new_msg = 'problems connecting the TestLink Server %s\n%s' %\
            (self._server_url, msg) 
            raise testlinkerrors.TLConnectionError(new_msg)
        except xmlrpclib.Fault, msg:
            new_msg = 'problems calling the API method %s\n%s' %\
            (methodAPI, msg) 
            raise testlinkerrors.TLAPIError(new_msg)

        return response
        
    #
    # GENERIC API CALLS - using decorators
    # http://stackoverflow.com/questions/1015307/python-bind-an-unbound-method
    
    @decoApiCallWithoutArgs
    def about(self):
        """ about : Gives basic information about the API  """

    @decoApiCallWithoutArgs
    def ping(self):
        """ ping :   """
    
    @decoApiCallWithArgs
    def repeat(self, **argsAPI):
        """ echo : """
    
    @decoApiCallWithArgs
    def doesUserExist(self, **argsAPI):
        """ doesUserExist : Checks if a user name exists """
               
    @decoApiCallAddDevKey               
    @decoApiCallWithArgs
    def checkDevKey(self, **argsAPI):
        """ checkDevKey :  check if Developer Key exists """
        
    @decoApiCallAddDevKey               
    @decoApiCallWithArgs
    def getProjects(self, **argsAPI):
        """ getProjects: Gets a list of all projects """
        
    @decoApiCallAddDevKey               
    @decoApiCallWithArgs
    def createTestProject(self, **argsAPI):
        """ createTestProject : Create a test project  
            Mandatory parameters : testprojectname, testcaseprefix
            Optional parameters : notes, options, active, public
            Options: requirementsEnabled, testPriorityEnabled, 
                     automationEnabled, inventoryEnabled 
        """        
        
     
               
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



