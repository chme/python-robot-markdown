*** Settings ***
Documentation    Example suite with initialization file
Suite Setup      Do Something    ${MESSAGE}
Test Tags        example
Library    ../../.venv/lib/python3.10/site-packages/robot/libraries/OperatingSystem.py

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
