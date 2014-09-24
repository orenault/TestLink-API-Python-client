*** Settings ***
Documentation     A test suite with a single test for valid login.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Suite Setup       Open Browser with TestLink Page
Suite Teardown    Close Browser
Resource          tlweb_resource.robot    #Suite Teardown    Close Browser

*** Test Cases ***
Login TestLink
    Login TestLink

Open Test Specification direkt
    Call Titlebar Link    Test Specification
    Capture Page Screenshot

Open Test Project Management
    Call Titlebar Link    Desktop
    Call Mainframe Link    Test Project Management    Description
    Capture Page Screenshot

Open Test Specification via Desktop
    Call Titlebar Link    Desktop
    Call Mainframe Link    Test Specification    Navigator - Test Specification
    Capture Page Screenshot

Logout TestLink
    Logout TestLink
