import pytest
from app.calculations import add


@pytest.mark.parametrize("num1, num2,sum", [(3,2,5 )])
def test_add():
    print("testing the add function")
    sum = add(5,3)
    assert sum == 8
    

test_add()