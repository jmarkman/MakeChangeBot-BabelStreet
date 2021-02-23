class ChangeCalculation(object):
    def __init__(self, orig_value: str, change: list):
        self.original_value = orig_value
        self.change_string = ''.join(change)
        self.dollars = change[0]
        self.quarters = change[1]
        self.dimes = change[2]
        self.nickles = change[3]
        self.pennies = change[4]

    def __str__(self):
        return f"{self.original_value} --> Dollars: '{self.dollars}', Quarters: '{self.quarters}', Dimes: '{self.dimes}', Nickles: '{self.nickles}', Pennies: '{self.pennies}'"


MAX_INPUT_LENGTH = 5
CHANGE_VALUES = [100, 25, 10, 5, 1]


def parse_cash_string_as_numeric_value_in_cents(cash: str):
    value_in_cents = 0
    without_dollar_sign = cash[1:]
    split_value = without_dollar_sign.split('.')
    value_in_cents += (int(split_value[0]) * 100) + int(split_value[1])
    return value_in_cents


def make_change(cash_as_pennies: int, cash_input: str):
    values = []
    change = cash_as_pennies
    for val in CHANGE_VALUES:
        values.append(change // val)
        change %= val
    return ChangeCalculation(cash_input, values)


def calculate_change(cash: str):
    # Rudimentary NOP
    if len(cash) > MAX_INPUT_LENGTH:
        print("The provided cash value is too large for calculation")
        return
    parsed_cash = parse_cash_string_as_numeric_value_in_cents(cash)

    change_object = make_change(parsed_cash, cash)

    print(change_object)


if __name__ == '__main__':
    calculate_change('$1.57')
