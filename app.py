from flask import *
app=Flask(__name__,static_url_path='/static')

@app.route("/")
def main():
    return render_template('main.html')


@app.route("/showSignUp")
def showSignUP():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST'])
def signUp():
    #read posted values from the form
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    #validating the received values
    if _name and _email and _password:
        return json.dumps({'html':'<span>All fields good!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


if __name__=="__main__":
    app.run(host='127.0.0.1', port=8080)
    app.debug=True