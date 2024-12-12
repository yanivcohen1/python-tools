
# all tested need to be in format test_*.py
# in file setup.cfg in section [tool:pytest] testpaths=flaskr/tools/py_test
# in settings.json
"""
"python.testing.pytestEnabled": true,
"python.testing.unittestEnabled": false,
"python.testing.pytestArgs": [
  "flaskr/tools/py_test"
]
"""
# run the all tests ">pytest"
# run the spcific tests ">pytest -q test_class.py"
# from testing tab select tests to run or debug
from unittest import mock
from unittest.mock import call, patch, ANY
from flaskr.tools.py_test.sample import random_sum, silly

@patch("flaskr.tools.py_test.sample.random.randint")
def test_random_sum(mock_randint):
    mock_randint.side_effect = [3, 4] # first run return 3 second run return 4
    assert random_sum() == 7
    mock_randint.assert_has_calls(calls=[call(1, 10), call(1, 7)])

def my_side_effect(num1 , num2):
    return num2 + 1

@patch("flaskr.tools.py_test.sample.random")
def test_my_random_sum(mock_random):
    mock_random.randint.side_effect = my_side_effect
    assert random_sum() == 19
    mock_random.randint.assert_has_calls(calls=[call(1, 10), call(1, 7)])

@patch("flaskr.tools.py_test.sample.random.randint")
@patch("flaskr.tools.py_test.sample.time.time")
@patch("flaskr.tools.py_test.sample.requests.get")
def test_silly(mock_requests_get, mock_time, mock_randint):
    test_params = {
        "timestamp": 123,
        "number": 5
    }
    mock_time.return_value = test_params['timestamp']
    mock_randint.return_value = 5
    mock_requests_get.return_value = mock.Mock(**{"status_code": 200,
                        "json.return_value": {"args": test_params}}) # all fun need return_value
    assert silly() == test_params


def my_str(strs):
    return strs

@patch("flaskr.tools.py_test.sample.my_str")
def test_my_random_sum2(mock_my_str):
    mock_my_str.side_effect = my_str
    assert random_sum() == "mock"
    mock_my_str.assert_has_calls(calls=[call("mock")])


@patch("flaskr.tools.py_test.sample.random.randint")
@patch("flaskr.tools.py_test.sample.time.time")
@patch("flaskr.tools.py_test.sample.requests.get")
def test_silly2(mock_requests_get, mock_time, mock_randint):
    test_params = {
        "timestamp": 123,
        "number": 5
    }
    mock_time.return_value = test_params['timestamp']
    mock_randint.return_value = 5
    req_get_ret_val = mock_requests_get.return_value
    req_get_ret_val.status_code = 200
    req_get_ret_val.json.return_value = {"args": test_params} # all fun need return_value
    assert silly() == test_params
