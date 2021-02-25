import pymysql
import uuid
from dto import ChangeCalculation


class AWSDataAccess(object):
    def __init__(self, host, db, user, pw):
        self.rdb_host = host
        self.db_name = db
        self.user_name = user
        self.password = pw

    def __enter__(self):
        try:
            self.db_conn = pymysql.connect(self.rdb_host, user=self.user_name, passwd=self.password, db=self.db_name)
            return self.db_conn
        except pymysql.MySQLError as sqlErr:
            print(f"Error: could not connect to AWS MySQL RDB. {sqlErr}")

    def add_change_calculation(self, calculation: ChangeCalculation):
        """
        Adds a provided change calculation to the database
        :param calculation: The ChangeCalculation object containing the original value and denominations
        :return: 1 if the row was inserted successfully, 0 on failure
        """
        with self.db_conn.cursor() as cursor:
            sql = "insert into makechange_results (receipt, submittedby, initialvalue, compresseddenominations) values (%s, %s, %s, %s)"
            affected_rows = cursor.execute(sql, (self.__generate_receipt(), "bar", calculation.original_value, calculation.change_string))
        self.db_conn.commit()
        return affected_rows

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
        with self.db_conn.cursor() as cursor:
            sql = "select * from makechange_results where receipt = %s"
            cursor.execute(sql, receipt)
            row = cursor.fetchone()
            denomination_list = row["compresseddenomination"].split()
            change_dto = ChangeCalculation(row["initialvalue"], denomination_list)
            if user_name != row["submittedby"]:
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

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_conn.close()
        if exc_val:
            raise
