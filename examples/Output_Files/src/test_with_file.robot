*** Settings ***
Documentation     A simple test suite to show case how files created
...               in the output folder are included in robot-markdown
...               generated documentation.

Library           OperatingSystem

*** Variables ***
${JSON_CONTENT}    SEPARATOR=\n
...    \{
...        "a": "b"
...    }

*** Test Cases ***
Test with file
    [Documentation]    File created in output folder in a Test Case
    Create File        ${OUTPUT_DIR}/myfiles/test_with_file.json    content=${JSON_CONTENT}

File in sub keyword
    [Documentation]    File created in a sub keyword
    Create File In Output Folder

*** Keywords ***
Create File In Output Folder
    [Arguments]        ${filename}=mytestfile.txt    ${content}=Lorem ipsum
    Create File        ${OUTPUT_DIR}/${filename}    content=${content}
