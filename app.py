from flask import *
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'bhoolnamat'
app.config['MYSQL_DATABASE_DB'] = 'brucky'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cur = conn.cursor()
            _hashed_password = generate_password_hash(_password)

            cur.callproc('sp_createUser',(_name, _email, _hashed_password))
            data = cur.fetchall()

            if len(data) is 0:
                conn.commit()
                return jsonify({'message': 'User created successfully !'})
            else:
                return jsonify({'error': str(data[0])})
        else:
            return jsonify({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return jsonify({'error!!': str(e)})



if __name__ == "__main__":
    app.run()