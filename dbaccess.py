import pymysql
import uuid
from dto import ChangeCalculation


class AWSDataAccess(object):
    def __init__(self, host, db, user, pw):
        self.rdb_host = host
        self.db_name = db
        self.user_name = user
        self.password = pw

    def add_change_calculation(self, user_id: str, calculation: ChangeCalculation):
        """
        Adds a provided change calculation to the database
        :param user_id: The user currently requesting the calculation
        :param calculation: The ChangeCalculation object containing the original value and denominations
        :return: The receipt of the calculation to use for accessing it in the future
        """
        receipt = self.__generate_receipt()
        with pymysql.connect(host=self.rdb_host, user=self.user_name, passwd=self.password, db=self.db_name) as conn:
            with conn.cursor() as cursor:
                sql = "insert into makechange_results (receipt, submittedby, initialvalue, compresseddenominations, dateadded) values (%s, %s, %s, %s, %s)"
                affected_rows = cursor.execute(sql, (receipt, user_id, calculation.original_value, calculation.change_string, calculation.calculation_time))
            conn.commit()
        return receipt

    def get_change_from_receipt(self, receipt: str, user_name: str):
        """
        Retrieves the change calculation for the provided receipt
        :param receipt: The unique identifier for the desired change calculation
        :param user_name: The name of the user making the request
        :return: The change calculation dto if the user made the request matches the original user who submitted the
        calculation, otherwise returns a blocking string
        """
        # Not a fan that I'm doing an ambiguous (Any) return, but the idea is that
        # this is going to be printed to Slack as a message
        with pymysql.connect(host=self.rdb_host, user=self.user_name, passwd=self.password, db=self.db_name) as conn:
            with conn.cursor() as cursor:
                sql = "select * from makechange_results where receipt = %s"
                cursor.execute(sql, receipt)
                row = cursor.fetchone()
                denomination_list = list(row[3])
                change_dto = ChangeCalculation(row[2], denomination_list, row[4])
                if user_name != row[1]:
                   return "Users may only access their own change calculations."
                else:
                    return change_dto

    def __generate_receipt(self):
        """
        Generates a unique identifier based on generating a uuid4,
        accessing the hex value, and using the first 8 characters
        as the unique identifer
        :return: The identifier as a string
        """
        # Source: https://stackoverflow.com/a/42703170
        return uuid.uuid4().hex[:8].upper()

