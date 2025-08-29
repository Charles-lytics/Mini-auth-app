import subprocess
import requests
import json
import socket
import os
import platform
import sqlite3
import time
import tempfile
import sys
import pytest

sys.path.append('..')
from central_setup.central_setup import (
    execute_logic,
    check_internet_connection,
)

program_name = 'user_editing.py'

def run_test(client, test_name, test_point_key, offline_feedback):
     test_output, test_points_awarded, test_feedback, test_response_data = pre_test_setup(client, test_name)
 
     autograding_path = os.path.abspath(
         os.path.join(os.path.dirname(__file__), '..', '.github', 'classroom', 'autograding.json'))
     # Load points from autograding.json
     with open(autograding_path, 'r') as f:
         autograding_config = json.load(f)
 
     # Find the points for the specific test
     test_config = autograding_config["tests"][0]
     expected_points = test_config["points"] if test_config else 0
 
     if check_internet_connection():
         assert test_points_awarded.get(test_point_key, 0) == expected_points, test_feedback
     else:
         assert test_points_awarded.get(test_point_key, 0) == expected_points, offline_feedback


def check_database(user):
    """Check if the database has been created."""
    try:
        conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', 'people.db'))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (user,))
        user_data = cursor.fetchone()
        conn.close()
        return user_data
    except sqlite3.OperationalError:
        return None

def logic_access_row_exising_user(client):
    """Logic to test if the program can access an existing user."""
    response = client.get('/revise?username=George_Washington')
    return response

def logic_update_auth_existing_user(client):
    """Logic to test if the program can update the auth level of an existing user."""
    response = client.get('/revise?username=George_Washington&auth=3')
    return response

def logic_access_row_non_existing_user(client):
    """Logic to test if the program can access a non-existing user."""
    response = client.get('/revise?username=nonexistent')
    return response

def logic_update_auth_non_existing_user(client):
    """Logic to test if the program can update the auth level of a non-existing user."""
    response = client.get('/revise?username=nonexistent&auth=22')
    return response


def pre_test_setup(client, test_name=None, test_point_key=None):
    test_points_awarded = {}
    test_feedback = {}
    test_outputs = {}
    test_response_data = None

    test_response_data = None
    if test_name:
        if test_name == "access_row_existing_user":
            test_outputs["access_row_existing_user"] = logic_access_row_exising_user(client)
        elif test_name == "update_auth_existing_user":
            test_outputs["update_auth_existing_user"] = logic_update_auth_existing_user(client)
        elif test_name == "access_row_non_existing_user":
            test_outputs["access_row_non_existing_user"] = logic_access_row_non_existing_user(client)
        elif test_name == "update_auth_non_existing_user":
            test_outputs["update_auth_non_existing_user"] = logic_update_auth_non_existing_user(client)
    else:
        test_outputs = {
            "access_row_existing_user": logic_access_row_exising_user(client),
            "update_auth_existing_user": logic_update_auth_existing_user(client),
            "access_row_non_existing_user": logic_access_row_non_existing_user(client),
            "update_auth_non_existing_user": logic_update_auth_non_existing_user(client)
        }

    json_serializable_outputs = {
        key: (
            {
                "status_code": response.status_code,
                "json": response.get_json()
            }
        )
        for key, response in test_outputs.items()
    }


    # Add the current database record for "George_Washington" to the test outputs
    # for tests related to existing users. This ensures the test results include
    # the state of the database for validation purposes.
    if not test_name:
        json_serializable_outputs["access_row_existing_user"]["current_db_record"] = check_database("George_Washington")
        json_serializable_outputs["update_auth_existing_user"]["current_db_record"] = check_database("George_Washington")



    user_editing_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'user_editing.py'))
    autograding_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '.github', 'classroom', 'autograding.json'))
    test_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_user_editing.py'))

    if check_internet_connection():
        try:
            with open(user_editing_path, 'r') as f:
                student_code = f.read()
            with open(test_app_path, 'r') as f:
                pytest_code = f.read()
            with open(autograding_path, 'r') as f:
                autograding_config = json.load(f)
                filtered_autograding_config = {"tests": autograding_config["tests"][:-1]}

            # Pass the logic to the central_setup module
            test_outputs, test_points_awarded, test_feedback, test_response_data = execute_logic(
                test_name, json_serializable_outputs, student_code, pytest_code, autograding_config
            )

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"API call failed: {e}")
            print("Proceeding without API response. Run the test again with a working API to receive more user-friendly feedback.")

    return test_outputs, test_points_awarded, test_feedback, test_response_data