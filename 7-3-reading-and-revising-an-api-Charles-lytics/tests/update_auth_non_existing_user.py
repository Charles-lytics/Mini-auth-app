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

def test_update_auth_non_existing_user(client):

    # the first parameter is the name of the test file in /tests
    # the second parameter is the name of the te`st in autograding.json
    # the third parameter is the error message to display if the test fails
    run_test(client, "update_auth_non_existing_user", "Authentication update fails when updating authentication for a non-existing user", "Error: Please make sure that when attempting to access a non-existing user via API you return a user doesn't exist message back")

if __name__ == '__main__':
    pytest.main()