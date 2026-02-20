from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/shorten', methods=['POST'])
def shorten():
    pass

@app.route('/login')
def auth():
    return render_template("auth.html")

@app.route('/history')
def history():
    return render_template("history.html")

@app.route('/logout')
def logout():
    pass

@app.route('/<code>')
def redirect_short(code):
    pass

if __name__ == "__main__":
    app.run(debug=True)