*** Settings ***
Documentation     Simple smoke tests for Library TestlinkSeLibExtension, a Selenium2Library extension to access a TestLink web app to collect and verify test data for Teslink XMLRPC api tests.
...
...               Login - Open Test Specification and Test Project Management pages - Logout
...
...               pybot parameter for TestLink Demo applikation
...
...               --variable SERVER:demo.testlink.org/latest --variable DELAY:0.2
Suite Setup       Open Browser with TestLink Page
Suite Teardown    Close Browser
Test Setup        Unselect Frame
Force Tags        web
Default Tags      general
Resource          tlweb_resource.robot    #Suite Teardown    Close Browser

*** Test Cases ***
Login TestLink
    [Documentation]    Log into the TestLink web application can be done with _TestlinkSeLibExtension_ keyword *Login TestLink*.
    Login TestLink
    Location Should Contain    caller=login

Click Titlebar Element - Test Specification
    [Documentation]    Open Test Specification page can be done with _TestlinkSeLibExtension_ keyword *Click Titlebar Element*.
    Click Titlebar Element    Test Specification    mainframe
    Wait Until Frame Contains Element    mainframe    treeframe
    Capture Page Screenshot

Click Desktop Link - Test Project Management
    [Documentation]    Open Test Project Management page can be done with _TestlinkSeLibExtension_ keyword *Click Titlebar Element*.
    Click Desktop Link    Test Project Management    search
    Capture Page Screenshot

Get List with Indifier of All Visible Test Projects
    [Documentation]    List with Identifier of all visible Test Projects can be created \ with _TestlinkSeLibExtension_ keyword *Get All Visible Projects Identifier*.
    @{tp_infos}=    Get All Visible Projects Identifier
    Length Should Be    ${tp_infos}    4
    ${tp_count}=    Get Length    @{tp_infos}[0]
    Length Should Be    @{tp_infos}[1]    ${tp_count}
    Length Should Be    @{tp_infos}[2]    ${tp_count}
    Length Should Be    @{tp_infos}[3]    ${tp_count}

Select TestProject
    [Documentation]    selects the second test project in titlebars project list
    Select Frame    titlebar
    Log Source
    Capture Page Screenshot
    @{tprojects}=    Get List Items    testproject
    Select From List By Index    testproject    2
    Capture Page Screenshot
    Log Source
    ${tp_value}=    Execute Javascript    return document.getElementsByName("testproject")[0].options[0].value
    ${tp_title}=    Execute Javascript    return document.getElementsByName("testproject")[0].options[0].title

Click Desktop Link - Test Specification
    [Documentation]    Open Test Specification page can be done with _TestlinkSeLibExtension_ keyword *Click Desktop Link*.
    Click Desktop Link    Test Specification    treeframe
    Capture Page Screenshot

Logout TestLink
    [Documentation]    Log out of the TestLink web application can be done with _TestlinkSeLibExtension_ keyword *Logout TestLink*.
    Logout TestLink
    Location Should Contain    login.php
