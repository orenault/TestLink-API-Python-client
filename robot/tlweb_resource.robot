*** Settings ***
Documentation     A resource file with reusable keywords and variables testing the TestLink web application.
Library           Selenium2Library
Library           TestlinkSeLibExtension    ${TL_URL}    ${TL_USER}    ${TL_PASSWORD}

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
