from abc import ABC, abstractmethod
import datetime
import re


class Validator(ABC):
    def __init__(self, data: str, error):
        self.data: str = data
        self.error = error

    @abstractmethod
    def validate(self) -> bool:
        pass


class DateValidator(Validator):
    """Class used to validate a date formate"""

    def validate(self) -> bool:
        """Method used to validate date"""
        date: str = self.data
        # Check the date format first
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except Exception as e:
            raise self.error("Incorrect data format, should be YYYY-MM-DD.")

        return True


class EmailValidator(Validator):
    """Class Used to validate email formate"""

    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    def validate(self) -> bool:
        email: str = self.data
        if re.fullmatch(self.regex, email):
            return True
        raise self.error("Invalid email address.")


class NameValidator(Validator):
    """Class Used to validate name formate"""

    def validate(self) -> bool:
        """Function used to validate name"""
        name: str = self.data
        if not name:
            raise self.error(
                "Please make sure to enter you'r first name and last name."
            )
        if not name.isalpha():
            raise self.error("Your first name can only contain characters.")
        return True


class PasswordValidator(Validator):
    """Class Used to validate password"""

    def length(self, password: str):
        if len(password) < 8:
            raise self.error(
                "Password should be longer than 8 characters|numbers|special characters."
            )
        elif len(password) > 128:
            raise self.error(
                "Password should be less than 128 characters|numbers|special characters."
            )
        else:
            return True

    def character_format(self, password: str):
        if not any(char.isalpha() for char in password):
            raise self.error("Password should contain at least one character A-Z a-z.")
        if not any(number.isnumeric() for number in password):
            raise self.error("Password should contain at least one number 0-9.")
        return True

    def validate(self):
        """Function used to validate password"""
        password: str = self.data

        format_valid: bool = self.character_format(password)
        length_valid: bool = self.length(password)

        return format_valid and length_valid
