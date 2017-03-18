from flask import *
from flaskext.mysql import *
from werkzeug import generate_password_hash, check_password_hash

mysql=MySQL()
app=Flask(__name__,static_url_path='/static')

#configuring MySQL
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='bhoolnamat'
app.config['MYSQL_DATABASE_DB']='brucky'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('main.html')


@app.route("/showSignUp")
def showSignUP():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        # read posted values from the form
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validating the received values
        if _name and _email and _password:
            #call mysql

            conn=MySQL.connect()
            cursor=conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data=cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created sucessfully!'})
            else:
                return json.dumps({'error':str(data[0])})

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})




if __name__=="__main__":
    app.run()
    app.debug=True
