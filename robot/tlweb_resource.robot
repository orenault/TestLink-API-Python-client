*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           Selenium2Library

*** Variables ***
${SERVER}         lkatlinkd7/testlink
${BROWSER}        ff
${DELAY}          0.2
${TL_USER}        admin
${TL_PASSWORD}    admin
${TL_URL}         http://${SERVER}/

*** Keywords ***
Open Browser with TestLink Page
    Open Browser    ${TL_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}

Login TestLink
    [Arguments]    ${username}=${TL_USER}    ${password}=${TL_PASSWORD}
    Location Should Contain    login.php
    Input Text    tl_login    ${username}
    Input Text    tl_password    ${password}
    Click Button    login_submit
    Location Should Contain    caller=login

Logout TestLink
    Call Titlebar Link    Logout
    Location Should Contain    login.php

Call Titlebar Link
    [Arguments]    ${titlebar_link}    ${expected_text}=TestLink
    Log Location
    Go To    ${TL_URL}
    Select Frame    name=titlebar
    Click Link    link=${titlebar_link}
    Wait Until Page Contains    ${expected_text}

Call Mainframe Link
    [Arguments]    ${mainframe_link}    ${expected_text}=TestLink
    Select Frame    name=mainframe
    Click Link    link=${mainframe_link}
    Wait Until Page Contains    ${expected_text}
