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
@{ROBOTS}      Bender    Johnny5    Terminator    Robocop

*** Test Cases ***
Test with file
    [Documentation]    File created in output folder in a Test Case
    Create File        ${OUTPUT_DIR}/myfiles/test_with_file.json    content=${JSON_CONTENT}

File in sub keyword
    [Documentation]    File created in a sub keyword
    Create File In Output Folder

Use IF construct in Robot Framework
    IF    ${True}
        Log    This line IS executed.
    END
    IF    ${False}
        Log    This line is NOT executed.
    END
    IF    "cat" == "cat"
        Log    This line IS executed.
    END
    IF    "cat" != "dog"
        Log    This line IS executed.
    END
    IF    "cat" == "dog"
        Log    This line is NOT executed.
    END
    IF    "cat" == "cat" and "dog" == "dog"
        Log    This line IS executed.
    END
    IF    "cat" == "cat" and "dog" == "cat"
        Log    This line is NOT executed.
    END
    IF    1 == 1
        Log    This line IS executed.
    END
    IF    2 < 1
        Log    This line is NOT executed.
    END
    IF    2 <= 2
        Log    This line IS executed.
    END
    IF    len("cat") == 3
        Log    This line IS executed.
    END
    IF    (1 == 1 and 2 == 2) and 3 == 3
        Log    This line IS executed since the expressions evaluate to True.
    END
    IF    (1 == 2 or 3 == 4) or 3 == 3
        Log    This line IS executed since one of the expressions evaluates to True.
    END

Use inline IF construct in Robot Framework
    IF  "cat" == "cat"    Log    This is logged.    ELSE    Log    This is NOT logged.

Use IF / ELSE construct in Robot Framework
    IF    1 == 1
        Log    This line IS executed.
    ELSE
        Log    This line is NOT executed.
    END
    IF    1 == 2
        Log    This line is NOT executed.
    ELSE
        Log    This line IS executed.
    END

Use IF / ELSE IF construct in Robot Framework
    IF    1 == 1
        Log    This line IS executed.
    ELSE IF    2 == 2
        Log    This line is NOT executed.
    END
    IF    1 == 2
        Log    This line is NOT executed.
    ELSE IF    2 == 2
        Log    This line IS executed.
    END
    IF    1 == 2
        Log    This line is NOT executed.
    ELSE IF    2 == 3
        Log    This line is NOT executed.
    END

Use IF / ELSE IF / ELSE construct in Robot Framework
    IF    1 == 1
        Log    This line IS executed.
    ELSE IF    2 == 2
        Log    This line is NOT executed.
    ELSE
        Log    This line is NOT executed.
    END
    IF    1 == 2
        Log    This line is NOT executed.
    ELSE IF    2 == 2
        Log    This line IS executed.
    ELSE
        Log    This line is NOT executed.
    END
    IF    1 == 2
        Log    This line is NOT executed.
    ELSE IF    2 == 3
        Log    This line is NOT executed.
    ELSE
        Log    This line IS executed.
    END

Use Run Keyword If in Robot Framework
    Run Keyword If    ${True}    Log    This line IS executed.
    Run Keyword If    ${False}    Log    This line is NOT executed.

Use Run Keyword Unless in Robot Framework
    Run Keyword Unless    ${True}    Log    This line is NOT executed.
    Run Keyword Unless    ${False}    Log    This line IS executed.

Execute a for loop only three times
    FOR    ${robot}    IN    @{ROBOTS}
        IF    $robot == 'Terminator'    CONTINUE
        Log    ${robot}
    END

*** Keywords ***
Create File In Output Folder
    [Arguments]        ${filename}=mytestfile.txt    ${content}=Lorem ipsum
    Create File        ${OUTPUT_DIR}/${filename}    content=${content}
