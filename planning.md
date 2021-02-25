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

Update (2/23): I was thinking about it on the 21st and decided on the 22nd that it'd be best to limit the dollar cash value due to the project's time limit

### Retrieve Previous Change Making Operations

Given a text message via Slack in the form `Receipt# xxxxxxx` where the `x` characters form some kind of identifier for a "make change" operation, retrieve the calculation from a database.

Example from prompt:

`Receipt# QZ42D66` should print something along the lines of:

    Cash: $1.57
    Change: 1 dollar, 2 quarters, 0 dimes, 1 nickle, 2 pennies
    (formatting differs from example in prompt)
    
**Users retrieving receipts should not be able to get receipts for change calculations made by other users**
    
## Implementation

### General Implementation

This looks like an interesting opportunity to leverage AWS. The pathway I'm thinking of as I initially type this is:

Slack --> Amazon Lambda --> Amazon RDS (MySQL)

Why MySQL? Ease. While there's a lot of material about databases like PostgreSQL, I'd like something that's very battle tested for quick database operations, and MySQL is a very common RDB in that regard. I want the confidence that I can plug a question into google if I'm stuck and I'll find something relevant *fast*.

#### Make Change

1. Message sent in Slack using backslash command `/makechange`
2. Command hosted on AWS Lambda performs computation
3. Lambda pushes change computation to RDS
4. Lambda prints the change computation to Slack

#### Get Calculation

1. Message sent in Slack using backslash command `/receipt#`
2. Command hosted on AWS Lambda retrieves previous computation from database if user can access that computation
3. Lambda prints the results of that computation to Slack

#### Database Implementation

Columns:

- Receipt

Identifying receipt of the change calculation

- SubmittedBy

The Slack ID of the user who asked for the specified calculation

- InitialValue

The dollar amount submitted by the user

- CompressedDenominations

A string representing the completed change calculation

### Technical Details

As I write this (2/18/21) I believe the operation will go something like this:

1. Input from user comes through
2. Calculate change, store results in an array? Object? Dictionary? Leaning more towards array, but maybe an object might work.
3. Condense results into a string where the translation would look like this: `0 5-dollars, 1 1-dollar, 2 quarters, 0 dimes, 1 nickle, 2 pennies --> 012012`
4. Store necessary data in database
5. When requested, withdraw data from database and parse condensed results string

## 