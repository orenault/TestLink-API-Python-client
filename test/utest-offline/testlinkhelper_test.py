#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012-2017 Luiko Czub, TestLink-API-Python-client developers
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
import os
import sys


from testlink import TestLinkHelper


class DummyTestLinkAPI(object):
    """ Dummy for Simulation TestLinkAPICLient. 
    Used for init() tests with TestLinkHelper.connect(api_class)
    """
    
    def __init__(self, server_url, devKey, **args):
        self.server = server_url
        self.devKey = devKey
        self.args   = args

class TestLinkHelperTestCase(unittest.TestCase):
    """ TestCases for TestLinkHelper """
    
    CLASSUNDERTEST = TestLinkHelper
    ENVNAMES = ['TESTLINK_API_PYTHON_SERVER_URL', 'TESTLINK_API_PYTHON_DEVKEY', 
                'http_proxy']
    EXPECTED_DEFAULTS = ['http://localhost/testlink/lib/api/xmlrpc.php', '42',
                         '']

    def setEnviron(self, envname, envvalue ):
        """ manipulates os.environ - stores os.environ[envname] = envvalue """
        if envvalue is None:
            # UNSET environment variable
            if envname in os.environ:
                os.environ.pop(envname)
        else:
            os.environ[envname] = envvalue

    def setUp(self):
        """ backup TestLinkHelper related environment variables """
        self.backup = {}
        for envname in self.ENVNAMES:
            self.backup[envname] = os.getenv(envname)

    def tearDown(self):
        """ restore TestLinkHelper related environment variables """
        for envname in self.ENVNAMES:
            self.setEnviron(envname, self.backup[envname])
           
    def test_init_Env(self):
        """ init TestLinkHelper with environment variables """
        self.check_init_env((None, None, None), self.EXPECTED_DEFAULTS)
        self.check_init_env(('SERVER-URL-1', None, None), 
                            ('SERVER-URL-1', self.EXPECTED_DEFAULTS[1], 
                             self.EXPECTED_DEFAULTS[2]))
        self.check_init_env((None, 'DEVKEY-2', None), 
                            (self.EXPECTED_DEFAULTS[0], 'DEVKEY-2',
                             self.EXPECTED_DEFAULTS[2]))
        self.check_init_env(('SERVER-URL-3', 'DEVKEY-3', None), 
                            ('SERVER-URL-3', 'DEVKEY-3', self.EXPECTED_DEFAULTS[2]))
        self.check_init_env((None, None, 'Proxy-4'), 
                            (self.EXPECTED_DEFAULTS[0], self.EXPECTED_DEFAULTS[1],
                             'Proxy-4'))
        self.check_init_env(('SERVER-URL-5', 'DEVKEY-5', 'Proxy-5'), 
                            ('SERVER-URL-5', 'DEVKEY-5', 'Proxy-5'))
            
    def check_init_env(self, env_values, expectations ):
        # set TestLinkHelper related environment variables
        self.setEnviron(self.ENVNAMES[0], env_values[0])
        self.setEnviron(self.ENVNAMES[1], env_values[1])
        self.setEnviron(self.ENVNAMES[2], env_values[2])
        # init helper without method params
        a_helper = self.CLASSUNDERTEST()
        self.assertEqual(expectations[0], a_helper._server_url)
        self.assertEqual(expectations[1], a_helper._devkey)
        self.assertEqual(expectations[2], a_helper._proxy)
        
    def test_init_params(self):
        """ init TestLinkHelper with method parameter and no env variables """
        self.check_init_params(('SERVER-URL-11', None, None), 
                               ('SERVER-URL-11', self.EXPECTED_DEFAULTS[1],
                                self.EXPECTED_DEFAULTS[2]))
        self.check_init_params((None, 'DEVKEY-12', None), 
                               (self.EXPECTED_DEFAULTS[0], 'DEVKEY-12', 
                                self.EXPECTED_DEFAULTS[2]))
        self.check_init_params(('SERVER-URL-13', 'DEVKEY-13', None), 
                               ('SERVER-URL-13', 'DEVKEY-13', self.EXPECTED_DEFAULTS[2]))
        self.check_init_params((None, None, 'Proxy-14'), 
                               (self.EXPECTED_DEFAULTS[0], self.EXPECTED_DEFAULTS[1],
                                'Proxy-14'))
        self.check_init_params(('SERVER-URL-15', 'DEVKEY-15', 'Proxy-15'), 
                               ('SERVER-URL-15', 'DEVKEY-15', 'Proxy-15'))

    def check_init_params(self, param_values, expectations ):
        # unset TestLinkHelper related environment variables
        self.setEnviron(self.ENVNAMES[0], None)
        self.setEnviron(self.ENVNAMES[1], None)
        self.setEnviron(self.ENVNAMES[2], None)
        # init helper with method params
        a_helper = self.CLASSUNDERTEST(param_values[0], param_values[1], param_values[2])
        self.assertEqual(expectations[0], a_helper._server_url)
        self.assertEqual(expectations[1], a_helper._devkey)
        self.assertEqual(expectations[2], a_helper._proxy)

    def test_init_env_params(self):
        """ init TestLinkHelper with mixed method parameter and env variables """
        # set TestLinkHelper related environment variables
        self.setEnviron(self.ENVNAMES[0], 'SERVER-URL-21')
        self.setEnviron(self.ENVNAMES[1], 'DEVKEY-21')
        self.setEnviron(self.ENVNAMES[2], 'PROXY-21')
        # init helper with method params
        a_helper = self.CLASSUNDERTEST('SERVER-URL-22', 'DEVKEY-22', 'PROXY-22')
        # the method params have a high priority than the environment variables
        self.assertEqual('SERVER-URL-22', a_helper._server_url)
        self.assertEqual('DEVKEY-22', a_helper._devkey)
        self.assertEqual('PROXY-22', a_helper._proxy)
        

    def test_createArgparser(self):
        """ create TestLinkHelper command line argument parser """
        a_helper = self.CLASSUNDERTEST('SERVER-URL-31', 'DEVKEY-31', 'PROXY-31')
        a_parser = a_helper._createArgparser('DESCRIPTION-31')
        self.assertEqual('DESCRIPTION-31', a_parser.description)
        default_args=a_parser.parse_args('')
        self.assertEqual('SERVER-URL-31', default_args.server_url)
        self.assertEqual('DEVKEY-31', default_args.devKey)
        self.assertEqual('PROXY-31', default_args.proxy)
        
    def test_setParamsFromArgs(self):
        """ set TestLinkHelper params from command line arguments """
        a_helper = self.CLASSUNDERTEST()
        a_helper.setParamsFromArgs(None, ['--server_url', 'SERVER-URL-41', 
                                          '--devKey' , 'DEVKEY-41'])
        self.assertEqual('SERVER-URL-41', a_helper._server_url)
        self.assertEqual('DEVKEY-41', a_helper._devkey)
        
    def test_connect(self):
        """ create a TestLink API dummy """
        a_helper = self.CLASSUNDERTEST('SERVER-URL-51', 'DEVKEY-51')
        a_tl_api = a_helper.connect(DummyTestLinkAPI)
        self.assertEqual('SERVER-URL-51', a_tl_api.server)
        self.assertEqual('DEVKEY-51', a_tl_api.devKey)
        self.assertEqual({}, a_tl_api.args)
        
    def test_getProxiedTransport(self):
        """ create a ProxiedTransportTestLink API dummy """
        a_helper = self.CLASSUNDERTEST('SERVER-URL-61', 'DEVKEY-61', 'PROXY-61')
                                       #'http://fast.proxy.com.de/')
        a_pt = a_helper._getProxiedTransport()
        self.assertEqual('ProxiedTransport', a_pt.__class__.__name__)
        self.assertEqual('PROXY-61', a_pt.proxy)
     
       
    def test_connect_with_proxy(self):
        """ create a TestLink API dummy with ProxiedTransport"""
        a_helper = self.CLASSUNDERTEST('SERVER-URL-71', 'DEVKEY-71', 'PROXY-71')
        a_tl_api = a_helper.connect(DummyTestLinkAPI)
        self.assertEqual('SERVER-URL-71', a_tl_api.server)
        self.assertEqual('DEVKEY-71', a_tl_api.devKey)
        self.assertEqual('PROXY-71', a_tl_api.args['transport'].proxy)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()