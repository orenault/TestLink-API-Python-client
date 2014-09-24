*** Settings ***
Library           TestlinkAPILibrary
Library           Collections

*** Variables ***

*** Test Cases ***
Init TestLinkAPIClient
    ${tlapi_client}=    Create Api Client    TestlinkAPIClient
    ${method_args}=    Call Method    ${tlapi_client}    whatArgs    repeat
    Should Contain    ${method_args}    Repeats a message back
    Should Be Equal As Strings    ${tlapi_client.__class__.__name__}    TestlinkAPIClient

Init TestlinkAPIGeneric
    ${tlapi_client}=    Create Api Client    TestlinkAPIGeneric
    ${method_args}=    Call Method    ${tlapi_client}    whatArgs    repeat
    Should Contain    ${method_args}    Repeats a message back
    Should Be Equal As Strings    ${tlapi_client.__class__.__name__}    TestlinkAPIGeneric

Test Call Api Method sayHello
    ${response}=    Call Api Method    sayHello
    Should Be Equal As Strings    ${response}    Hello!

Test Call Api Method repeat
    ${response}=    Call Api Method    repeat    Hugo
    Should Be Equal As Strings    ${response}    You said: Hugo

Test Call Api Method getTestCaseIDByName
    @{response1}=    Call Api Method    getTestCaseIDByName    TESTCASE_B
    Should Not Be Empty    ${response1}
    @{response2}=    Call Api Method    getTestCaseIDByName    TESTCASE_B    testprojectname=PROJECT_API_GENERIC-10
    Should Not Be Empty    ${response2}
