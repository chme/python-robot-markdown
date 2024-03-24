*** Settings ***
Documentation    Example test suite with initialization file
Suite Setup      Do Something    ${MESSAGE}
Test Tags        example
Library          OperatingSystem

*** Variables ***
${MESSAGE}       Hello, world!
${CONTENT}       SEPARATOR=\n
...    version=1.0.0
...    env=QA
...    url=https://localhost:8080/myserver

*** Keywords ***
Do Something
    [Arguments]    ${arg}
    Log    Running suite setup - ${arg}
    Create File    ${OUTPUT_DIR}/test.env    content=${CONTENT}
