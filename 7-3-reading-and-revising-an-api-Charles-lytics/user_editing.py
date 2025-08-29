from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')  # The root/Index of the server
def home():
    return '''<span style='text-align:center'>
                <h1>User Management System</h1>
                <h3>Authorized Users Only</h3><hr/>
            </span>'''
            
@app.route('/revise')    # domain/revise route
def edit_request():
    username = request.args.get('username')  # URL form: /revise?username=x&auth=y
    auth = request.args.get('auth')  

    # Missing username
    if not username:
        return jsonify({'error': 'Please provide username.'}), 400

    # If auth not provided → just get record
    elif not auth:
        user = access_row(username)
        if user:
            return jsonify(user)
        else:
            return jsonify({'User not found': username}), 400

    # If auth provided → update
    else:
        user = access_row(username)  # get user with this username
        if user:
            try:
                auth = float(auth)  # change string from URL to decimal
            except ValueError:
                return jsonify({'error': 'Auth level must be a number.'}), 400
            update_auth(username, auth)  # Call SQL update method
            user = access_row(username)  # Get updated version
            return jsonify(user)
        else:
            return jsonify({'User not found': username}), 400

def access_row(username):
    conn = sqlite3.connect('people.db')  # Connect
    cursor = conn.cursor()  # Get cursor
    cursor.execute("SELECT username, auth_level FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()  # Get row
    conn.close()  # Release resources
    if user:
        return {'username': user[0], 'auth_level': user[1]}  # return as dict
    else:
        return False

def update_auth(username, auth_level):
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET auth_level = ? WHERE username = ?", (auth_level, username))
    conn.commit()  # Ensure the update is saved
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
