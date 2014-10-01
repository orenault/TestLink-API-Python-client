*** Settings ***
Documentation     A test suite with a simple smoke tests for TestLinkngle test for valid login.
...
...               Login - Open Test Specification and Test Project Management pages - Logout
Suite Setup       Open Browser with TestLink Page
Suite Teardown    Close Browser
Test Setup        Unselect Frame
Force Tags        web
Default Tags      general
Resource          tlweb_resource.robot    #Suite Teardown    Close Browser

*** Test Cases ***
Login TestLink
    Login TestLink

Open Test Specification direkt
    Click Titlebar Image    Test Specification    mainframe
    Wait Until Frame Contains Element    mainframe    treeframe
    Capture Page Screenshot

Open Test Project Management
    Click Desktop Link    Test Project Management    search
    Capture Page Screenshot

Open Test Specification via Desktop
    Click Desktop Link    Test Specification    treeframe
    Capture Page Screenshot

Logout TestLink
    Logout TestLink
