[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=20076267)
# 7.4 Final Project: Reading and Revising an API

## Before you Start
You must complete Assignment 7.4 Creating and Filling a Database Table properly or you will not be able to do this assignment.

Before you attempt to complete this assignment, make sure you have successfully executed the `show_all_records.py` program, and that the resulting output shows the forty+ users in the database in a manner shown below:

```
1 George_Washington 1799 1
2 John_Adams 1826 1
3 Thomas_Jefferson 1826 1
4 James_Madison 1836 1
5 James_Monroe 1831 1
```

## The Final Project

In this Final Project, you will create Python code, including routing information, that will allow you to enter a URL containing certain embedded parameters that will allow you to either read all the information associated with a particular user, or alter the authorization level of a particular user and show, through returned JSON, that the authorization level has, indeed, been changed.

An example program can be found in this Github Codespace:  `fertilizer_editing.py`

## Your Task
Using the users table created in assignment 7.4 as the backend database supporting the API, create a Flask app with only two routes: a root (index) and a /revise route. 

The **root ( / )** route will reveal a generic greeting welcoming the client to the Users Database.
The **revise ( /revise )** route will accept parameters that will either retrieve a particular user or alter his/her authorization level, much like the `fertilizer_editing.py` program.
Your program (call it `user_editing.py`) will either retrieve a JSON object of a particular user (specified by a username) or alter the authorization level of a particular user if the parameters include the username and a new authorization value. It should be like the `fertilizer_editing.py` program, so make sure you have watched the video explaining that code.

## Example Output
When you run a Python Flask Application (Which is what this assignment is), a browser is launched and waits for the user to enter a URL.
When you run your application in GitHub Codespaces, a blue button will appear (after a short wait) in pop-up window at the bottom of the screen. Clicking on this button opens the browser at a temporary domain assigned by Codespaces. Alternatively, you can click a link provided in the terminal window that will open up the browser. That link looks like this: *Running on http://127.0.0.1:5000*.

When you open up the browser you are at the root (`/`) level. Your greeting should appear:

**User Database Management**
<br>
**Authorized Users Only**

If you add a `/revise` to the domain name, this JSON object should appear:

```
{
  "error": "Please provide a username."
}
```
 If you add a username parameter, as in `/revise?username=George_Washington`, a JSON object similar to this should appear:

```
{
  "userid": 1,
  "username": "George_Washington",
  "password": 1799,
  "auth": 1
}
```
In other words, A JSON object containing a *user_id*, *user_name* and 
*auth_level*. 

Finally, If you add a username parameter and a new authorization level, for example in `/revise?username=george_washington&auth=5`, a JSON object should be returned showing the authorization level has been changed:

```
{
 "userid": 1,
 "username": "George_Washington",
 "password": 1799,
 "auth": 5 
}
```


## Rubric

| Criteria                                     | Points |
|----------------------------------------------|--------|
| `/revise` test access row existing user      | 10     |
| `/revise` test access row non existing user  | 10     |
| `/revise` test update auth existing user     | 10     |
| `/revise` test update auth non existing user | 10     |
| Code is submitted to github                  | 10     |
| **Total**                                    | **50** |