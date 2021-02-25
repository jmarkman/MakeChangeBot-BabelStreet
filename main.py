from dto import ChangeCalculation

MAX_INPUT_LENGTH = 5
CHANGE_VALUES = [100, 25, 10, 5, 1]


def parse_cash_string_as_numeric_value_in_cents(cash: str):
    """
    Given a string that represents a dollar value, this function
    trims the dollar sign and represents the total value as pennies
    """
    value_in_cents = 0
    without_dollar_sign = cash[1:]
    split_value = without_dollar_sign.split('.')
    value_in_cents += (int(split_value[0]) * 100) + int(split_value[1])
    return value_in_cents


def make_change(cash_as_pennies: int, cash_input: str):
    """
    Given the total number of pennies that make up the provided value,
    calculate the best way to break it into change using the fewest
    denominations of coins. This method requires the original input
    from the user so it can be stored in the ChangeCalculation DTO
    for logging and storage in the database
    """
    values = []
    change = cash_as_pennies
    for val in CHANGE_VALUES:
        values.append(change // val)
        change %= val
    return ChangeCalculation(cash_input, ''.join())


def calculate_change(cash: str):
    """
    Given a dollar amount in the form '$x.xx', determines the appropriate
    way to break the value into change with the fewest number of denominations
    """
    # Rudimentary NOP
    # TODO: This only checks that input matches a max string length, need additional checking (i.e., is float)
    # 'cash' could be '$x.xx' verbatim, which would pass this check but break the implementation
    if len(cash) > MAX_INPUT_LENGTH:
        print("The provided cash value is too large for calculation")
        return
    parsed_cash = parse_cash_string_as_numeric_value_in_cents(cash)

    change_object = make_change(parsed_cash, cash)

    print(change_object)


if __name__ == '__main__':
    calculate_change('$1.57')
