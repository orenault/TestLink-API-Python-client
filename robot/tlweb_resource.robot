*** Settings ***
Documentation     A resource file with reusable keywords and variables testing the TestLink web application.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           Selenium2Library

*** Variables ***
${SERVER}         lkatlinkd7/testlink
${BROWSER}        ff
${DELAY}          0.1
${TL_USER}        admin
${TL_PASSWORD}    admin
${TL_URL}         http://${SERVER}/

*** Keywords ***
Open Browser with TestLink Page
    [Documentation]    prepares the browser for testing the TestLink web app
    Open Browser    ${TL_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

Login TestLink
    [Arguments]    ${username}=${TL_USER}    ${password}=${TL_PASSWORD}
    [Documentation]    Logs into the TestLink web app
    Location Should Contain    login.php
    Input Text    tl_login    ${username}
    Input Text    tl_password    ${password}
    Click Button    login_submit
    Location Should Contain    caller=login

Logout TestLink
    [Documentation]    Logs out of the TestLink web app
    Click Titlebar Image    Logout    login_div
    Location Should Contain    login.php

Click Titlebar Image
    [Arguments]    ${titlebar_link}    ${expected_elem}
    [Documentation]    Clicks on an image in TestLinks *titlebar*
    Log Location
    Click Frame Element    titlebar    xpath=//img[@title='${titlebar_link}']
    Wait Until Page Contains Element    ${expected_elem}

Click Desktop Link
    [Arguments]    ${desktop_link}    ${expected_elem}
    [Documentation]    Opens TestLinks *Desktop* page and clicks on a link.
    ...    Waits till the _mainframe_ includes a element.
    Click Titlebar Image    Desktop    mainframe
    Click Frame Element    name=mainframe    link=${desktop_link}
    Wait Until Frame Contains Element    mainframe    ${expected_elem}

Click Frame Element
    [Arguments]    ${frame_name}    ${frame_elem}    ${frame_unselect}=${true}
    [Documentation]    Selects a frame and clicks on an element in this frame
    ...
    ...    internal keyword for testing the TestLink web app which uses framesets
    Select Frame    ${frame_name}
    Click Element    ${frame_elem}
    Run Keyword If    ${frame_unselect}    Unselect Frame

Wait Until Frame Contains Element
    [Arguments]    ${frame_name}    ${frame_elem}
    [Documentation]    Waits, till a frame exists, select this frame and waits again till a sepcific element exists in this frame.
    ...
    ...    internal keyword for testing the TestLink web app which uses framesets
    Wait Until Page Contains Element    name=${frame_name}
    Select Frame    ${frame_name}
    Wait Until Page Contains Element    ${frame_elem}
