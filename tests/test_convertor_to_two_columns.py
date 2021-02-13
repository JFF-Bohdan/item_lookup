from shared.filtering_and_transformation import convert_to_two_columns_line


def test_able_to_convert_valid_line__into_two_columns_tuple():
    data = "foo,bar"
    assert convert_to_two_columns_line(data) == ("foo", "bar")


def test_able_to_convert_line_with_spaces_into_two_columns_tuple():
    data = "     foo    ,    bar    "
    assert convert_to_two_columns_line(data) == ("foo", "bar")


def test_will_return_none_for_non_two_column_line_provided():
    data = "foo,bar,bizz,bazz"
    assert convert_to_two_columns_line(data) is None


def test_able_to_process_empty_line():
    data = ""
    assert convert_to_two_columns_line(data) is None
