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

def test_access_row_non_existing_user(client):

    # the first parameter is the name of the test file in /tests
    # the second parameter is the name of the te`st in autograding.json
    # the third parameter is the error message to display if the test fails
    run_test(client, "access_row_non_existing_user", "User access fails when when trying to access a non-existing user via API", "Error: User access should fail when when trying to access a non-existing user via API")

if __name__ == '__main__':
    pytest.main()