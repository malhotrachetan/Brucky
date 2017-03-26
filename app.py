from flask import *
from flaskext.mysql import MySQL
from werkzeug import *

mysql = MySQL()
app = Flask(__name__)
app.secret_key="What if I don't give you the key?"

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
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')

#userHome
@app.route("/userHome")
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = "Unauthorized access")

#method for logout
@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect("/")

#validating the signin/login
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
                return redirect("/userHome")
            else:
                return render_template("error.html",error="Wrong email or password!!")
        else:
            return render_template("error.html",error="Wrong email or password!!")

    except Exception as e:
        return render_template('error.html',error=str(e))




#logic for signup
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
            check = cur.execute('select user_email from table_user where user_email=p_email')

            if len(data) is 0:
                conn.commit()
                return jsonify({'message': 'User created successfully !'})
            elif check == _email:
                return render_template('userHome.html')
            else:
                return jsonify({'error': str(data[0])})

        else:
            return jsonify({'html': '<span>Enter the required fields</span>'})
    #output the exception in the web console
    except Exception as e:
        return jsonify({'error!!': str(e)})






if __name__ == "__main__":
    app.run()