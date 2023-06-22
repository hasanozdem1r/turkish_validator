"""
This module provides control to the Turkish ID Number and Turkish Tax Number validity status.
Developed within the framework of PEP8 and type annotations rules
"""

# NO IMPORTS

# FUNCTIONS


def is_valid_turkish_id(turkish_id: str) -> bool:
    """
    Turkish Identification Number is a unique personal identification number that is assigned to every citizen of Turkey.
    This function return your Turkish ID number validity status
    :param turkish_id: <str> 11 digits number
    :return: True(TR ID Valid), False(TR ID Invalid)
    """
    try:
        turkish_id: list = [int(item) for item in turkish_id]
        if len(turkish_id) != 11:
            return False
        else:
            if turkish_id[0] == 0:
                return False
            else:
                # given digit
                expected_10th_item: int = turkish_id[9]

                # variables to store sum of singular and plural digits
                total_singular, total_plural = 0, 0

                # sum of [1st, 3rd, 5th, 7th, 9th] digits
                total_singular = sum([
                    turkish_id[item] for item in range(0,
                                                       len(turkish_id) - 1, 2)
                ])

                # sum of [2nd, 4th, 6th, 8th] digits
                total_plural = sum([
                    turkish_id[item] for item in range(1,
                                                       len(turkish_id) - 3, 2)
                ])

                # calculated digit
                actual_10th_item = ((total_singular * 7) - (total_plural)) % 10

                if actual_10th_item != expected_10th_item:
                    return False
                else:
                    # given digit
                    expected_11th_item = turkish_id[10]

                    # calculated digit
                    actual_11th_item = sum(turkish_id[0:10]) % 10

                    if expected_11th_item != actual_11th_item:
                        return False
                    else:
                        return True
    except ValueError as error:
        raise Exception('Please only enter numbers').with_traceback(
            error.__traceback__)


def is_valid_turkish_tax_no(turkish_tax_no: str) -> bool:
    """
    Turkish tax identification number is the number used when paying taxes. Everyone with income has to pay tax through this number.
    The tax identification number is the number used to check the person's tax transactions.
    This function return your Turkish Tax number validity status
    :param turkish_tax_no: <str> 11 digits number
    :return: True(TR Tax Number Valid), False(TR Tax Number Invalid)
    """
    try:
        # convert string to list
        turkish_tax_no: list = [int(item) for item in turkish_tax_no]

        # must be 10 digits
        if len(turkish_tax_no) != 10:
            return False

        else:
            # temporary list to control 10th digit
            turkish_tax_no_temp: list = []
            # given 10th item
            actual_10th_item: int = turkish_tax_no[9]

            for item in range(0, len(turkish_tax_no) - 1, 1):
                # temp variable to check whether is 9 or !9
                temp_item: int = (turkish_tax_no[item] + 10 - item) % 10

                if temp_item == 9:
                    turkish_tax_no_temp.append(temp_item)
                else:
                    temp_item = (turkish_tax_no[item] * 2)**(10 - item) % 9
                    turkish_tax_no_temp.append(temp_item)

            # calculated 10th item
            calculated_10th_item: int = (10 - sum(turkish_tax_no_temp)) % 10

            if actual_10th_item != calculated_10th_item:
                return False
            else:
                return True

    except ValueError as error:
        raise Exception('Please only enter numbers').with_traceback(
            error.__traceback__)
