class ChangeCalculation(object):
    def __init__(self, orig_value: str, change: list):
        self.original_value = orig_value
        self.change_string = ''.join(str(c) for c in change)
        self.dollars = change[0]
        self.quarters = change[1]
        self.dimes = change[2]
        self.nickles = change[3]
        self.pennies = change[4]

    def __str__(self):
        return f"{self.original_value} --> Dollars: '{self.dollars}', Quarters: '{self.quarters}', Dimes: '{self.dimes}', Nickles: '{self.nickles}', Pennies: '{self.pennies}'"