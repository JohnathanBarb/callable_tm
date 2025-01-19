import transaction

from callable_tm.callable_tm import callable_tm


@callable_tm
def my_tested_function(array_to_append, value):
    array_to_append.append(value)
    return


def test_successful_transaction():
    result_array = []
    my_tested_function(result_array, 1)

    # assert that function was not called yet
    assert len(result_array) == 0

    transaction.commit()

    assert result_array == [1]


def test_aborted_transaction():
    result_array = []
    my_tested_function(result_array, 1)
    transaction.abort()

    assert result_array == []


def test_multiple_calls():
    result_array = []
    my_tested_function(result_array, 1)
    my_tested_function(result_array, 2)
    my_tested_function(result_array, 3)
    my_tested_function(result_array, 4)

    assert len(result_array) == 0

    transaction.commit()

    assert result_array == [1, 2, 3, 4]
