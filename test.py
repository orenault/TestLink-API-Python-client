#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import TestLinkAPI
from nose.tools import *

class TestClass():
    def setUp(self):
        """Initialisation
        """

        SERVEUR_URL = "http://localhost/testlink/lib/api/xmlrpc.php"
        KEY = "7ec252ab966ce88fd92c25d08635672b"
        self.client = TestLinkAPI.TestLinkAPIClient(server_url=SERVEUR_URL, devKey=KEY)

    def test_getTestCaseIDByName(self):
        """ getTestCaseIDByName test
        """
        (val, message) = self.client.getTestCaseIDByName("Fin de programme", "Séquence 2", "Test 2")
        assert_equal(message, None )
        (val, message) = self.client.getTestCaseIDByName("Initialisation", "Séquence 1", "Test 2")
        assert_equal(message, "(getTestCaseIDByName) - Several case test found. Suite name must not be duplicate for the same project") 

    def test___str__(self):
        """ __str__ test
        Check that return is a string that contains the version number
        """

        message = self.client.__str__()
        assert_not_equal(re.search(self.client.__VERSION__, message), None) 


