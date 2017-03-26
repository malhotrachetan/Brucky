from flask import *
from flaskext.mysql import MySQL
from werkzeug import *

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'bhoolnamat'
app.config['MYSQL_DATABASE_DB'] = 'brucky'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#mainpage
@app.route('/')
def main():
    return render_template('main.html')

#signup
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

#signin
@app.route("/showSignin")
def showSignin():
    return render_template('signin.html')


@app.route("/validateLogin",methods=["POST"])
def validateLogin():

    try:
        _email=request.form['inputEmail']
        _password=request.form['inputPassword']

        #connect to mysql
        con=mysql.connect()
        cursor=con.cursor()
        cursor.callproc('sp_validateLogin',(_email,))
        data=cursor.fetchall()

        if len(data)>0:
            if check_password_hash(str(data[0][3]),_password):
                return 





@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # calling mysql stored procedures for making a new user

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
    #output the exception in the web console
    except Exception as e:
        return jsonify({'error!!': str(e)})






if __name__ == "__main__":
    app.run()