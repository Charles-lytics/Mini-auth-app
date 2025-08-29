import pytest
from common_setup import run_test
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from user_editing import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_access_row_exising_user(client):

    # the first parameter is the name of the test file in /tests
    # the second parameter is the name of the test in autograding.json
    # the third parameter is the error message to display if the test fails
    run_test(client, "access_row_existing_user", "Correct user returned when accessing an existing user via API", "The program cannot access an existing user")

if __name__ == '__main__':
    pytest.main()