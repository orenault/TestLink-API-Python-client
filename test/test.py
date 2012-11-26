#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2011-2012 pade (Patrick Dassier), TestLink-API-Python-client developers
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

'''
 Source file
 File name: test.py
 Creation date: 04-10-2012
 Author: dassier

'''

'''
Fichier de test pour le module "TestLinkAPI.py"
'''

import re
from testlink import TestLink, TestLinkError, TestLinkHelper
from nose.tools import *

class TestClass():
    def setUp(self):
        """Initialisation
        """

        # precondition - SERVEUR_URL and KEY are defined in environment
        # TESTLINK_API_PYTHON_SERVER_URL=http://localhost/testlink/lib/api/xmlrpc.php
        # TESTLINK_API_PYTHON_DEVKEY=7ec252ab966ce88fd92c25d08635672b
        self.client = TestLinkHelper().connect(TestLink)

    def test_getTestCaseIDByName(self):
        """ getTestCaseIDByName test
        """
        val = self.client.getTestCaseIDByName("Fin de programme", "Séquence 2", "Test 2")
        # 31 is test case id
        assert_equal(val, '31' )

        # Check if an error is raised in case of bad parameters
        assert_raises(TestLinkError, self.client.getTestCaseIDByName, "Initialisation", "Séquence 1", "Test 2")

    def test_getTestProjectByName(self):
        project = self.client.getTestProjectByName("Test 2")
        assert_equals(type(project), dict)
        # Check if an error is raised in case of bad parameters
        assert_raises(TestLinkError, self.client.getTestProjectByName, "Unknown project")

    def test_getTestPlanByName(self):
        plan_ok = self.client.getTestPlanByName("Test 2", "Full")

        # Assume that plan id is 33
        assert_equal(plan_ok['id'], '33')

        assert_raises(TestLinkError, self.client.getTestPlanByName, "Test 2", "Name Error")

    def test_getBuildByName(self):
        pass

    def test_reportResult(self):
        dico = {'testProjectName': 'Automatique',
                'testPlanName': 'FullAuto',
                'buildName': 'V0.1'}
        execid = self.client.reportResult("p", "test1", "S1", "An example of note", **dico)
        assert_equal(type(execid), str)

        execid = self.client.reportResult("f", "test2", "S1", **dico)
        assert_equal(type(execid), str)

