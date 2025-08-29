# *****************************************************************************
# *                                                                           *
# *   IMPORTANT: DO NOT MODIFY THIS FILE                                      *
# *                                                                           *
# *   This testing file is provided to help you check the functionality of    *
# *   your code and understand the requirements for this assignment.          *
# *                                                                           *
# *   Please review the tests carefully to understand what is expected, but   *
# *   DO NOT make any changes to this file. Modifying this file will          *
# *   interfere with the grading system, lead to incorrect results, and       *
# *   will be flagged as cheating.                                            *
# *                                                                           *
# *   Focus on writing your own code to meet the requirements outlined in the *
# *   tests.                                                                  *
# *                                                                           *
# *****************************************************************************

import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from user_editing import app
from common_setup import pre_test_setup, check_internet_connection, check_database



@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_all(client):
    test_output, test_points_awarded, test_feedback, test_response_data = pre_test_setup(client)  # passing no tests means test everything
    if check_internet_connection():
        assert test_response_data['totalPointsAwarded'] == test_response_data['totalPointsPossible'], test_feedback
    else:
        ## Asserts for Test Access Row Existing User
        db_record = check_database('George_Washington')
        if not db_record:
            pytest.fail("Error: Database not created. Solution: Please make sure to run the createDB.py and insert_recs.py scripts.")
        assert (1, 'George_Washington', '1799') == db_record[:3] or (1, 'george_washington', '1799') == db_record[:3]
        response = test_output['access_row_existing_user']
        assert response.status_code == 200
        data = response.get_json()
        assert data[1] == 'George_Washington' or 'george_washington'

        ## Asserts for Test Access Row Non Existing User
        response = test_output['access_row_non_existing_user']
        assert response.status_code == 400
        data = response.get_json()
        assert data == {'User not found': 'nonexistent'} or {'user not found': 'nonexistent'}

        ## Asserts for Test Update Auth Existing User
        response = test_output['update_auth_existing_user']
        assert response.status_code == 200
        data = response.get_json()
        assert (data[1], data[3]) == ('George_Washington', 3.0) or ('george_washington', 3.0) or (data[1], data[3]) == ('George_Washington', 3) or ('george_washington', 3)
        db_record = check_database('George_Washington')
        assert db_record == (1, 'George_Washington', '1799', 3.0) or (1, 'george_washington', '1799', 3.0) or db_record == (1, 'George_Washington', '1799', '3') or (1, 'george_washington', '1799', '3')
        db_record = check_database('George_Washington')
        if not db_record:
            pytest.fail("Error: George Washington's record is missing or his auth level was not updated to 3.0. Ensure the record exists and the API correctly updates the auth level.")
        assert (1, 'George_Washington', '1799', 3.0) == db_record or (1, 'George_Washington', '1799', 3) == db_record

        ## Asserts for Test Update Auth Non Existing User
        response = test_output['update_auth_non_existing_user']
        assert response.status_code == 400
        data = response.get_json()
        assert data == {'User not found': 'nonexistent'}  or {'user not found': 'nonexistent'}


        # Scaduoosh
