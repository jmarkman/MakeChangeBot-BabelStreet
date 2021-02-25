import base64
import rds_config
import re
import time
from urllib import parse as urlparse
from dto import ChangeCalculation
from dbaccess import AWSDataAccess

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
    return ChangeCalculation(cash_input, ''.join(str(v) for v in values), time.strftime('%Y-%m-%d %H:%M:%S'))


def get_calculation_from_receipt(receipt: str, current_user: str):
    """
    Given a receipt, retrieves the results of a previous change calculation
    :param receipt: The unique identifier for the calculation
    :param current_user: The user making the request - users may only access their own calculations
    :return:
    """
    data_access = AWSDataAccess(rds_config.host, rds_config.db_name, rds_config.db_username, rds_config.db_password)

    valid_receipt = re.search("[A-Z0-9]{8}", receipt)

    if valid_receipt:
        return f"Change calculation for {receipt}:\n{str(data_access.get_change_from_receipt(receipt, current_user))}"
    else:
        return "The provided receipt was not valid"


def calculate_change(cash: str, current_user: str):
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

    data_access = AWSDataAccess(rds_config.host, rds_config.db_name, rds_config.db_username,
                                rds_config.db_password)

    receipt = data_access.add_change_calculation(current_user, change_object)

    return f"{change_object}\nReceipt: {receipt}"

def lambda_handler(event, context):
    slack_msg_dict = dict(urlparse.parse_qsl(base64.b64decode(str(event['body'])).decode('ascii')))
    command = slack_msg_dict.get('command', 'err')
    input = slack_msg_dict.get('text', 'err')
    current_user = slack_msg_dict.get('user_id', 'err')

    bot_commands = {
        "/makechangefrom": calculate_change(input, current_user),
        "/getchangecalculation": get_calculation_from_receipt(input, current_user)
    }

    try:
        result = bot_commands[command]
    except KeyError:
        result = "Invalid command"

    return {
        "response_type": "in_channel",
        "text": result
    }
