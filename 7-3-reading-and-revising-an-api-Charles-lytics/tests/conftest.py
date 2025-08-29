import pytest

def pytest_sessionfinish(session, exitstatus):
    if exitstatus == 0:
        print("\n\033[1;32m🎉 Congratulations! 🚀 All tests passed,\033[0m \033[1;31mBUT to get full points, please submit your code to GitHub (10 points for submitting to GitHub)\033[0m")