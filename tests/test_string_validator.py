from shared.filtering_and_transformation import is_valid_number_item


def test_able_check_valid_passport_series():
    dictionary = {str(index) for index in range(10)}
    data = "1234"
    assert is_valid_number_item(data, 4, dictionary) == True


def test_able_to_find_input_with_invalid_symbol():
    dictionary = {str(index) for index in range(10)}
    data = "12A4"
    assert is_valid_number_item(data, 4, dictionary) == False


def test_able_to_find_wrong_length_of_input():
    dictionary = {str(index) for index in range(10)}
    data = "12345"
    assert is_valid_number_item(data, 4, dictionary) == False


def test_able_check_valid_passport_number():
    dictionary = {str(index) for index in range(10)}
    data = "123456"
    assert is_valid_number_item(data, 6, dictionary) == True
