# Babel Street Code Challenge -  Change Bot

## Objectives

### Make Change

Given a text message via Slack in the form `$x.xx`, make change from that value in the fewest number of denominations and return an identifier for this operation.
Example 1 from prompt:
    $1.57 --> 1 dollar, 2 quarters, 0 dimes, 1 nickle, 2 pennies
    Receipt# QZ42D66
    
Example 2 self-created:
    $9.31 --> 1 5-dollar, 4 1-dollar, 1 quarter, 0 dimes, 1 nickle, 1 penny
    Receipt# AM61H54

Will enforce arbitrary limitation of being unable to make change from values greater than $9.99 due to time constraints.

### Retrieve Previous Change Making Operations

Given a text message via Slack in the form `Receipt# xxxxxxx` where the `x` characters form some kind of identifier for a "make change" operation, retrieve the calculation from a database.

Example from prompt:
    `Receipt# QZ42D66` should print something along the lines of:
    Cash: $1.57
    Change: 1 dollar, 2 quarters, 0 dimes, 1 nickle, 2 pennies
    (formatting differs from example in prompt)
    
## Implementation