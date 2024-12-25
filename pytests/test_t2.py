import pytest
import requests
from unittest.mock import patch, MagicMock

def make_external_call(data, api_key):
    url = "https://some_url.com/data-dump"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(
        url, headers=headers, params = {"data": data}
        )
    return response.json()

def div_fun(a, b):
    data = a/b
    response = make_external_call(data=data, api_key="api@123")
    return response

@pytest.fixture(scope="module")
def var_dict():
    return {
        'a':5,
        'b':2
    }

def test_division(var_dict):
    with patch("test_t2.make_external_call") as mock_external_call:
        response = MagicMock()
        response.status = "Success"
        response.status_code = 200
        mock_external_call.return_value = response
        a = var_dict.get("a")
        b = var_dict.get("b")

        expected_result = a/b
        response = div_fun(a,b)
        assert response.status_code == 200
        mock_external_call.assert_called_once_with(
            data=expected_result, api_key='api@123'
        )

def test_div_by_zero_error(var_dict):
    a = var_dict.get('a')
    b = 0
    with pytest.raises(ZeroDivisionError):
        div_fun(a, b)




