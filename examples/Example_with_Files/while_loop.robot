*** Test Cases ***
WHILE: A simple while loop using the default loop limit
    WHILE    True    limit=10
        Log    Executed until the given loop limit (10) is hit.
    END

WHILE: Loop while the given limit is hit
    TRY
        WHILE    True    limit=10
            Log    Executed until the given loop limit (10) is hit.
        END
    EXCEPT    WHILE loop was aborted    type=start
        Log    The loop did not finish within the limit.
    END

WHILE: Loop while condition evaluates to True or the default loop limit is hit
    ${x}=    Set Variable    ${0}
    WHILE    ${x} < 3
        Log    Executed as long as the condition is True.
        ${x}=    Evaluate    ${x} + 1
    END

WHILE: Skip a loop iteration with CONTINUE
    ${x}=    Set Variable    ${0}
    WHILE    ${x} < 3
        ${x}=    Evaluate    ${x} + 1
        IF    ${x} == 2    CONTINUE    # Skip this iteration.
        Log    x = ${x}    # x = 1, x = 3
    END

WHILE: Exit loop with BREAK
    WHILE    True
        BREAK
        Log    This will not be logged.
    END