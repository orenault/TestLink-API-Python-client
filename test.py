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
from testlink import TestLink, TestLinkErrors
from nose.tools import *

class TestClass():
    def setUp(self):
        """Initialisation
        """

        SERVEUR_URL = "http://localhost/testlink/lib/api/xmlrpc.php"
        KEY = "7ec252ab966ce88fd92c25d08635672b"
        self.client = TestLink(server_url=SERVEUR_URL, key=KEY)

    def test_getTestCaseIDByName(self):
        """ getTestCaseIDByName test
        """
        val = self.client.getTestCaseIDByName("Fin de programme", "Séquence 2", "Test 2")
        # 31 is test case id
        assert_equal(val, '31' )

        try:
            val = self.client.getTestCaseIDByName("Initialisation", "Séquence 1", "Test 2")
        except TestLinkErrors, e:
            assert_equal(str(e), "(getTestCaseIDByName) - Several case test found. Suite name must not be duplicate for the same project") 
        else:
            print "An error message is expected !"
            assert_equal(False, True)

