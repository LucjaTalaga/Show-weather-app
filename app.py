from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    mssg = "A pewnie, że tak"
    return render_template("index.html", mssg = mssg)

if __name__ == '__main__':
    app.run()
