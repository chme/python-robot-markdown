*** Settings ***
Documentation     A simple test suite to show case how files created
...               in the output folder are included in robot-markdown
...               generated documentation.

Library    ../../.venv/lib/python3.10/site-packages/robot/libraries/OperatingSystem.py

*** Variables ***
${JSON_CONTENT}    SEPARATOR=\n
...    \{
...        "a": "b"
...    }

*** Test Cases ***
Test with file
    [Documentation]    File created in output folder in a Test Case
    Create File        ${OUTPUT_DIR}/myfiles/test_with_file.json    content=${JSON_CONTENT}
