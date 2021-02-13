from shared.filtering_and_transformation import is_valid_format


def test_able_identify_that_passport_info_is_correct():
    data = tuple(["1234", "567890"])
    assert is_valid_format(data) == True


def test_able_identify_wrong_letter_in_passport_number():
    data = tuple(["123A", "567890"])
    assert is_valid_format(data) == False


def test_able_identify_wrong_number_of_digits_in_passport_number():
    data = tuple(["123456", "1234"])
    assert is_valid_format(data) == False
