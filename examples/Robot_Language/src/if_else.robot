*** Settings ***
Documentation     Example test cases with IF conditions

*** Variables ***
@{ROBOTS}      Bender    Johnny5    Terminator    Robocop

*** Test Cases ***
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
