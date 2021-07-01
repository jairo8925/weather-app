from flask import Flask
from flask import render_template
import sys

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
