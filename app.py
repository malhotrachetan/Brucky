from flask import *
app=Flask(__name__, static_url_path='/static')

@app.route("/")
def main():
    return render_template('index.html')




if __name__=="__main__":
    app.run()
    app.debug=True