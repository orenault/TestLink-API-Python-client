#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2013-2017 Luiko Czub, TestLink-API-Python-client developers
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

import sys

if sys.version_info[0] == 2 and sys.version_info[1] == 6:
    # py26 needs backport unittest2
    import unittest2 as unittest
else:
    import unittest

if sys.version_info[0] == 2 and sys.version_info[1] == 7:
    # py27 and py31 assertRaisesRegexp was renamed in py32 to assertRaisesRegex
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

from testlink.testlinkerrors import TLResponseError
from testlink.testlinkargs import registerMethod, getArgsForMethod
from testlink.testlinkdecorators import decoApiCallAddAttachment,\
decoApiCallAddDevKey, decoApiCallWithoutArgs, \
decoMakerApiCallReplaceTLResponseError, decoMakerApiCallWithArgs, \
decoMakerApiCallChangePosToOptArg




class testlinkdecoratorsTestCase(unittest.TestCase):
    """ TestCases for decorators, used by TestlinkAPIGeneric for build 
        TestLink API methodsServer.  """
        
    devKey = '007'
    def setUp(self):
        self.api = self
        
    def _getAttachmentArgs(self, attachmentfile):
        # simulation of TestlinkAPIGeneric._getAttachmentArgs()
        # needed in test_decoApiCallAddAttachment
        return {'filename': 'name %s' % attachmentfile,
                'filetype': 'type %s' % attachmentfile,
                'content' : 'content %s' % attachmentfile}

#     def tearDown(self):
#         pass

    def test_noWrapperName_decoApiCallWithoutArgs(self):
        " decorator test: original function name should be unchanged "
        
        @decoApiCallWithoutArgs
        def orig_funcname1(a_api):
            "orig doc string1"
            return 'noArgs'
        
        self.assertEqual('orig_funcname1', orig_funcname1.__name__)
        self.assertEqual('orig doc string1', orig_funcname1.__doc__)
        self.assertIn('testlinkdecorators_test', orig_funcname1.__module__)

    def test_decoApiCallWithArgs(self):
        " decorator test: positional and optional arguments should be registered "
        
        from testlink.testlinkargs import getMethodsWithPositionalArgs
        @decoMakerApiCallWithArgs(['Uno', 'due', 'tre'], ['quad'])
        def DummyMethod(a_api):
            "a dummy api method with 3 positional args and 1 optional arg"
            pass
        
        posArgs = getMethodsWithPositionalArgs()
        self.assertEqual(['Uno', 'due', 'tre'], posArgs['DummyMethod'])

    def test_noWrapperName_decoApiCallWithArgs(self):
        " decorator test: original function name should be unchanged "
        
        @decoMakerApiCallWithArgs()
        def orig_funcname2(a_api):
            "orig doc string2"
            return 'noArgs'
        
        self.assertEqual('orig_funcname2', orig_funcname2.__name__)
        self.assertEqual('orig doc string2', orig_funcname2.__doc__)
        self.assertIn('testlinkdecorators_test', orig_funcname2.__module__)

    def test_decoApiCallAddDevKey(self):
        " decorator test: argsOptional should be extended with devKey"
        
        registerMethod('a_func')
        @decoApiCallAddDevKey
        def a_func(a_api, *argsPositional, **argsOptional):
            return argsPositional, argsOptional
        
        # check method argument definition
        allArgs = getArgsForMethod('a_func')
        self.assertEqual((['devKey'], []), allArgs)
        # check call arguments
        response = a_func(self.api)
        self.assertEqual({'devKey' : self.api.devKey}, response[1])

    def test_noWrapperName_decoApiCallAddDevKey(self):
        " decorator test: original function name should be unchanged "
        
        registerMethod('orig_funcname3')
        @decoApiCallAddDevKey
        def orig_funcname3(a_api, *argsPositional, **argsOptional):
            "orig doc string3"
            return argsPositional, argsOptional
        
        self.assertEqual('orig_funcname3', orig_funcname3.__name__)
        self.assertEqual('orig doc string3', orig_funcname3.__doc__)
        self.assertIn('testlinkdecorators_test', orig_funcname3.__module__)
        
    def test_decoApiCallReplaceTLResponseError_NoCodeError(self):
        " decorator test: TLResponseError (code=None) should be handled "
        
        @decoMakerApiCallReplaceTLResponseError()
        def a_func(a_api, *argsPositional, **argsOptional):
            raise TLResponseError('DummyMethod', 
                                argsOptional, 'Empty Response! ')

        response = a_func(self.api)
        self.assertEqual([], response)
        
    def test_decoApiCallReplaceTLResponseError_CodeError(self):
        " decorator test: TLResponseError (code=777) should be raised "
        
        @decoMakerApiCallReplaceTLResponseError()
        def a_func(a_api, *argsPositional, **argsOptional):
            raise TLResponseError('DummyMethod', 
                                argsOptional, 'Empty Response! ', 777)

        with self.assertRaisesRegex(TLResponseError, '777.*Empty'):
            a_func(self.api)
        
    def test_decoApiCallReplaceTLResponseError_CodeErrorOk(self):
        " decorator test: TLResponseError (code=777) should be handled "
        
        @decoMakerApiCallReplaceTLResponseError(777)
        def a_func(a_api, *argsPositional, **argsOptional):
            raise TLResponseError('DummyMethod', 
                                argsOptional, 'Empty Response! ', 777)

        response = a_func(self.api)
        self.assertEqual([], response)

    def test_decoApiCallReplaceTLResponseError_NoError(self):
        " decorator test: response without TLResponseError should be passed "
        
        @decoMakerApiCallReplaceTLResponseError(777)
        def a_func(a_api, *argsPositional, **argsOptional):
            return argsOptional

        response = a_func(self.api, name='BigBird')
        self.assertEqual({'name' : 'BigBird'}, response)

    def test_decoApiCallReplaceTLResponseError_replaceValue(self):
        " decorator test: TLResponseError should be replaced with {}"
        
        @decoMakerApiCallReplaceTLResponseError(replaceValue={})
        def a_func(a_api, *argsPositional, **argsOptional):
            raise TLResponseError('DummyMethod', 
                                argsOptional, 'Empty Response! ')

        response = a_func(self.api)
        self.assertEqual({}, response)

    def test_noWrapperName_decoApiCallReplaceTLResponseError(self):
        " decorator test: original function name should be unchanged "
        
        @decoMakerApiCallReplaceTLResponseError()
        def orig_funcname4(a_api, *argsPositional, **argsOptional):
            "orig doc string4"
            return argsPositional, argsOptional
        
        self.assertEqual('orig_funcname4', orig_funcname4.__name__)
        self.assertEqual('orig doc string4', orig_funcname4.__doc__)
        self.assertIn('testlinkdecorators_test', orig_funcname4.__module__)
        
    def test_decoApiCallAddAttachment(self):
        " decorator test: argsOptional should be extended attachment file infos"
        
        registerMethod('func_addAttachment')
        @decoApiCallAddAttachment
        def func_addAttachment(a_api, *argsPositional, **argsOptional):
            return argsPositional, argsOptional
        
        # check method argument definition
        allArgs = getArgsForMethod('func_addAttachment')
        self.assertEqual((['devKey'], ['attachmentfile']), allArgs)
        # check call arguments
        response = func_addAttachment(self.api, 'a_file')
        self.assertEqual({'devKey' : self.api.devKey, 'filename': 'name a_file',
                    'filetype': 'type a_file', 'content' : 'content a_file'}, 
                         response[1])
        
    def test_noWrapperName_decoApiCallAddAttachment(self):
        " decorator test: original function name should be unchanged "
        
        registerMethod('orig_funcname5')
        @decoApiCallAddAttachment
        def orig_funcname5(a_api):
            "orig doc string5"
            return 'noArgs'
        
        self.assertEqual('orig_funcname5', orig_funcname5.__name__)
        self.assertEqual('orig doc string5', orig_funcname5.__doc__)
        self.assertIn('testlinkdecorators_test', orig_funcname5.__module__)
        
    def test_noWrapperName_decoApiCallChangePosToOptArg(self):
        " decorator test: original function name should be unchanged "
        
        @decoMakerApiCallChangePosToOptArg(2, 'optArgName')
        def orig_funcname6(*argsPositional, **argsOptional):
            "orig doc string6"
            return argsPositional, argsOptional
        
        self.assertEqual('orig_funcname6', orig_funcname6.__name__)
        self.assertEqual('orig doc string6', orig_funcname6.__doc__)
        self.assertIn('testlinkdecorators_test', orig_funcname6.__module__)
        
    def test_decoApiCallChangePosToOptArg_posArg2(self):
        " decorator test:  change  posArg 2"
        
        @decoMakerApiCallChangePosToOptArg(2, 'due')
        def a_func(a_api, *argsPositional, **argsOptional):
            return argsPositional, argsOptional

        #'Uno', 'due', 'tre', 'quad',  'cinque'
        # 2 posArgs 2optArgs -> 1posArg, 3optArg
        (posArgs, optArgs) = a_func(self.api, 1, 2, tre = 3, quad = 4 )
        self.assertEqual((1,), posArgs)
        self.assertEqual({'due' : 2, 'tre' : 3, 'quad' : 4 }, optArgs)

        # 3 posArgs 2optArgs -> 2posArg, 2optArg
        (posArgs, optArgs) = a_func(self.api, 1, 2, 3, quad = 4 , due = 5)
        self.assertEqual((1,3), posArgs)
        self.assertEqual({'due' : 2, 'quad' : 4 }, optArgs)

        # 1 posArgs 2optArgs -> 1posArg, 2optArg
        (posArgs, optArgs) = a_func(self.api, 1, due = 2, tre = 3)
        self.assertEqual((1,), posArgs)
        self.assertEqual({'due' : 2, 'tre' : 3 }, optArgs)

        # 0 posArgs 2optArgs -> 0posArg, 2optArg
        (posArgs, optArgs) = a_func(self.api, uno = 1, due = 2)
        self.assertEqual( (), posArgs)
        self.assertEqual({'uno' : 1, 'due' :2}, optArgs)

    def test_decoApiCallChangePosToOptArg_posArg3(self):
        " decorator test:  change  posArg 3"
        
        @decoMakerApiCallChangePosToOptArg(3, 'tre')
        def a_func(a_api, *argsPositional, **argsOptional):
            return argsPositional, argsOptional

        # 3 posArgs 0optArgs -> 2posArg, 1optArg
        (posArgs, optArgs) = a_func(self.api, 1, 2, 3 )
        self.assertEqual((1,2), posArgs)
        self.assertEqual({'tre' : 3}, optArgs)

        # 2 posArgs 0optArgs -> 2posArg, 0optArg
        (posArgs, optArgs) = a_func(self.api, 1, 2 )
        self.assertEqual((1,2), posArgs)
        self.assertEqual({}, optArgs)

    def test_decoApiCallChangePosToOptArg_posArgNeg1(self):
        " decorator test:  change  posArg -1"
        
        @decoMakerApiCallChangePosToOptArg(-1, 'last')
        def a_func(a_api, *argsPositional, **argsOptional):
            return argsPositional, argsOptional

        # 3 posArgs 0optArgs -> 2posArg, 1optArg
        (posArgs, optArgs) = a_func(self.api, 1, 2, 3 )
        self.assertEqual((1,2,3), posArgs)
        self.assertEqual({}, optArgs)

        # 1 posArgs 0optArgs -> 0posArg, 1optArg
        (posArgs, optArgs) = a_func(self.api, 1 )
        self.assertEqual((1,), posArgs)
        self.assertEqual({}, optArgs)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()